# -*- coding: utf-8 -*-
from psychopy.iohub.datastore.util import ExperimentDataAccessUtility
from psychopy.iohub import EventConstants

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties

from common_workshop_functions import processSampleEventGaps,VisualAngleCalc

# Enter data for use in this example
#
# We will process one of the two eye data streams available, indicate which:
#
USE_RIGHT_EYE=False
# We will do the pixel to degree calculation and plotting for one trial in
# the sample data file, select which to use (0 - 4):
#
TRIAL_INDEX=1
# Enter the eye tracker setup used for the data collection.
#
calibration_area_info=dict(display_size_mm=(340,280.0),
                   display_res_pix=(1280.0,1024.0),
                   eye_distance_mm=590.0)


##### STEP A. #####
# Retrieve a subset of the BINOCULAR_EYE_SAMPLE event attributes, for events that occurred
# between each time period defined by the TRIAL_START and TRIAL_END trial variables of each entry
# in the trial_conditions data table.
#
# Load an ioDataStore file containing 120 Hz sample data from a
# remote eye tracker that was recording both eyes. In the plotting example
#
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

if USE_RIGHT_EYE:    
    pix_x=trial_data.right_gaze_x
    pix_y=trial_data.right_gaze_y
    pupil=trial_data.right_pupil_measure1
    invalid_data_mask=trial_data.status%10>=2
else:
    pix_x=trial_data.left_gaze_x
    pix_y=trial_data.left_gaze_y
    pupil=trial_data.left_pupil_measure1
    invalid_data_mask=trial_data.status//10>=2
    
# No need to keep the hdf5 file open anymore...
#
dataAccessUtil.close()

##### STEP B. #####
# Use the VisualAngleCalc class defined in the common_workshop_functions to
# generate an object that can convert data from pixels to visual angles based
# on the supplied calibration / display surface geometry and eye distance.
#                            
vac=VisualAngleCalc(**calibration_area_info)
# Calculate the visual degree position in x and y for the given pixel position arrays.
#  
degree_x,degree_y=vac.pix2deg(pix_x,pix_y)

# Process the eye fields using the processSampleEventGaps function defined
# in the common_workshop_functions.py file. The last argument of 'clear'
# tells the function to set any x or y position missing data samples to NaN
# and to set the pupil size field to 0. The operations are preformed in-place
# on the numpy arrays passed to the function.
# The returned valid_data_periods is a list of each group of temporally adjacent
# samples that are valid, each element of the list is the (start, stop)
# index for a given period of valid data.
#
valid_data_periods=processSampleEventGaps(pix_x,pix_y,pupil,invalid_data_mask,
                                          'clear')
#### STEP C. ####
# Create a plot of eye position in pixels and visual degrees
#                                          
fig = plt.figure(figsize=(12,8))
fig.suptitle("Eye Sample Data For Trial Index %d"%(TRIAL_INDEX+1),fontsize=14)

# Get the range to use for the x axis
# 
tmin=time.min()//1
tmax=time.max()//1+1

# Create the y axis (time)
ax=plt.gca()
px=ax.plot(time, pix_x,label='X Position (Pixels)',color=(.5,.5,1))
py=ax.plot(time, pix_y,label='Y Position (Pixels)',color=(1,.5,.5))
plt.xticks(np.arange(tmin,tmax,0.5),rotation='vertical')

# Fill in missing eye data areas of the plot with a vertical bar the full
# height of the sub plot.
trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
ax.fill_between(time, 0, 1, where=pupil==0, facecolor='DarkRed',
                      alpha=0.5, transform=trans)
ax.set_ylabel('Pixels')
ax.set_xlabel('Time (sec)')

ax2 = ax.twinx()
dgx=ax2.plot(time, degree_x,label='X Position (Degrees)',color=(0,0,1))
dgy=ax2.plot(time, degree_y,label='Y Position (Degrees)',color=(1,0,0))
ax2.set_ylabel('Degrees')
# Resize the plot x axis by 85% so that the legend , which is outside
# the plot, will still fit in the matplotlib window.
#
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width, box.height-.05])
ax2.set_position([box.x0, box.y0, box.width, box.height-.05])
fontP = FontProperties()
fontP.set_size('small')

lns = px+py+dgx+dgy
labs = [l.get_label() for l in lns]
plt.legend(lns, labs, loc='upper left', bbox_to_anchor=(.8, 1.15), borderaxespad=0,prop = fontP)

plt.show()
