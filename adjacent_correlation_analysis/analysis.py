import numpy as np
from operator import itemgetter


def _compute_stokes(ex, ey, normed=False):
    """A subroutine to compute the Stokes parameters from spin-2 vector component

    Args:
        ex: x component of the spin-2 vector 
        ey: y component of the spin-2 vector 
        normed (bool, optional): normalize the vectors according to the intensity. Defaults to False.
    Returns:
        tuple: the Stokes i, q, u parameters
    """
    i = ex**2 + ey**2
    q = ex**2 - ey**2
    u = 2 * ex * ey
    if normed:
        return i, q/i, u/i
    return i, q, u



def _compute_correlation_coef(gx, gy):
    """compute the correlation coefficient between two measurements

    Args:
        gx (_type_): measurement 1
        gy (_type_): measurement 2
        xedges, yedges:  edges of the bins used by the histogram function.
        correlation (_type_): the correlation function to use

    Returns:
        the correlation value
    """
    # gx = np.array(np.gradient(xdata))
    # gy = np.array(np.gradient(ydata))
    
    # i, q, u = compute_stokes(gx,gy)
    
    # i_sum = i.sum(axis=0)
    # q_sum = q.sum(axis=0)
    # u_sum = u.sum(axis=0)
    
    # p, ex, ey = compute_angle(i_sum, q_sum, u_sum)
    gx2 = gx**2
    gy2 = gy**2
    gxgy = gx*gy
         
    gx2_value = np.sqrt(gx2.sum(axis=0))
    gy2_value = np.sqrt(gy2.sum(axis=0))
    gxgy_value = gxgy.sum(axis=0)
    
    return gxgy_value / (gx2_value * gy2_value)


def compute_correlation_matrix(gx, gy):
    """compute the correlation coefficient between two measurements

    Args:
        gx (_type_): measurement 1
        gy (_type_): measurement 2
        xedges, yedges:  edges of the bins used by the histogram function.
        correlation (_type_): the correlation function to use

    Returns:
        the correlation value
    """
    # gx = np.array(np.gradient(xdata))
    # gy = np.array(np.gradient(ydata))
    
    # i, q, u = compute_stokes(gx,gy)
    
    # i_sum = i.sum(axis=0)
    # q_sum = q.sum(axis=0)
    # u_sum = u.sum(axis=0)
    
    # p, ex, ey = compute_angle(i_sum, q_sum, u_sum)
    gx2 = gx**2
    gy2 = gy**2
    gxgy = gx*gy
         
    # gx2_value = np.sqrt(gx2.sum(axis=0))
    # gy2_value = np.sqrt(gy2.sum(axis=0))
    # gxgy_value = gxgy.sum(axis=0)
    
    return gx2, gxgy, gy2

def _compute_p_ex_ey(i, q, u):
    """Compute the polarization vector from the Stokes i, q, u parameters 

    Args:
        i: Stokes I parameter
        q: Stokes Q parameter
        u: Stokes U parameter

    Returns:
        tuple: p (polarization vector), Ex, Ey (x and y components of the polarization vector)
    """
    p = np.sqrt(q**2 + u**2) / i
    angle = 1/2 * np.arctan2(u, q)
    return p, np.cos(angle), np.sin(angle)

def _compute_weighted_hist(values_1, values_2, data, weight, xedges, yedges):
    """Compute weighted histogram for given values.
        values1: x
        values2: y
        
    """
    n, _, _ = np.histogram2d(values_1, values_2, weights=data*weight, bins=(xedges, yedges))
    d, _, _ = np.histogram2d(values_1, values_2, weights=data, bins=(xedges, yedges))
    return n/d


