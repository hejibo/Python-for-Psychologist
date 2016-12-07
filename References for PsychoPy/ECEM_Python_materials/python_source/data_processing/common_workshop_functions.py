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

def calculateVelocity(time,degrees_x,degrees_y=None):
    """
    Calculate the instantaneous velocity (degrees / second) for data points in 
    degrees_x and (optionally) degrees_y, using the time numpy array for 
    time delta information.

    Numpy arrays time, degrees_x, and degrees_y must all be 1D arrays of the same
    length.
    
    If both degrees_x and degrees_y are provided, then the euclidian distance
    between each set of points is calculated and used in the velocity calculation.

    time must be in seconds.msec units, while degrees_x and degrees_y are expected
    to be in visual degrees. If the position traces are in pixel coordinate space,
    use the VisualAngleCalc class to convert the data into degrees.
    """
    if degrees_y is None:
        data=degrees_x
    else:
        data=np.sqrt(degrees_x*degrees_x+degrees_y*degrees_y)
    
    velocity_between = (data[1:]-data[:-1])/(time[1:]-time[:-1])
    velocity = (velocity_between[1:]+velocity_between[:-1])/2.0
    return velocity

def calculateAccelleration(time,data_x,data_y=None):
    """
    Calculate the accelleration (degrees / second / second) for data points in 
    degrees_x and (optionally) degrees_y, using the time numpy array for 
    time delta information.
    """
    velocity=calculateVelocity(time,data_x,data_y)
    accel = calculateVelocity(time[1:-1],velocity)
    return accel

# savitzky_golay implementation from http://wiki.scipy.org/Cookbook/SavitzkyGolay
# implemented by Thomas Haslwanter
#  
def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')
