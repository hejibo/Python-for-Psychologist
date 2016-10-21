from psychopy.iohub.datastore.util import ExperimentDataAccessUtility
from psychopy.iohub import EventConstants
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties
import scipy
import scipy.signal

from common_workshop_functions import processSampleEventGaps,VisualAngleCalc,calculateVelocity


SPATIAL_FILTER_WINDOW_SIZE=5
VELOCITY_FILTER_WINDOW_SIZE=5

calibration_area_info=dict(display_size_mm=(340,280.0),
                           display_res_pix=(1280.0,1024.0),
                           eye_distance_mm=590.0)


def createTrialDataStreams():
    trial_data_streams=[]

    # Get the filtered event data.
    # We will use right eye data only for the testing..
    #
    dataAccessUtil=ExperimentDataAccessUtility('../hdf5_files','remote_data.hdf5', 
                                           experimentCode=None,sessionCodes=[])

    event_type=EventConstants.BINOCULAR_EYE_SAMPLE
    retrieve_attributes=('time','right_gaze_x','right_gaze_y','right_pupil_measure1','status')
    trial_event_data=dataAccessUtil.getEventAttributeValues(event_type,
                retrieve_attributes,
                conditionVariablesFilter=None,
                startConditions={'time':('>=','@TRIAL_START@')},
                endConditions={'time':('<=','@TRIAL_END@')},
                )
 
    dataAccessUtil.close()
    
    for t,trial_data in enumerate(trial_event_data):
        #Create a mask to be used to define periods of missing data in a data trace (eye tracker dependent)
        #
        invalid_data_mask=trial_data.status%10>=2
        
        time=trial_data.time
        pupil=trial_data.right_pupil_measure1
        # Get x, y eye position traces (in pixels), setting sample positions where there is track loss
        # to NaN.
        xpix_cleared=trial_data.right_gaze_x.copy()
        ypix_cleared=trial_data.right_gaze_y.copy()
        processSampleEventGaps(xpix_cleared,ypix_cleared,pupil,invalid_data_mask,'clear')
    
        # Get x, y eye position traces (in pixels), setting sample positions 
        # where there is track loss to be linearly interpolated using each 
        # missing_sample_start-1 and missing_sample_end+1 as the points to
        # interpolate between.
        #
        xpix_linear=trial_data.right_gaze_x.copy()
        ypix_linear=trial_data.right_gaze_y.copy()
    
        # valid_data_periods is a list of array slice objects giving the start,end index of each non missing 
        # period of in the data stream.
        #
        valid_data_periods=processSampleEventGaps(xpix_linear,ypix_linear,pupil,invalid_data_mask,'linear')
     
        # Convert from pixels to visual angle coordinates
        calibration_area_info=dict(display_size_mm=(340,280.0),
                           display_res_pix=(1280.0,1024.0),
                           eye_distance_mm=590.0)
        vac=VisualAngleCalc(**calibration_area_info)      
        xdeg,ydeg=vac.pix2deg(xpix_linear,ypix_linear)
    
        # Create Filtered versions of the x and y degree data traces
        # We'll use the Median Filter...
        #
        xdeg_filtered = scipy.signal.medfilt(xdeg,SPATIAL_FILTER_WINDOW_SIZE)
        ydeg_filtered = scipy.signal.medfilt(ydeg,SPATIAL_FILTER_WINDOW_SIZE)
        
        # Create the velocity stream
        #
        xvel=calculateVelocity(time,xdeg_filtered)
        yvel=calculateVelocity(time,ydeg_filtered)

        # Filter the velocity data
        #
        FILTER_ORDER=2
        Wn=0.3
        b, a = scipy.signal.butter(FILTER_ORDER, Wn, 'low')
        ffunc=scipy.signal.filtfilt
        xvel_filtered = ffunc(b, a, xvel)
        yvel_filtered = ffunc(b, a, yvel)

