import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from .analysis import compute_correlation_vector

def adjacent_correlation_plot(xdata, ydata, bins=None, ax=None, scale=10, cmap='Blues_r', color_bad='white', headaxislength=0, headlength=0, facecolor='r', plot_p_angle=True, xlabel='x', ylabel='y', return_r_value=False, lognorm=False, **kwargs):
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
    
    Ex, Ey = compute_correlation_vector(xdata, ydata, xedges, yedges)

    myextent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    cmap = mpl.colormaps.get(cmap)
    cmap.set_bad(color=color_bad)

    if lognorm:
        ax.imshow(np.log10(hist_rho).T, origin='lower', extent=myextent, interpolation='nearest', aspect='auto', cmap=cmap)
    else:
        ax.imshow(hist_rho.T, origin='lower', extent=myextent, interpolation='nearest', aspect='auto', cmap=cmap)
    xx = np.linspace(xedges[0], xedges[-1], len(xedges)-1)
    yy = np.linspace(yedges[0], yedges[-1], len(yedges)-1)
    x_grid, y_grid = np.meshgrid(xx, yy)
    
    ax.quiver(x_grid, y_grid, -Ex.T, -Ey.T, headaxislength=headaxislength, facecolor=facecolor, scale=scale, headlength=headlength, pivot='middle', angles='xy')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    p = np.sqrt(Ex**2 + Ey**2)
    R = np.nansum(p * hist_rho) / np.nansum(hist_rho)
    
    return Ex, Ey, xedges, yedges, R