def compute_correlation_vector_p_nx_ny(xdata, ydata, xedges, yedges, weights=None, axes=None, time_like=False, projection_vector_parallel=None, projection_vector_perpendicular=None):
    """compute the adjacent correlation between two measurements

    Args:
        ld1 (_type_): measurement 1
        
        ld2 (_type_): measurement 2
        xedges, yedges:  edges of the bins used by the histogram function.
        weights (optional): weight factor
        time_like (optional): superimpose the correlations using the role of vector, default: false
        projection_vector: only consider the correlations projected 

    Returns:
        shape p, nx, ny, describing the degree of corelation (p) and the direction of the correlation (nx, ny)
    """
    
    if projection_vector_parallel is not None and projection_vector_perpendicular is not None:
        print("Both A and B are not None")

    mask = np.isfinite(xdata * ydata)
    values_x = xdata[mask].flatten()
    valuex_y = ydata[mask].flatten()
    gradient_x = np.gradient(xdata) #/ dx # gradient of data1 and data2
    gradient_y= np.gradient(ydata) #/ dy
        
    vec_dot= lambda x, y: np.array([i * j for i, j in zip(x, y)])
    
    if projection_vector_parallel is not None:
        gradient_x = vec_dot(gradient_x, projection_vector_parallel)
        gradient_y = vec_dot(gradient_y, projection_vector_parallel)
    
    if projection_vector_perpendicular is not None:
        gradient_x = gradient_x - vec_dot(gradient_x, projection_vector_perpendicular)
        gradient_y = gradient_y - vec_dot(gradient_y, projection_vector_perpendicular)
    
    if axes is None:
        pass
    else:
        gradient_x = itemgetter(*axes)(gradient_x)
        gradient_y = itemgetter(*axes)(gradient_y)
        
    if (xdata.ndim == 1): # spectra treatment when the input data is only 1d
        gradient_x = [gradient_x]
        gradient_y = [gradient_y]
    
    shape = xdata.shape
    # ndim = len(shape)
    # if ndim == 1: # ???
    #     gradient_x = [gradient_x]
    #     gradient_y = [gradient_y]


    
    gradient_x_1d = np.array([i[mask].flatten() for i in gradient_x])# remove nan values
    
    gradient_y_1d = np.array([i[mask].flatten() for i in gradient_y])
    
    
    
    data_x_3d = np.array([values_x for i in gradient_x])  # duplicate data_x to match the number of dimensions as in the gradients
    
    data_y_3d = np.array([valuex_y for i in gradient_y])
    
 #   norm = np.array(np.sqrt(gradient_x_1d**2 + gradient_y_1d **2))
    
    Ex = gradient_x_1d # /norm  # normalize the vectors, deriving C_i
    Ey = gradient_y_1d  # /norm 
    stokes_i, stokes_q, stokes_u = _compute_stokes(Ex , Ey)
    
    
    values_x_all = np.array(data_x_3d).flatten()
    valuex_y_all =np.array(data_y_3d).flatten() 
    
   
    values_i_all =np.array(stokes_i).flatten() 
    values_q_all =np.array(stokes_q).flatten()
    values_u_all = np.array(stokes_u).flatten()
    
    # identify the locations of the valid data
    mask_list = [values_x_all, valuex_y_all, values_i_all, values_q_all,values_i_all]
    bool_list = [np.isfinite(i) for i in mask_list]
    mask_valid = np.logical_and.reduce(bool_list) # mask out invalid values
    
    # hist_rho_all, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],bins=(xedges, yedges)) # probability density of the data
    if time_like is False:
        if weights is None:

            hist_w_i_all, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights=values_i_all[mask_valid],bins=(xedges, yedges)) # weighted histogram of i    
            hist_w_q_all, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights=values_q_all[mask_valid],bins=(xedges, yedges)) # weighted histogram of q
            hist_w_u_all, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights=values_u_all[mask_valid],bins=(xedges, yedges)) # weighted histogram of u 
        else:
            hist_w_i_all = _compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid],values_i_all[mask_valid], weights)
            hist_w_q_all = _compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid],values_q_all[mask_valid], weights)
            hist_w_u_all = _compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid],values_u_all[mask_valid], weights) 
        p, nx_result, ny_result = _compute_p_ex_ey(hist_w_i_all, hist_w_q_all, hist_w_u_all) # compute the polarization degree, Ex, Ey from 
        
        stokes_i = hist_w_i_all
        return p, nx_result, ny_result

    else:
        if weights is None:

            hist_ex, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights=Ex[mask_valid],bins=(xedges, yedges)) 
            hist_ey, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights=Ey[mask_valid],bins=(xedges, yedges)) 

            hist_ex_abs, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights= abs(Ex[mask_valid]),bins=(xedges, yedges)) 
            hist_ey_abs, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights= abs(Ey[mask_valid]),bins=(xedges, yedges)) 
        else:
            hist_ex = _compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid], Ex[mask_valid], weights)
            hist_ey = _compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid], Ey[mask_valid], weights)
            hist_ex_abs = _compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid], abs(Ex[mask_valid]), weights)
            hist_ey_abs = _compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid], abs(Ey[mask_valid]), weights)
            # hist_w_u_all = compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid],values_u_all[mask_valid], weights) 

        mod_vec = np.sqrt(hist_ex**2 + hist_ey**2) # compute the polarization degree, Ex, Ey from
        mod_vec_abs = np.sqrt(hist_ex_abs**2 + hist_ey_abs**2) # compute the polarization degree, Ex, Ey from
        p = mod_vec / mod_vec_abs
        nx_result = hist_ex / mod_vec
        ny_result = hist_ey / mod_vec
        return p, nx_result, ny_result
    



def compute_correlation_vector(xdata, ydata, xedges, yedges, weights=None, axes=None, time_like=False, projection_vector_parallel=None, projection_vector_perpendicular=None):
    p, nx, ny = compute_correlation_vector_p_nx_ny(xdata, ydata, xedges, yedges, weights, axes, time_like, projection_vector_parallel, projection_vector_perpendicular)
    ex = nx * p
    ey = ny * p
    return ex, ey
    
def compute_correlation_map(xdata, ydata):
    """compute the correlation value between two measurements

    Args:
        xdata (_type_): measurement 1
        ydata (_type_): measurement 2
        xedges, yedges:  edges of the bins used by the histogram function.
        correlation (_type_): the correlation function to use

    Returns:
        the correlation strength i, 
        the correlation degree p, 
        the correlation angle arctan2(ey, ex
        ), 
        the correlation coefficient
    """
    
    
    gx = np.array(np.gradient(xdata))
    gy = np.array(np.gradient(ydata))
    
    i, q, u = _compute_stokes(gx,gy)
    
    i_sum = i.sum(axis=0)
    q_sum = q.sum(axis=0)
    u_sum = u.sum(axis=0)
    
    corr_coef = _compute_correlation_coef(gx, gy)
    
    p, ex, ey = _compute_p_ex_ey(i_sum, q_sum, u_sum)
    
    # stdx = np.nanstd(gx.flatten())
    # stdy = np.nanstd(gy.flatten())
    


    return p, np.arctan2(ey,ex), corr_coef, i

