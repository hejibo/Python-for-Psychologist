# -*- coding: utf-8 -*-

# This source file is available in python_source/data_processing/velocity_accelleration.py

from psychopy.iohub.datastore.util import ExperimentDataAccessUtility
from psychopy.iohub import EventConstants
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
from matplotlib.font_manager import FontProperties

from common_workshop_functions import processSampleEventGaps,VisualAngleCalc,calculateVelocity,calculateAccelleration

# Enter data for use in this example
#
# We will do the pixel to degree calculation and plotting for one trial in
# the sample data file, select which to use (0 - 4):
#
TRIAL_INDEX=3
# Enter the eye tracker setup used for the data collection.
#
calibration_area_info=dict(display_size_mm=(340,280.0),
                   display_res_pix=(1280.0,1024.0),
                   eye_distance_mm=590.0)


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

# Use the VisualAngleCalc class defined in the common_workshop_functions to
# generate an object that can convert data from pixels to visual angles based
# on the supplied calibration / display surface geometry and eye distance.
#                            
vac=VisualAngleCalc(**calibration_area_info)
# Calculate the visual degree position in x and y for the given pixel position arrays.
#  
degree_x,degree_y=vac.pix2deg(pix_x,pix_y)

# Process the eye fields using the processSampleEventGaps function defined
# in the common_workshop_functions.py file. 
#
valid_data_periods=processSampleEventGaps(degree_x,degree_y,pupil,invalid_data_mask,
                                          'clear')

# calculate unfiltered velocity and accelleration streams
#
velocity=np.abs(calculateVelocity(time,degree_x,degree_y))
accelleration=calculateAccelleration(time,degree_x,degree_y)

pix_x[invalid_data_mask]=np.NaN
pix_y[invalid_data_mask]=np.NaN
degree_x[invalid_data_mask]=np.NaN
degree_y[invalid_data_mask]=np.NaN

# Get the range to use for the x axis
# 
tmin=time.min()//1
tmax=time.max()//1+1

# Create a subplot of eye position in degrees and velocity and a subplot
# of eye position in degrees and accelleration.                                      
fig = plt.figure(figsize=(12,8))
fig.suptitle("Eye Sample Data For Trial Index %d"%(TRIAL_INDEX+1),fontsize=14)

# position and velocity
#
gax=fig.add_subplot(2,1,1)
px=gax.plot(time, degree_x,label='X Position',color=(0,0,1))
py=gax.plot(time, degree_y,label='Y Position',color=(0,1,0))
plt.xticks(np.arange(tmin,tmax,0.5),rotation='vertical')

trans = mtransforms.blended_transform_factory(gax.transData, gax.transAxes)
gax.fill_between(time, 0, 1, where=invalid_data_mask, facecolor='DarkRed',
                      alpha=0.5, transform=trans)
gax.set_ylabel('Degrees')
gax.set_xlabel('Time (sec)')

vax = gax.twinx()
v=vax.plot(time[1:-1], velocity,label='Velocity',color=(1,0,0))
vax.set_ylabel('Degrees / Second')

box = gax.get_position()
gax.set_position([box.x0, box.y0, box.width, box.height-.05])
vax.set_position([box.x0, box.y0, box.width, box.height-.05])
fontP = FontProperties()
fontP.set_size('small')
lns = px+py+v
labs = [l.get_label() for l in lns]
plt.legend(lns, labs, loc='upper left', bbox_to_anchor=(.8, 1.15), borderaxespad=0,prop = fontP)

# position and accelleration
#
gax=fig.add_subplot(2,1,2)
px=gax.plot(time, degree_x,label='X Position',color=(0,0,1))
py=gax.plot(time, degree_y,label='Y Position',color=(0,1,0))
plt.xticks(np.arange(tmin,tmax,0.5),rotation='vertical')

trans = mtransforms.blended_transform_factory(gax.transData, gax.transAxes)
gax.fill_between(time, 0, 1, where=invalid_data_mask, facecolor='DarkRed',
                      alpha=0.5, transform=trans)
gax.set_ylabel('Degrees')
gax.set_xlabel('Time (sec)')

vax = gax.twinx()
v=vax.plot(time[2:-2], accelleration,label='Accelleration',color=(1,0,1))
vax.set_ylabel('Degrees / Second / Second')

box = gax.get_position()
gax.set_position([box.x0, box.y0, box.width, box.height-.05])
vax.set_position([box.x0, box.y0, box.width, box.height-.05])
fontP = FontProperties()
fontP.set_size('small')
lns = px+py+v
labs = [l.get_label() for l in lns]
plt.legend(lns, labs, loc='upper left', bbox_to_anchor=(.8, 1.15), borderaxespad=0,prop = fontP)

plt.show()

