# -*- coding: utf-8 -*-

# This source file is available in python_source/data_processing/filters.py

from psychopy.iohub.datastore.util import ExperimentDataAccessUtility
from psychopy.iohub import EventConstants
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties

from scipy.ndimage.filters import gaussian_filter1d
from scipy.signal import butter,filtfilt,medfilt

from common_workshop_functions import processSampleEventGaps,VisualAngleCalc,savitzky_golay

calibration_area_info=dict(display_size_mm=(340,280.0),
                           display_res_pix=(1280.0,1024.0),
                           eye_distance_mm=590.0)


def filterEyeSamples(filter_type,xpix,ypix,pupil,invalid_data_mask,**kwargs):
    processSampleEventGaps(xpix,ypix,pupil,invalid_data_mask,'linear')        
    vac=VisualAngleCalc(**calibration_area_info)    
    xdeg,ydeg=vac.pix2deg(xpix,ypix)

    if filter_type=='butter':  
        wn=kwargs.get('wn',0.2)
        order=kwargs.get('order',2)
        b, a = butter(order, wn, 'low')                    
        x_filtered = filtfilt(b, a, xdeg)
        y_filtered = filtfilt(b, a, ydeg)
        
    elif filter_type=='gauss':  
        sigma=kwargs.get('sigma',2)
        x_filtered = gaussian_filter1d(xdeg,sigma)
        y_filtered = gaussian_filter1d(ydeg,sigma)
            
    elif filter_type=='median':  
        size=kwargs.get('size',5)
        x_filtered=medfilt(xdeg,size)
        y_filtered=medfilt(ydeg,size)
    
    elif filter_type=='sg':  
        size=kwargs.get('size',7)
        order=kwargs.get('order',2)
        x_filtered=savitzky_golay(xdeg,window_size=size, order=order)
        y_filtered=savitzky_golay(ydeg,window_size=size, order=order)

    elif filter_type=='average':  
        weights=np.asarray(kwargs.get('weights',[1.,2.,3.,2.,1.]))
        weights=weights/np.sum(weights)  
        x_filtered=np.convolve(xdeg, weights,'same')
        y_filtered=np.convolve(ydeg, weights,'same')

    else:
        raise ValueError('Unknown Filter Type: %s. Must be one of %s'%(filter_type,str(['sg','butter','gauss','median'])))

    xdeg[invalid_data_mask]=np.NaN
    ydeg[invalid_data_mask]=np.NaN
    x_filtered[invalid_data_mask]=np.NaN
    y_filtered[invalid_data_mask]=np.NaN  

    return (xdeg,ydeg),(x_filtered,y_filtered)

# Enter data for use in this example
#
# We will do the pixel to degree calculation and plotting for one trial in
# the sample data file, select which to use (0 - 4):
#
TRIAL_INDEX=3
# Enter the eye tracker setup used for the data collection.
#
calibration_area_info=dict(display_size_mm=(500,280.0),
                           display_res_pix=(1280.0,1024.0),
                           eye_distance_mm=550.0)

dataAccessUtil=ExperimentDataAccessUtility('../hdf5_files','remote_data.hdf5', 
                                           experimentCode=None,sessionCodes=[])
# Get the filtered event data.
#
event_type=EventConstants.BINOCULAR_EYE_SAMPLE
retrieve_attributes=('time','left_gaze_x','left_gaze_y','left_pupil_measure1',
            'right_gaze_x','right_gaze_y','right_pupil_measure1','status')
trial_event_data=dataAccessUtil.getEventAttributeValues(event_type,
            retrieve_attributes,
            conditionVariablesFilter=None,
            startConditions={'time':('>=','@TRIAL_START@')},
            endConditions={'time':('<=','@TRIAL_END@')},
            )

trial_data=trial_event_data[TRIAL_INDEX]

time=trial_data.time
status=trial_data.status
pix_x=trial_data.right_gaze_x
pix_y=trial_data.right_gaze_y
pupil=trial_data.right_pupil_measure1
invalid_data_mask=trial_data.status%10>=2

# No need to keep the hdf5 file open anymore...
#
dataAccessUtil.close()

# Get the range to use for the x axis
# 
tmin=time.min()//1
tmax=time.max()//1+1

#filter_label='butter'
#unfiltered,filtered=filterEyeSamples(filter_label,pix_x,pix_y,pupil,invalid_data_mask,wn=0.2,order=2)

#filter_label='gauss'
#unfiltered,filtered=filterEyeSamples(filter_label,pix_x,pix_y,pupil,invalid_data_mask,sigma=1.5)

#filter_label='median'
#unfiltered,filtered=filterEyeSamples(filter_label,pix_x,pix_y,pupil,invalid_data_mask,size=5)

#filter_label='sg'
#unfiltered,filtered=filterEyeSamples(filter_label,pix_x,pix_y,pupil,invalid_data_mask,size=7,order=2)

filter_label='average'
unfiltered,filtered=filterEyeSamples(filter_label,pix_x,pix_y,pupil,invalid_data_mask,weights=[.5,1.5,3,6,3,1.5,.5])
unfiltered_x,unfiltered_y=unfiltered
filtered_x,filtered_y=filtered

# Create a plot of filtered and unfiltered eye position for the full trial.
#                                     
fig = plt.figure(figsize=(12,8))
fig.suptitle("%s Filtered and Unfiltered Eye Sample Data"%(filter_label.upper()),fontsize=14)
gax=plt.gca()
gax.plot(time, unfiltered_x,label='X Filtered',color=(1,.5,.25))
gax.plot(time, unfiltered_y,label='Y Filtered',color=(.25,.5,1))
gax.plot(time, filtered_x,label='X Unfiltered',color=(.5,.25,0))
gax.plot(time, filtered_y,label='Y Unfiltered',color=(0,.25,.5))
plt.xticks(np.arange(tmin,tmax,0.5),rotation='vertical')

trans = mtransforms.blended_transform_factory(gax.transData, gax.transAxes)
gax.fill_between(time, 0, 1, where=invalid_data_mask, facecolor='DarkRed',
                      alpha=0.5, transform=trans)
gax.set_ylabel('Degrees')
gax.set_xlabel('Time (sec)')

box = gax.get_position()
gax.set_position([box.x0, box.y0, box.width, box.height-.05])
fontP = FontProperties()
fontP.set_size('small')
plt.legend(loc='upper left', bbox_to_anchor=(.8, 1.15), borderaxespad=0,prop = fontP)

plt.show()
