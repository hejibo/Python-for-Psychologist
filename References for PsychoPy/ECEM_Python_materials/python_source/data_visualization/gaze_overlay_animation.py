# This Python Source File Available in python_source/data_visualization/gaze_overlay_animation.py

# This is a slightly more advanced demo to show you fancy things like animations
#
# It's based on a how-to about python plotting animations at
# http://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
# It is also possible to save the animation as a video file

from psychopy.iohub.datastore.util import ExperimentDataAccessUtility
from psychopy.iohub import EventConstants

#import some maths/plotting libs
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import animation

#import our own helper funcs (from the python_source folder)
from common_workshop_functions import processSampleEventGaps

##### STEP A. #####
# Load an ioDataStore file containing 1000 Hz sample data from a 
# head supported eye tracker that was recording the right eye. 
dataAccessUtil=ExperimentDataAccessUtility('../hdf5_files',
                                           'head_supported_data.hdf5', 
                                           experimentCode=None,
                                           sessionCodes=[])

TRIAL_ID=1 #we'll just play back a single trial here
et_sampling_rate=1000.0 #eye tracker sampling rate
desired_playback_rate=20 #what rate (in Hz) will we update our figure (not every eye frame!)

# Retrieve a subset of the MONOCULAR_EYE_SAMPLE event attributes, for events that occurred
# between each time period defined by the TRIAL_START and TRIAL_END trial variables of each entry
# in the trial_conditions data table.
event_type=EventConstants.MONOCULAR_EYE_SAMPLE
retrieve_attributes=('time','gaze_x','gaze_y','pupil_measure1','status')
trial_event_data=dataAccessUtil.getEventAttributeValues(event_type,
                            retrieve_attributes,
                            conditionVariablesFilter=None, 
                            startConditions={'time':('>=','@TRIAL_START@')},
                            endConditions={'time':('<=','@TRIAL_END@')})

# No need to keep the hdf5 file open anymore...
dataAccessUtil.close()

# Get the data for the one trial we will playback
trial_data=trial_event_data[TRIAL_ID]

##### STEP B. #####
# Get the needed left eye sample arrays 
gaze_x=trial_data.gaze_x
gaze_y=trial_data.gaze_y
pupil_size=trial_data.pupil_measure1
# get the array of sample times for the current trial
time=trial_data.time
#clear absent data
invalid_data_mask = (trial_data.pupil_measure1==0) #vendor specific codes
valid_data_periods=processSampleEventGaps(gaze_x,gaze_y,
                                               pupil_size,
                                               invalid_data_mask,
                                               'clear')

##### STEP C. #####       
# Load the image used in the current trial.                                        
# get the trial condition values used for each trial in example experiment.
condition_set=trial_data.condition_set 
# Get the image name used for display during the trial
image_name=condition_set.IMAGE_NAME
trial_id=condition_set.trial_id

# load the image as a numpy array
trial_image_array=np.flipud(mpimg.imread("./images/"+image_name))

# Reduce size for easier viewing
w, h = trial_image_array.shape[1]/2, trial_image_array.shape[0]/2

##### STEP D. #####
# Create the Animated Figure
dpi = 100
margin = 0.05 # (add 5% of the width/height of the figure...)

# Make a figure big enough to accomodate an axis of xpixels by ypixels
# as well as the ticklabels, etc...
figsize =  w / dpi,  h / dpi
fig = plt.figure(figsize=figsize, dpi=dpi)
plt.title("Trial %i: %s" %(trial_id,image_name))
# get the current axes
ax = fig.gca()

# Draw the background image array
ax.imshow(trial_image_array,origin='lower',extent=(-w/2, w/2,-h/2, h/2))

# Create a circle graphic to use as the gaze overlay cursor.
circle = plt.Circle((1000, 1000), radius=9, facecolor='r',edgecolor='y', 
                    linewidth=2, alpha=0.7)
                    
# Create a semi-transparent text box to display the current trial time.
time_text = ax.text(0.02, 0.95, '', color='black', fontsize=12, 
                    bbox={'facecolor':'red', 'alpha':0.5, 'pad':10},
                    transform=ax.transAxes)

# Calculate the eye trackers sampling rate in msec.
ifi=1000.0/et_sampling_rate
# Calculate how many samples occur within the requested playback rate.
sample_frame_interval=desired_playback_rate//ifi+1 #note that // means integer divide
actual_playback_rate=int(sample_frame_interval*ifi) #true rate after rounding
sample_frame_count=int(len(time)/sample_frame_interval) #true n frames after rounding

# Create the matplotlib Animation object
def init():
    """
    This gets called each time the animation first starts.
    You must return any of the plot graphics that change
    Each frame of the animation.
    """
    ax.add_patch(circle)
    time_text.set_text('time = %.1f sec' % time[0])
    return circle,time_text

def animate(i):
    """
    This gets called each frame of the animation.
    This is where the animated graphics can be updated for the next frame.
    You must return any of the plot graphics that change
    Each frame of the animateion.
    """
    s=int(i*sample_frame_interval)
    circle.center = (gaze_x[s]/2., gaze_y[s]/2.)
    time_text.set_text('time = %.1f sec' % time[s])
    return circle,time_text

# Start the animation, but only play it for 1 frame
# (This gets around a current bug in the matplotlib animation code when
# you want to use blit=True during the real playback; which you do as it is
# 10x faster than when blit=False)
anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=1, 
                               interval=actual_playback_rate,
                               blit=False)

# Start the animation for real this time. Based on the args provided,
# the animation will play from start to finish and then loop to the
# start and play over again. This repeats until you close the matplotlib window.
anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=sample_frame_count, 
                               interval=actual_playback_rate,
                               blit=True)

plt.show()
