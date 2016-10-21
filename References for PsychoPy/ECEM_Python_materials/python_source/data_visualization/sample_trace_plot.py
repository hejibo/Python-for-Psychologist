# This Python Source File Available in python_source/data_visualization/sample_trace_plot.py

from psychopy.iohub.datastore.util import ExperimentDataAccessUtility
from psychopy.iohub import EventConstants

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties

from common_workshop_functions import processSampleEventGaps

import numpy as np

# Load an ioDataStore file containing 120 Hz sample data from a
# remote eye tracker that was recording both eyes. In the plotting example
dataAccessUtil=ExperimentDataAccessUtility('../hdf5_files','remote_data.hdf5', experimentCode=None,sessionCodes=[])

##### STEP A. #####
# Retrieve a subset of the BINOCULAR_EYE_SAMPLE event attributes, for events that occurred
# between each time period defined by the TRIAL_START and TRIAL_END trial variables of each entry
# in the trial_conditions data table.
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

# No need to keep the hdf5 file open anymore...
#
dataAccessUtil.close()

# Process and plot the sample data for each trial in the data file.
#
for trial_index,trial_samples in enumerate(trial_event_data):
    ##### STEP B. #####
    # Find all samples that have missing eye position data and filter the eye position
    # and pupil size streams so that the eye track plot is more useful. In this case that
    # means setting position fields to NaN and pupil size to 0.
    #
    # left eye manufacturer specific missing data indicator
    left_eye_invalid_data_masks=trial_samples.status//10>=2
    # Right eye manufacturer specific missing data indicator
    right_eye_invalid_data_masks=trial_samples.status%10>=2
    # Get the needed left eye sample arrays
    #
    left_gaze_x=trial_samples.left_gaze_x
    left_gaze_y=trial_samples.left_gaze_y
    left_pupil_size=trial_samples.left_pupil_measure1
    # Process the left eye fields using the processSampleEventGaps function defined
    # in the common_workshop_functions.py file. The last argument of 'clear'
    # tells the function to set any x or y position missing data samples to NaN
    # and to set the pupil size field to 0. The operations are preformed in-place
    # on the numpy arrays passed to the function.
    # The returned valid_data_periods is a list of each group of temporally adjacent
    # samples that are valid, but providing a list where each element is the (start, stop)
    # index for a given period of valid data.
    #
    left_valid_data_periods=processSampleEventGaps(left_gaze_x,left_gaze_y,
        left_pupil_size,
        left_eye_invalid_data_masks,
        'clear')

    # Get the needed right eye sample field arrays
    #
    right_gaze_x=trial_samples.right_gaze_x
    right_gaze_y=trial_samples.right_gaze_y
    right_pupil_size=trial_samples.right_pupil_measure1

    # Process the right eye fields
    #
    right_valid_data_periods=processSampleEventGaps(right_gaze_x,right_gaze_y,
        right_pupil_size,
        right_eye_invalid_data_masks,
        'clear')

    # get the array of sample times for the current trial
    time=trial_samples.time
    ##### STEP C. #####
    # Plot the sample traces for x and y gaze positions separately for each eye
    # using two sub plots.
    #
    # Get the range to use for the x axis
    tmin=time.min()//1
    tmax=time.max()//1+1

    #Create a 12x8 inch figure
    fig = plt.figure(figsize=(12,8))
    # Create a subplot for the left eye, 2,1,1 means the subplot
    # grid will be 2 rows and 1 column, and we are about to create
    # the subplot for row 1 of 2
    #"Left Eye Position"
    left_axis = fig.add_subplot(2,1,1)
    left_axis.plot(time,left_gaze_x,label="X Gaze")
    left_axis.plot(time,left_gaze_y,label="Y Gaze")
    plt.xticks(np.arange(tmin,tmax,0.5),rotation='vertical')
    # Fill in missing eye data areas of the plot with a vertical bar the full
    # height of the sub plot.
    trans = mtransforms.blended_transform_factory(left_axis.transData, left_axis.transAxes)
    left_axis.fill_between(time, 0, 1, where=left_pupil_size==0,
            facecolor='DarkRed',
            alpha=0.5, transform=trans)
    #text(0.5, 0.95, 'test', transform=fig.transFigure, horizontalalignment='center')
    left_axis.set_ylabel('Position (pixels)')
    # Left Eye Sample Sub Plot
    left_axis.set_title("Left Eye Position", fontsize=12)

    # Resize the plot x axis by 85% so that the legend , which is outside
    # the plot, will still fit in the matplotlib window.
    #
    box = left_axis.get_position()
    left_axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0,prop = fontP)
    # Right Eye Sample Sub Plot
    # Basically the same as the left eye, but we are adding to the row 2 sub plt now.
    #
    right_axis = fig.add_subplot(2,1,2,sharex=left_axis,sharey = left_axis)
    right_axis.plot(time,right_gaze_x,label="X Gaze")
    right_axis.plot(time,right_gaze_y,label="Y Gaze")
    plt.xticks(np.arange(tmin,tmax,0.5),rotation='vertical')
    trans = mtransforms.blended_transform_factory(right_axis.transData, right_axis.transAxes)
    right_axis.fill_between(time, 0, 1, where=right_pupil_size==0,
            facecolor='DarkRed',
            alpha=0.5, transform=trans)
    right_axis.set_xlabel('Time')
    right_axis.set_ylabel('Position (Pixels)')
    right_axis.set_title("Right Eye Position", fontsize=12)
    plt.subplots_adjust(hspace=0.35, bottom=0.125)
    fig.suptitle("Eye Sample Data For Trial Index %d"%(trial_index+1),fontsize=14)

    # Show each trial's eye sample trace. The program will block until you close
    # the trial plot, and will then open the next trial plt.
    #
    plt.show()