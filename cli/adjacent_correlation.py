#!/usr/bin/env python
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib as mpl
import pickle

def compute_stokes(ex, ey, normed=False):
    """A subroutine to compute the Stokes parameters from spin-2 vector component

    Args:
        ex (_type_): x component of the spin-2 vector 
        ey (_type_): y component of the spin-2 vector 
        normed (bool, optional): normalize the vectors according to the intensity. Defaults to True.
    Returns:
        the stokes i, q, u parameter
    """
    i = ex**2 + ey **2
    q = ex**2 - ey**2
    u = 2 * ex * ey
    if normed:
        return i/i,q/i, u/i
    else:
        return i, q, u
    
def compute_angle(i,q,u):
    """compute the polarization vector from the stokes i, q, u parameter 

    Args:
        i (_type_): _description_
        q (_type_): _description_
        u (_type_): _description_

    Returns:
        p, the polarization vector, and Ex, Ey, the x and y component of the polarization vector
    """
    p = np.sqrt(q**2 + u**2) / i
    angle = 1/2 * np.arctan2(u,q)
    return p, np.cos(angle), np.sin(angle)

def compute_weighted_hist(values_1, values_2, data, weight, xedges, yedges):
    n,_,_ = np.histogram2d(values_1,values_2,weights=data*weight,bins=(xedges, yedges)) # weighted histogram of i    
    d,_,_ = np.histogram2d(values_1,values_2,weights=data,bins=(xedges, yedges)) # 
    
    return n/d


def compute_adjacent_correlation_vector(xdata, ydata, xedges, yedges, weights=None):
    """compute the adjacent correlation between two measurements

    Args:
        ld1 (_type_): measurement 1
        ld2 (_type_): measurement 2
        xedges, yedges:  edges of the bins used by the histogram function.

    Returns:
        shape p, nx, ny, describing the degree of corelation (p) and the direction of the correlation (nx, ny)
    """
    xx = np.linspace(xedges[0],xedges[-1],len(xedges)-1)
    yy = np.linspace(yedges[0],yedges[-1],len(yedges)-1)
    dx = xedges[1]-xedges[0]
    dy = yedges[1]-yedges[0]
    
    mask = np.isfinite(xdata * ydata)
    values_x = xdata[mask].flatten()
    valuex_y = ydata[mask].flatten()
    
    
    gradient_x = np.gradient(xdata) #/ dx # gradient of data1 and data2
    gradient_y= np.gradient(ydata) #/ dy
	
 

    if (xdata.ndim == 1): # spectra treatment when the input data is only 1d
        gradient_x = [gradient_x]
        gradient_y = [gradient_y]
        
    
    ampli1 = np.sqrt(np.array([i**2 for i in gradient_x]).sum(axis=0)) # magnitude of the spatial gradients  
    ampli2 = np.sqrt(np.array([i**2 for i in gradient_y]).sum(axis=0))
   
        
    # pngg1 = gg1.copy() 
    # pngg2 = gg2.copy()
    

    
    gradient_x_1d = np.array([i[mask].flatten() for i in gradient_x])
    
    gradient_y_1d = np.array([i[mask].flatten() for i in gradient_y])
    
    
    
    data_x_3d = np.array([values_x for i in gradient_x])  # duplicate data_x to match the number of dimensions as in the gradients
    
    data_y_3d = np.array([valuex_y for i in gradient_y])
    
    norm = np.array(np.sqrt(gradient_x_1d**2 + gradient_y_1d **2))
    
    Ex = gradient_x_1d/norm  # normalize the vectors, deriving C_i
    Ey = gradient_y_1d/norm 
    stokes_i, stokes_q, stokes_u = compute_stokes(Ex , Ey)
    
    
    values_x_all = np.array(data_x_3d).flatten()
    valuex_y_all =np.array(data_y_3d).flatten() 
    
   
    values_i_all =np.array(stokes_i).flatten() 
    values_q_all =np.array(stokes_q).flatten()
    values_u_all = np.array(stokes_u).flatten()
    
    mask_list = [values_x_all, valuex_y_all, values_i_all, values_q_all,values_i_all]
    bool_list = [np.isfinite(i) for i in mask_list]
    mask_valid = np.logical_and.reduce(bool_list) # mask out invalid values
    
    # hist_rho_all, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],bins=(xedges, yedges)) # probability density of the data
    if weights is None:

        hist_w_i_all, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights=values_i_all[mask_valid],bins=(xedges, yedges)) # weighted histogram of i    
        hist_w_q_all, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights=values_q_all[mask_valid],bins=(xedges, yedges)) # weighted histogram of q
        hist_w_u_all, _, _ = np.histogram2d(values_x_all[mask_valid],valuex_y_all[mask_valid],weights=values_u_all[mask_valid],bins=(xedges, yedges)) # weighted histogram of u 
    else:
        hist_w_i_all = compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid],values_i_all[mask_valid], weights)
        hist_w_q_all = compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid],values_q_all[mask_valid], weights)
        hist_w_u_all = compute_weighted_hist(values_x_all[mask_valid],valuex_y_all[mask_valid],values_u_all[mask_valid], weights) 
         
    
    p, Ex_result, Ey_result = compute_angle(hist_w_i_all, hist_w_q_all, hist_w_u_all) # compute the polarization degree, Ex, Ey from 
    
    return p, Ex_result, Ey_result




