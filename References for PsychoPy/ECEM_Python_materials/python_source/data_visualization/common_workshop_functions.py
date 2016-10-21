# Python Source File Available in python_source/data_visualization/common_workshop_functions.py

import numpy as np

def processSampleEventGaps(x,y,pupil,missing_points_marray,gap_fill_operation='clear'):
    """
    Performs the requested fill operation on areas of the x,y and pupil size arrays
    that are specified by the missing_points_marray masked array. 
    
    Supported fill operations are 'clear', and 'linear'.
    
    x, y, and pupil arrays must be of equal length, with each element of the 
    different arrays representing the sample value for the same time 
    during data collection.
    
    Parameters:
        x : numpy array like object
            Array shape must be Nx1, where N is the number of x position readings in the data list.
    
        y : numpy array like object
            Array shape must be Nx1, where N is the number of y position readings in the data list.
    
        pupil : numpy array like object
            Array shape must be Nx1, where N is the number of pupil size readings in the data list.
    
        missing_points_marray : numpy masked array
            A masked array of shape Nx1, where N == the length of the x,y,pupil array. Each element of the array indicates if the associated data array element should be considered as a missing value reading, or a valid data point.
    
        gap_fill_operation : either 'clear' or 'linear'
            Indicates how missing value periods within the x,y, and pupil data arrays should be filled. 'clear': Set missing data elements with numpy.NaN for x,y arrays and 0 for the pupil size array. 'linear': Set each missing data regions, Mi:Mj, within the x and y arrays to be linearly interpolated between the values of element i-1 and j of the array. pupil size array elements are set to 0.
    
    Returns:
        valid_data_periods : list of array slices
            Returns the list of array slices that specify the array regions in x,y, and pupil that should be considered valid data periods that have note been cleared or created using linear interpolation.    
    """
    valid_data_periods=np.ma.extras.notmasked_contiguous(
                                np.ma.array(pupil, mask=missing_points_marray)
                                )                                
    if gap_fill_operation == 'linear':
        # Linear fill in for data processing / filtering continuity
        #
        fill_in_data_arrays=[x,y]           
        for data_array in fill_in_data_arrays:        
            data_array[0:valid_data_periods[0].start]=data_array[valid_data_periods[0].start]
            last_slice_end=valid_data_periods[0].stop
            for data_slice in valid_data_periods[1:]:
                invalid_1=last_slice_end
                invalid_2=data_slice.start
                valcount=(invalid_2-invalid_1)
                # fill
                startval=data_array[invalid_1-1]
                endval=data_array[invalid_2]
                last_slice_end=data_slice.stop
                #display("{}:{}, {}:{}, {}, {}".format(invalid_1,invalid_2,startval,endval,valcount,(endval-startval)/valcount))
                if endval==startval:
                    data_array[invalid_1:invalid_2]=endval
                else:
                    data_array[invalid_1:invalid_2]=np.arange(startval,endval,(endval-startval)/valcount)[0:valcount]
        pupil[missing_points_marray]=0
    elif gap_fill_operation=='clear':
        fill_in_data_arrays=[x,y]           
        for data_array in fill_in_data_arrays:        
            data_array[missing_points_marray]=np.NaN
        pupil[missing_points_marray]=0        
    return valid_data_periods


class VisualAngleCalc(object):
    def __init__(self,display_size_mm,display_res_pix,eye_distance_mm=None):
        """
        Used to store calibrated area information and eye distance to screen data
        so that pixel data values can be converted to visual degree values.
        The pix2deg method is vectorized, meaning that is will perform the 
        pixel to angle calculations on all elements of the provided pixel
        position numpy arrays in one numpy call.
        
        The convertion process can use either a fixed eye to calibration 
        plane distance, or a numpy array of eye distances equal in length to the
        pixel_x, pixel_y (optional) pixel position data array. 
        
        Note: The information for display_size_mm,display_res_pix, and default
        eye_distance_mm could all be read automatically when openning a ioDataStore
        file. Tis automation should be implemented in a future release.
        """
        self._display_width=display_size_mm[0]
        self._display_height=display_size_mm[1]
        self._display_x_resolution=display_res_pix[0]
        self._display_y_resolution=display_res_pix[1]
        self._eye_distance_mm=eye_distance_mm
        
    def pix2deg(self,pixel_x,pixel_y=None,display_dim_x=None,display_dim_y=None,eye_distance_mm=None):
        """
        Stimulus positions (pixel_x,pixel_y) are defined in x and y pixel units, 
        with the origin (0,0) being at the **center** of the display, as to match
        the PsychoPy pix unit coord type.
    
        Stimulus dimentions (display_dim_x,display_dim_y) are defined in pixels,
        representing the width, height of the stim area, with stim_xy being the 
        origin. stim_dim_xy is optional.
    
        For example, a stim with a width,height of 100,100 pixels, 
        centered on display pixel localation 200,200 
        (where 0,0 is the display center), would have:
            pixel_x,pixel_y=150,150
            display_dim_xy=100,100
        """
        if self._eye_distance_mm is None and eye_distance_mm is None:
            raise ValueError("The eye_distance_mm arguement must not be None as no default eye distance was provided for VisualAngleCalc.")
        eye_dist_mm=self._eye_distance_mm
        if eye_distance_mm is not None:
            eye_dist_mm=eye_distance_mm
            
        sx,sy=pixel_x,pixel_y
        
        thetaH1=np.degrees(np.arctan(sx/(eye_dist_mm*self._display_x_resolution/self._display_width)))
        
        if sy is not None:
            thetaV1=np.degrees(np.arctan(sy/(eye_dist_mm*self._display_y_resolution/self._display_height)))

        if display_dim_x:
            sw,sh=display_dim_x,display_dim_y
            thetaH2=np.degrees(np.arctan(((sw+sx)/(eye_dist_mm*self._display_x_resolution/self._display_width))))
            horz_degree_dist=thetaH2-thetaH1
            if display_dim_y:
                thetaV2=np.degrees(np.arctan(((sh+sy)/(eye_dist_mm*self._display_y_resolution/self._display_height))))
                vert_degree_dist=thetaV2-thetaV1
        
        if sy is not None:
            if display_dim_y:
                return (thetaH1,thetaV1),(horz_degree_dist,vert_degree_dist)
            else:
                return thetaH1,thetaV1
        else:
            if display_dim_x:
                return thetaH1,horz_degree_dist
            else:
                return thetaH1