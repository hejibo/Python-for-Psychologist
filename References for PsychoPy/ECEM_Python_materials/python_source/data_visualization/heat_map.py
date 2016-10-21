# This Python Source File Available in python_source/data_visualization/heat_map.py

import matplotlib.pyplot as plt
import matplotlib.pylab as plb
import matplotlib.image as mpimg
import matplotlib.cm as cm

from scipy.stats import scoreatpercentile
import numpy as np

plt.close()

##### STEP A. #####
# Define the value for settings when creating the heat map.
#
# We will use a sigma 33 pixels for the gaussian distribution applied to
# the fixation density map for each fixation position, which
# = ~ 2 visual degrees on a 1024x768 monitor when viewed at 60 cm.
#
sigma_x = sigma_y = 33.0
# If fixation duration is used to weight each fixation when added to the 
# fixation density array, these two variables specify the min and max fixation 
# duration that will be applied.
#
min_fix_duration=0
max_fix_duration=500
# use_dwell_time_weighting:
# True : Each fixations impact on the fixation map is linearly proprotional 
#        to the fixation dwell time within the fixation duration range 
#        min_fix_duration to max_fix_duration
# False: Fixations are still filtered by min_fix_duration, max_fix_duration; 
#        however each fixation provides equal weight to the fixtion map, 
#        regardless of duration.
#
use_dwell_time_weighting=True
# Percentile range of fixation map distribution to include in heat map 
# calculation.
#
fix_perc_range=[.05,.95]
# Percentile floor of fixation map distribution for heat map visualization
#
min_fix_dist_perc=10
# We will be creating simulated fixation data, this specifies the number of 
# fixation points to create.
#
sim_fix_count=500
 
##### STEP B. #####
# Create 2D Gaussian Mask template as a 2D numpy array
#
# Create x and y pixel ranges for Gauss Mask.
#
x = np.arange(-sigma_x*2.5,sigma_x*2.5, 1)
y = np.arange(-sigma_y*2.5, sigma_y*2.5, 1)
# Create X and Y pixel position values for each element of Gauss. Mask.
#
X, Y = np.meshgrid(x, y)
# Create 2D Gauss Mask as numpy array using X and Y mesh grid data
# and sigma's, with Gauss centered in 2D array (0,0)
#
gauss=plb.bivariate_normal(X, Y, sigma_x, sigma_y, 0,0)
# Normalize the Gausian, such that the max value in the is 1.0.
#
gauss*=1.0/gauss.flatten().max()
ghw,ghh=gauss.shape[0]//2,gauss.shape[1]//2

##### STEP C. #####
# Load Background Image Displayed During Eye Data Collection 
# Flip vertically
#
image_array=np.flipud(mpimg.imread("./images/canal.jpg"))    
# Get background image size
#
image_size=image_array.shape#(image_array.shape[0],image_array.shape[1])
ihw,ihh=image_size[0]/2,image_size[1]/2

##### STEP D. #####
# Create some Random Fixation Data
#
# Here, the fixation event data is being simulated as sim_fix_count fixations
# of random position within center 50% of fixation density map (since it
# is created with 2*width, 2*height of the image that the fixation density map
# will be applied to).Random fixation durations between 150 and 1500 msec 
# are used.
#
border=10
fix_duration_range=min_fix_duration,max_fix_duration
fixation_x_range=-ihw+border, ihw-border
fixation_y_range=-ihh+border, ihh-border

# Create the dummy Fixation Data as a 3x500 numpy array
#
fix_pos=np.column_stack( (np.random.randint(*fixation_y_range, size=sim_fix_count),
                          np.random.randint(*fixation_x_range, size=sim_fix_count),
                          np.random.randint(*fix_duration_range, size=sim_fix_count)))

##### STEP E. #####
# Create the Fixation Density Map Layer based on 
# the Gauss Mask Template and the Fixation Data
# Start with empty 2D numpy array 2x size of background image to be used 
# (this makes applying Gauss mask for each fixation easier as array clipping
# is not a consern.). The density map will be trimmed back to the center
# 50% later.
#
fixation_map=np.zeros((image_size[0]*2,image_size[1]*2))

# Apply Gaussian Mask for each fixation position to the density array
# based on the created fixation event data.
#

if use_dwell_time_weighting:
    for fx,fy,fix_dur in fix_pos:
        fx+=ihh*2
        fy+=ihw*2
        fixation_map[fy-ghh:fy+ghh+1,fx-ghw:fx+ghw+1]+=(gauss*fix_dur)