def get_valid_args(func, args_dict):
    '''Return dictionary without invalid function arguments.'''
    validArgs = func.func_code.co_varnames[:func.func_code.co_argcount]
    return dict((key, value) for key, value in args_dict.iteritems() 
                if key in validArgs)
    
    
def adjacent_correlation_plot(xdata, ydata, bins=None, ax = plt.gca(),scale=10, cmap='viridis',color_bad='lightblue',headaxislength=0, headlength=0,facecolor='w', plot_p_angle=True, plot_separate=False,xlabel='x', ylabel='y',return_r_value=False,**kwargs):
    """function to generate the adjacent correlation plot

    Args:
        xdata (_type_): ndarray
        ydata (_type_): ndarray
        bins (_type_, optional): bins used to compute the histogram. Defaults to None. The convention is the same as np.histogram2d.
        ** args: additional arguments to be passed to the plot function, see matplotlib.pyplot.imshow and matplotlib.pyplot.quiver for more details
    Returns:
        hist_rho, Ex, Ey, xedges, yedges (_type_): the histogram of the data, the x and y component of the polarization vector, the edges of the bins used to compute the histogram        
    """

    ll = xdata * ydata
    mask = np.isfinite(ll)
    values_x = xdata[mask].flatten()
    values_y = ydata[mask].flatten()
    
    
    
    if bins is None:
        hist_rho, xedges, yedges = np.histogram2d(values_x, values_y)    
    else:
        hist_rho, xedges, yedges = np.histogram2d(values_x, values_y,bins=bins)    
    p, nx, ny = compute_adjacent_correlation_vector(xdata, ydata, xedges, yedges)
    Ey =  ny * p 
    Ex =  nx * p

    myextent  =[xedges[0],xedges[-1],yedges[0],yedges[-1]]
    
    cmap = mpl.colormaps.get(cmap)  # viridis is the default colormap for imshow
    cmap.set_bad(color=color_bad)

        
        
    # cmap = mpl.colormaps.get('viridis')  # viridis is the default colormap for imshow
    # cmap.set_bad(color='skyblue')
    
    ax.imshow(np.log10(hist_rho).T,origin='lower',extent=myextent,interpolation='nearest',aspect='auto',cmap=cmap)
    
    xx = np.linspace(xedges[0],xedges[-1],len(xedges)-1)
    yy = np.linspace(yedges[0],yedges[-1],len(yedges)-1)
    dx = xedges[1]-xedges[0]
    dy = yedges[1]-yedges[0]
    x_grid, y_grid = np.meshgrid(xx, yy)

    
    # args = get_valid_args(plt.quiver, kwargs)
    
    # plt.quiver(x_grid, y_grid, Ex.T, Ey.T, **args)
    ax.quiver(x_grid, y_grid, -Ex.T, -Ey.T, headaxislength=headaxislength, facecolor=facecolor, scale=scale, headlength=headlength, pivot='middle',angles='xy')
    # ax.quiver(x_grid, y_grid, Ex.T, Ey.T, headaxislength=headaxislength, facecolor=facecolor,scale=scale, headlength=headlength)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    p = np.sqrt(Ex**2 + Ey**2)
    
    R = np.nansum(p * hist_rho) / np.nansum(hist_rho)
    
    if plot_separate:

        plt.figure()
        plt.subplot(121)    
        frac = np.sqrt(Ex**2 + Ey**2)
        plt.imshow(frac.T, origin='lower',extent=myextent,aspect='auto',vmin=0, vmax=1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.colorbar()

    
        ax.set_title('R = ' + str(R))
            
        plt.subplot(122)    
        plt.imshow( np.arctan(Ey.T/Ex.T) /(np.pi/2), origin='lower',extent=myextent,aspect='auto',vmin=-1, vmax=1,cmap='twilight')
        plt.colorbar()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
        
    
    return Ex, Ey, xedges, yedges, R


def compute_outlier_thresholds(data, method='percentile', **kwargs):
  """
  Computes the lower and upper thresholds for outlier removal based on the
  specified method.

  Args:
    data (numpy.ndarray): The input data array.
    method (str, optional): The method to use for threshold computation.
                           Options are 'std_dev', 'iqr', 'percentile', 'zscore'.
                           Defaults to 'iqr'.
    **kwargs: Additional keyword arguments to pass to the thresholding function.
              - For 'std_dev': 'num_std' (float, default=3).
              - For 'iqr': 'k' (float, default=1.5).
              - For 'percentile': 'lower_percentile' (float, default=5),
                                  'upper_percentile' (float, default=95).
              - For 'zscore': 'threshold' (float, default=3).

  Returns:
    tuple: A tuple containing (lower_threshold, upper_threshold).
           Returns (np.nan, np.nan) if the method is invalid.
  """
  data = data[np.isfinite(data)]
  if method == 'std_dev':
    num_std = kwargs.get('num_std', 3)
    mean = np.mean(data)
    std = np.std(data)
    lower_threshold = mean - num_std * std
    upper_threshold = mean + num_std * std
    return lower_threshold, upper_threshold
  elif method == 'iqr':
    k = kwargs.get('k', 1.5)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_threshold = q1 - k * iqr
    upper_threshold = q3 + k * iqr
    return lower_threshold, upper_threshold
  elif method == 'percentile':
    lower_percentile = kwargs.get('lower_percentile', 0.001)
    upper_percentile = kwargs.get('upper_percentile', 99.999)
    lower_threshold = np.percentile(data, lower_percentile)
    upper_threshold = np.percentile(data, upper_percentile)
    return lower_threshold, upper_threshold
  elif method == 'zscore':
    from scipy import stats
    threshold = kwargs.get('threshold', 3)
    z_scores = np.abs(stats.zscore(data))
    outlier_mask = z_scores > threshold
    valid_data = data[~outlier_mask]
    if valid_data.size > 0:
      lower_threshold = np.min(valid_data)
      upper_threshold = np.max(valid_data)
    else:
      return -np.inf, np.inf # Return extreme values if no valid data remains
    return lower_threshold, upper_threshold
  else:
    print(f"Invalid method: '{method}'. Please choose from 'std_dev', 'iqr', 'percentile', 'zscore'.")
    return np.nan, np.nan

def apply_percentile_filter(data, low_percentile, high_percentile):
  """
  Calculates vmin and vmax based on percentile filtering of the input data,
  handling potential NaN values.

  Args:
    data (numpy.ndarray): The input data array.
    low_percentile (float): The lower percentile to use for vmin (e.g., 2.0).
    high_percentile (float): The upper percentile to use for vmax (e.g., 98.0).

  Returns:
    tuple: A tuple containing (vmin, vmax).
  """
  valid_data = data[np.isfinite(data)]  # Filter out NaN values
  if valid_data.size == 0:
    return np.nan, np.nan  # Return NaN if all data is NaN
  vmin = np.percentile(valid_data, low_percentile)
  vmax = np.percentile(valid_data, high_percentile)
  return vmin, vmax

if __name__ == "__main__":
    f1 = sys.argv[1]
    f2 = sys.argv[2]
    
    h1 = fits.open(f1)
    h2 = fits.open(f2)
    
    d1 = h1[0].data
    d2 = h2[0].data
    
    if d1 is None:
        d1 = h1[1].data
        d2 = h2[1].data
    try:
        print(sys.argv[3])
        if float(sys.argv[3]) > 0:
            Logdata1=True
        else:
            Logdata1=False        
    except:
        Logdata1 = False
        
    if Logdata1:    
        ld1 = np.log10(d1)
        # ld1[np.isnan(ld1)]=1
        # ld1[np.isinf(ld1)]=1
        # ld2[np.isnan(ld2)]=1
        # ld2[np.isinf(ld2)]=1
    else:
        ld1 = d1
     
        
    try:
        print(sys.argv[4])
        if float(sys.argv[4]) > 0:
            Logdata2=True
        else:
            Logdata2=False        
    except:
        Logdata2 = False
        
    if Logdata2:    
        ld2 = np.log10(d2)
        # ld1[np.isnan(ld1)]=1
        # ld1[np.isinf(ld1)]=1
        # ld2[np.isnan(ld2)]=1
        # ld2[np.isinf(ld2)]=1
    else:
        ld2 = d2
            



    if Logdata1:
        xlabel = 'Log(' + f1 + ')'
    else:
        xlabel = f1
        
    if Logdata2:
        ylabel = 'Log(' + f2 + ')'
    else:
        ylabel = f2
        
    vmin1, vmax1 = compute_outlier_thresholds(ld1.flatten())
    vmin2, vmax2 = compute_outlier_thresholds(ld2.flatten())
    delta_1 = vmax1 - vmin1
    fd = 0.3
    vmin1 = vmin1 - delta_1 * fd
    vmax1 = vmax1 + delta_1 * fd
    delta_2 = vmax2 - vmin2
    vmin2 = vmin2 - delta_2 * fd
    vmax2 = vmax2 + delta_2 * fd
    nbins = 100
    bins1 = np.linspace(vmin1, vmax1, nbins)
    bins2 = np.linspace(vmin2, vmax2, nbins)

    Ex, Ey, x_grid, y_grid, R = adjacent_correlation_plot(ld1, ld2, bins=[bins1, bins2], scale=20,xlabel=xlabel,ylabel=ylabel, plot_separate=True)
    # Ex, Ey, x_grid, y_grid, R = adjacent_correlation_plot(ld1, ld2, bins=nbins, scale=20,xlabel=xlabel,ylabel=ylabel, plot_separate=True)
    
    p = np.sqrt(Ex**2 + Ey**2)
    
    # R = (p * hist_rho).sum() / hist_rho.sum()
    
    # plt.title('R = ' + str(R))
    
    result= {"xedges":x_grid, "yedges":y_grid, "Ex":Ex, "Ey":Ey}
    
    # np.save("result.npy", result)    
    # pickle.dump(result, open("dump.p", "wb"))  # 
    if Logdata1:
        plt.xlabel('Log' + f1)
    else:
        plt.xlabel(f2)
        
    if Logdata2:
        plt.ylabel('Log' + f2)  
    else:
        plt.ylabel(f2)
    # if plot_p_angle:
    #     plt.figure()
    #     plt.subplot(121)    
    #     frac = np.sqrt(Ex**2 + Ey**2)
    #     plt.imshow(frac.T, origin='lower',extent=myextent,aspect='auto',vmin=0, vmax=1)
    #     plt.colorbar()
        
            
    #     plt.subplot(122)    
    #     plt.imshow( np.arctan(Ey.T/Ex.T) /(np.pi/2), origin='lower',extent=myextent,aspect='auto',vmin=-1, vmax=1,cmap='twilight')
    #     plt.colorbar()
    #     plt.show()
        
    
    plt.show()

    # test()