#        xvel_filtered=savitzky_golay(xvel,window_size=VELOCITY_FILTER_WINDOW_SIZE,order=2)
#        yvel_filtered=savitzky_golay(yvel,window_size=VELOCITY_FILTER_WINDOW_SIZE,order=2)
#        xvel_filtered=gaussian_filter1d(xvel,VELOCITY_FILTER_WINDOW_SIZE)
#        yvel_filtered=gaussian_filter1d(yvel,VELOCITY_FILTER_WINDOW_SIZE)
#        xvel_filtered=scipy.signal.medfilt(xvel,VELOCITY_FILTER_WINDOW_SIZE)
#        yvel_filtered=scipy.signal.medfilt(yvel,VELOCITY_FILTER_WINDOW_SIZE)

        velocity=np.sqrt(xvel*xvel+yvel*yvel)
        velocity_filtered=np.sqrt(xvel_filtered*xvel_filtered+yvel_filtered*yvel_filtered)

        # Create a data trace dictionary for all the different types
        #  of data traces created for the trial
        #
        trial_data={}
        trial_data['time']=time
        trial_data['xpix_cleared']=xpix_cleared
        trial_data['ypix_cleared']=ypix_cleared
        trial_data['xpix_linear']=xpix_linear
        trial_data['xpix_linear']=xpix_linear
        trial_data['xdeg']=xdeg
        trial_data['ydeg']=ydeg
        trial_data['xdeg_filtered']=xdeg_filtered
        trial_data['ydeg_filtered']=ydeg_filtered
        trial_data['pupil']=pupil
        trial_data['velocity']=velocity
        trial_data['velocity_filtered']=velocity_filtered
        trial_data['valid_data_periods']=valid_data_periods
        trial_data['missing_data_mask']=invalid_data_mask
        # Add the data trace dictionary to a list
        #
        trial_data_streams.append(trial_data)
    return trial_data_streams

def calculateVelocityThresholdPerTrial(trial_data_streams):
    for t,trial_data in enumerate(trial_data_streams):        
        pt_list=[]        
        missing_data_mask=trial_data['missing_data_mask']
        valid_velocity_filtered=trial_data['velocity_filtered'][~missing_data_mask[1:-1]]
        PT=valid_velocity_filtered.min()+valid_velocity_filtered.std()*3.0
        velocity_below_thresh=valid_velocity_filtered[valid_velocity_filtered<PT]
        PTd=2.0
        while PTd >= 1.0:   
            if len(pt_list)>0:
                PT=velocity_below_thresh.mean()+3.0*velocity_below_thresh.std()
                velocity_below_thresh=valid_velocity_filtered[valid_velocity_filtered<PT]
                PTd=np.abs(PT-pt_list[-1])
            pt_list.append(PT)

        saccade_candidate_mask=(trial_data['velocity_filtered']>=PT)
        saccade_candidate_mask[missing_data_mask[1:-1]]=0
        saccade_candidate_periods=np.ma.extras.notmasked_contiguous(
                                np.ma.array(trial_data['velocity_filtered'],
                                            mask=saccade_candidate_mask)
                                )                                
    
        trial_data['velocity_threshold_points']=np.asarray(pt_list)
        trial_data['saccade_candidate_mask']=saccade_candidate_mask
        trial_data['saccade_candidate_periods']=saccade_candidate_periods

def markEventTypes(trial_data_streams):
    MISSING=1
    SACCADE=4
    FIXATION=8
    
    eye_event_status=np.zeros(trial_data_streams[0]['time'].shape,dtype=np.uint8)

    for t,trial_traces_dict in enumerate(trial_data_streams):
        missing_data_mask=trial_traces_dict['missing_data_mask']
        saccade_candidate_mask=trial_traces_dict['saccade_candidate_mask']
        
        # Create event event status stream. 
        # Currently only tags missing data periods, saccades, 
        # and fills in the rest a Fixaions. 
        # This can be improved to distinguish between missing data 
        # periods that are likely from a blink, 
        # vs. other eye signal loss reason. Further more, it would be nice to 
        # determine periods of smooth persuite from the currently tagged Fixation
        # regions when possible.
        #
        eye_event_status[missing_data_mask]+=MISSING
        eye_event_status[saccade_candidate_mask]+=SACCADE
        eye_event_status[eye_event_status==0]+=FIXATION
        
        trial_traces_dict['eye_event_status']=eye_event_status
    
