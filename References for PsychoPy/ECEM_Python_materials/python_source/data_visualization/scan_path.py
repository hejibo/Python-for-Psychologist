# This Python Source File Available in python_source/data_visualization/scan_path.py

from psychopy.iohub.datastore.util import ExperimentDataAccessUtility
from psychopy.iohub import EventConstants

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.collections import LineCollection

from common_workshop_functions import processSampleEventGaps

import numpy as np

# Load an ioDataStore file containing 1000 Hz sample data from a 
# head supported eye tracker that was recording the right eye.
# 
dataAccessUtil=ExperimentDataAccessUtility('..\hdf5_files','head_supported_data.hdf5', 
                                           experimentCode=None,sessionCodes=[])

##### STEP A. #####
# Retrieve a subset of the MONOCULAR_EYE_SAMPLE event attributes, for events that occurred
# between each time period defined by the TRIAL_START and TRIAL_END trial variables of each entry
# in the trial_conditions data table.
#
event_type=EventConstants.MONOCULAR_EYE_SAMPLE
retrieve_attributes=('time','gaze_x','gaze_y','pupil_measure1','status')
trial_event_data=dataAccessUtil.getEventAttributeValues(event_type,
                            retrieve_attributes,
                            conditionVariablesFilter=None, 
                            startConditions={'time':('>=','@TRIAL_START@')},
                            endConditions={'time':('<=','@TRIAL_END@')})

# No need to keep the hdf5 file open anymore...
#
dataAccessUtil.close()

# Process and plot the sample data for each trial in the data file.
#
for trial_index,trial_data in enumerate(trial_event_data):
    plt.close()    
    ##### STEP B. #####
    # Find all samples that have missing eye position data and filter the eye position
    # and pupil size streams so that the eye track plot is more useful. In this case that
    # means setting position fields to NaN and pupil size to 0.
    #
    
    # Eye manufacturer specific missing data indicator
    #
    invalid_data_mask=trial_data.pupil_measure1==0

    
    # Get the needed left eye sample arrays 
    #
    gaze_x=trial_data.gaze_x
    gaze_y=trial_data.gaze_y
    pupil_size=trial_data.pupil_measure1
    
    # Process the eye fields using the processSampleEventGaps function defined
    # in the common_workshop_functions.py file. The last arguement of 'clear'
    # tells the function to set any x or y position missing data samples to NaN 
    # and to set the pupil size field to 0. The operations are preformed in-place
    # on the numpy arrays passed to the function.
    # The returned valid_data_periods is a list of each group of temporally adjacent 
    # samples that are valid, but providing a list where each element is the (start, stop)
    # index for a given period of valid data.
    #
    valid_data_periods=processSampleEventGaps(gaze_x,gaze_y,
                                                   pupil_size,
                                                   invalid_data_mask,
                                                   'clear')
                                                   
    # get the array of sample times for the current trial
    #
    time=trial_data.time

    # Start plotting for the trial
    plt.figure(figsize=(12,8))

    ##### STEP C. #####
    # Create Image background for each trial scanpath
    # Get the condition variable set used for the current trial
    #
    condition_set=trial_data.condition_set    
    # Get the image name and trial_id from the condition data for
    # the trial.
    #
    image_name=condition_set.IMAGE_NAME
    trial_id=condition_set.trial_id    
    plt.title("Trial {0}: {1}".format(trial_id,image_name))
    # Load the image
    #
    trial_image_array=np.flipud(mpimg.imread("./images/"+image_name))
    # Get background image size
    #
    image_size=(trial_image_array.shape[1],trial_image_array.shape[0])
    ihw,ihh=image_size[0]/2,image_size[1]/2
    # Draw the image to the plot
    #
    bip=plt.imshow(trial_image_array,origin='lower',extent=(-ihw, ihw,-ihh, ihh))
    
    ##### STEP D. #####
    # To create the scan path data for the plot, convert the two 1D numpy
    # arrays into one 2D array of shape (num_samples,2), where the second
    # dimention is the x,y position for every sample in num_samples.
    #
    sample_points = np.array([gaze_x, gaze_y]).T.reshape(-1, 1, 2)
    
    # To create the csan path graphics, we will create one line for every sample
    # position point by specifying the start and end point of each line as
    # x1,y1,x2,y2 ... xn-1,yn-1,xn,yn, where n == the number of sample points
    # in the trial.
    #
    sample_segments = np.concatenate([sample_points[:-1], sample_points[1:]], axis=1)

    # Create the actual matplotlib line graphics group, and use the built in
    # color map 'YlOrRd', meaning Yellow->Orange->Red
    #
    scan_path_line_collection = LineCollection(sample_segments, 
                                               cmap=plt.get_cmap('YlOrRd'),
                                               norm=plt.Normalize(time.min(), time.max()))
    scan_path_line_collection.set_array(time)
    scan_path_line_collection.set_linewidth(2)
    plt.gca().add_collection(scan_path_line_collection)
    
    ##### STEP E. #####
    # Display the color bar and different sample times associated with the 
    # different colors in the color range.
    #
    cb=plt.colorbar(scan_path_line_collection)

    # Give the Color Bar a title
    #
    cb.set_label("Trial Time (sec)") 

    plt.show()
    