else:
    for fx,fy,fix_dur in fix_pos:
        fx+=ihh*2
        fy+=ihw*2
        fixation_map[fy-ghh:fy+ghh+1,fx-ghw:fx+ghw+1]+=gauss

fixation_map=fixation_map[ihw:image_size[0]+ihw,ihh:image_size[1]+ihh]
# Apply fixation duration and distribution pertentile heuristics to heat map:
#
fixation_map_min=fixation_map.min()
fixation_map_max=fixation_map.max()
fix_range=fixation_map_max-fixation_map_min
fix_range=fixation_map_min+fix_perc_range[0]*fix_range,fixation_map_min+fix_perc_range[1]*fix_range
min_fix_map_value=scoreatpercentile(fixation_map, min_fix_dist_perc, limit=fix_range)
fix_floor_value=scoreatpercentile(fixation_map, fix_perc_range[0]*100.0)
fix_ceil_value=scoreatpercentile(fixation_map, fix_perc_range[1]*100.0)

fixation_map[fixation_map<fix_floor_value]=fix_floor_value
fixation_map[fixation_map>fix_ceil_value]=fix_ceil_value
fixation_map[fixation_map<min_fix_map_value]=min_fix_map_value


##### STEP F. #####
# Plot the Fixation Gaussian, the Simulated Fixation Points,
# the resulting Fixation Density Map, and the background image
# to be used for illustrative purposes.
#

#Create a 12x8 inch figure
#
fig = plt.figure(figsize=(14,10))
fig.suptitle("Components in Creating a Fixation Density Based Heat Map",fontsize=14)
# Figure will have 2 x 2 subplots
#
gauss_axis = fig.add_subplot(2,2,1)
#left_axis.set_ylabel('Position (pixels)')
plt.imshow(gauss,cmap=cm.gray,origin='lower',extent=(-ghh, ghh,-ghw, ghw))
gauss_axis.set_title("Gaussian Mask Used for Each Fixation", fontsize=12)
gauss_axis.set_ylabel('Pixels')

# Display the background image.
#
image_axis = fig.add_subplot(2,2,2)
plt.imshow(image_array,origin='lower',extent=(-ihh, ihh,-ihw, ihw))
image_axis.set_title("Background Image", fontsize=12)


# Plot the simulated fixation data.
#
fix_point_axis = fig.add_subplot(2,2,3)
plt.scatter(fix_pos[:,0],fix_pos[:,1],s=fix_pos[:,2]/10)
fix_point_axis.set_title("Simulated Fixation Point Data.\nPoint Size Proportional to Fixation Duration", fontsize=12)
fix_point_axis.set_ylabel('Pixels')
fix_point_axis.set_xlabel('Pixels')
plt.xlim((-ihh, ihh))
plt.ylim((-ihw, ihw))
# Plot fixation density mask using a Yellow->Orange->Red Color Map,
# clipped to center 50% of 
#.
heat_map_axis = fig.add_subplot(2,2,4)
clmap=plt.get_cmap('YlOrRd')
im = plt.imshow(fixation_map, interpolation='nearest', 
                                origin='lower',
                                extent=(-ihh, ihh,-ihw, ihw),
                                cmap=clmap)           
heat_map_axis.set_title("Heat Map for the Fixation Density Map.", fontsize=12)
heat_map_axis.set_xlabel('Pixels')


plt.tight_layout() 
plt.subplots_adjust(left = 0.1, bottom=0.1, top=0.9,hspace=0.2, wspace=.2)

plt.show()
  
###### STEP G. #####
## Putting it all Together: Heat Map Representation of Fixation Position 
## and Dwell Time Density During Image Viewing
##
fig = plt.figure(figsize=(14,10))
fig.suptitle("Fixation Density Heat Map",fontsize=14)

## Draw the background Image
#
image_array=np.flipud(mpimg.imread("./images/canal.jpg"))    
plt.imshow(image_array,origin='lower',extent=(-ihh, ihh,-ihw, ihw))
# Create RGBA values for the color map created above.
# Set the Color Map Transparency to Increase as a Function of Fixation Dwell Time.  
#
clmap._init()
alphas = np.linspace(.3, 0.9, clmap.N+3)
clmap._lut[:,-1] = alphas
# Draw the Fixation Map Mask over the Background Image using the Color Map:
#
plt.imshow(fixation_map, origin='lower',extent=(-ihh, ihh,-ihw, ihw),cmap=clmap)
# Display the Heat Map Scale:
#
cb=plt.colorbar()
if use_dwell_time_weighting:
    cb.set_label("Fixation Density (msec scale)") 
else:
    cb.set_label("Fixation Density (count scale)") 
    
plt.show()