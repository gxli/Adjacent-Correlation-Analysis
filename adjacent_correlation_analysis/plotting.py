import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# from .analysis import compute_adjacent_correlation_vector

def adjacent_correlation_plot(xdata, ydata, bins=None, ax=None, scale=10, cmap='viridis', color_bad='lightblue', headaxislength=0, headlength=0, facecolor='w', plot_p_angle=True, plot_separate=False, xlabel='x', ylabel='y', return_r_value=False, **kwargs):
    """Generate the adjacent correlation plot

    Args:
        xdata: ndarray
        ydata: ndarray
        bins: bins used to compute the histogram. Defaults to None.
        ax: matplotlib axes object. Defaults to plt.gca().
        scale, cmap, color_bad, etc.: plotting parameters
        **kwargs: additional arguments for matplotlib.pyplot.imshow and quiver

    Returns:
        tuple: Ex, Ey (polarization components), xedges, yedges (bin edges), R (correlation metric)
    """
    if ax is None:
        ax = plt.gca()

    ll = xdata * ydata
    mask = np.isfinite(ll)
    values_x = xdata[mask].flatten()
    values_y = ydata[mask].flatten()
    
    if bins is None:
        hist_rho, xedges, yedges = np.histogram2d(values_x, values_y)
    else:
        hist_rho, xedges, yedges = np.histogram2d(values_x, values_y, bins=bins)
    
    p, nx, ny = compute_correlation_vector(xdata, ydata, xedges, yedges)
    Ey = ny * p 
    Ex = nx * p

    myextent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    
    cmap = mpl.colormaps.get(cmap)
    cmap.set_bad(color=color_bad)
    
    ax.imshow(np.log10(hist_rho).T, origin='lower', extent=myextent, interpolation='nearest', aspect='auto', cmap=cmap)
    
    xx = np.linspace(xedges[0], xedges[-1], len(xedges)-1)
    yy = np.linspace(yedges[0], yedges[-1], len(yedges)-1)
    dx = xedges[1] - xedges[0]
    dy = yedges[1] - yedges[0]
    x_grid, y_grid = np.meshgrid(xx, yy)
    
    ax.quiver(x_grid, y_grid, -Ex.T, -Ey.T, headaxislength=headaxislength, facecolor=facecolor, scale=scale, headlength=headlength, pivot='middle', angles='xy')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    p = np.sqrt(Ex**2 + Ey**2)
    R = np.nansum(p * hist_rho) / np.nansum(hist_rho)
    
    if plot_separate:
        plt.figure()
        plt.subplot(121)    
        frac = np.sqrt(Ex**2 + Ey**2)
        plt.imshow(frac.T, origin='lower', extent=myextent, aspect='auto', vmin=0, vmax=1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.colorbar()
        
        ax.set_title('R = ' + str(R))
            
        plt.subplot(122)    
        plt.imshow(np.arctan(Ey.T/Ex.T) / (np.pi/2), origin='lower', extent=myextent, aspect='auto', vmin=-1, vmax=1, cmap='twilight')
        plt.colorbar()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()
    
    return Ex, Ey, xedges, yedges, R