def plotParsingResults(trial_data_streams):
    deg_pos_colors=((0.,.25,0.),(0.,.75,0.),(0.,0.,.25),(0.,0.,.25),(0.,0.,0.))
    velocity_colors=((.25,0.,0.),(.75,0.,0.),(.5,0.,0.))
    
    for t,trial_traces_dict in enumerate(trial_data_streams):
        time=trial_traces_dict['time']
        pupil=trial_traces_dict['pupil']
        xdeg_filtered=trial_traces_dict['xdeg_filtered']
        ydeg_filtered=trial_traces_dict['ydeg_filtered']
        velocity_filtered=trial_traces_dict['velocity_filtered']
        missing_data_mask=trial_traces_dict['missing_data_mask']
        
        xdeg_filtered[missing_data_mask]=np.NaN
        ydeg_filtered[missing_data_mask]=np.NaN
        velocity_filtered[missing_data_mask[1:-1]]=np.NaN

        fig = plt.figure('Trial %d'%(t+1),figsize=(12,8))
        fig.title=("Trial %d Eye Data with Parsed Saccades"%(t+1))

        ax=plt.gca()
        ax.plot(time,xdeg_filtered,label='Filtered Horz. Pos. (Degrees)',color=deg_pos_colors[1])
        ax.plot(time,ydeg_filtered,label='Filtered Vert. Pos. (Degrees)',color=deg_pos_colors[3])

        tmin=time.min()//1
        tmax=time.max()//1+1

        plt.xticks(np.arange(tmin,tmax,0.5),rotation='vertical')
        trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
        
        # Missing data vertical bars
        ax.fill_between(time, 0, 1, where=pupil==0, facecolor=(.2,.2,.2), edgecolor=(.2,.2,.2),
                        alpha=0.5, transform=trans)


        # Saccade Canditates vertical bars
        ax.fill_between(time[1:-1], 0, 1, 
                        where=trial_traces_dict['velocity_filtered']>=trial_traces_dict['velocity_threshold_points'][-1],
                        facecolor=(.5,0,.5), edgecolor=(.5,0,.5),
                        alpha=0.5, transform=trans)

        ax.set_xlabel('Time')
        ax.set_ylabel('Position (Degrees)',color=deg_pos_colors[-1])
        for tl in ax.get_yticklabels():
            tl.set_color(deg_pos_colors[-1])
        
        ax2 = ax.twinx()
        ax2.plot(time[1:-1],velocity_filtered,label='Filtered XY Velocity',color=velocity_colors[1])
        ax2.set_ylabel('Velocity (degrees / second)',color=velocity_colors[-1])
        for tl in ax2.get_yticklabels():
            tl.set_color(velocity_colors[-1])

        plt.axhline(y=trial_traces_dict['velocity_threshold_points'][0],color='g')
        plt.axhline(y=trial_traces_dict['velocity_threshold_points'][-1],color='r')

        handles, labels = ax.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels()
        handles.extend(handles2)
        labels.extend(labels2)
#        plt.legend(handles,labels,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.) #plt.legend(loc=(1.01,.8))        

        box = ax2.get_position()
        ax.set_position([box.x0, box.y0, box.width, box.height-.05])
        ax2.set_position([box.x0, box.y0, box.width, box.height-.05])
        fontP = FontProperties()
        fontP.set_size('small')
        plt.legend(handles,labels, loc='upper left', bbox_to_anchor=(.8, 1.15), borderaxespad=0,prop = fontP)

        plt.grid()
        plt.show()

# Run the event parser test..
#
trial_data_streams=createTrialDataStreams()

calculateVelocityThresholdPerTrial(trial_data_streams)

markEventTypes(trial_data_streams)

plotParsingResults(trial_data_streams)