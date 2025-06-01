import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from .analysis import compute_correlation_vector

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def adjacent_correlation_plot(xdata, ydata, bins=None, ax=None, scale=10, cmap='Blues_r', 
                            color_bad='white', headaxislength=0, headlength=0, 
                            facecolor='r', xlabel='x', ylabel='y', lognorm=False, 
                            colorbar=True, **kwargs):
    """Generate a 2D histogram with a vector field showing local correlations.

    Args:
        xdata (ndarray): Input data for x-axis.
        ydata (ndarray): Input data for y-axis, same shape as xdata.
        bins (int, tuple, or None): Number of bins for histogram (int for equal bins, 
                                   tuple for (xbins, ybins), or None for auto).
        ax (matplotlib.axes.Axes, optional): Axes to plot on. Defaults to plt.gca().
        scale (float): Scaling factor for quiver arrows.
        cmap (str): Colormap for histogram (e.g., 'Blues_r', 'viridis').
        color_bad (str): Color for invalid data in histogram.
        headaxislength (float): Length of quiver arrow head axis.
        headlength (float): Length of quiver arrow head.
        facecolor (str): Color of quiver arrows.
        xlabel (str): Label for x-axis.
        ylabel (str): Label for y-axis.
        lognorm (bool): If True, apply logarithmic scaling to histogram.
        colorbar (bool): If True, add a colorbar to the plot.
        **kwargs: Additional arguments for matplotlib.pyplot.imshow and quiver.

    Returns:
        tuple: (Ex, Ey, xedges, yedges, R)
            - Ex, Ey: Correlation vector components (from compute_correlation_vector).
            - xedges, yedges: Bin edges for x and y axes.
            - R: Correlation metric (weighted sum of vector magnitudes).

    Raises:
        ValueError: If xdata and ydata have mismatched shapes or are not 1D/2D arrays.
        ImportError: If compute_correlation_vector is not available.
    """
    # Input validation
    if not isinstance(xdata, np.ndarray) or not isinstance(ydata, np.ndarray):
        raise ValueError("xdata and ydata must be NumPy arrays")
    if xdata.shape != ydata.shape:
        raise ValueError("xdata and ydata must have the same shape")
    if xdata.size == 0 or ydata.size == 0:
        raise ValueError("xdata and ydata must not be empty")

    # Use current axes if none provided
    if ax is None:
        ax = plt.gca()

    # Mask invalid data
    ll = xdata * ydata
    mask = np.isfinite(ll)
    values_x = xdata[mask].flatten()
    values_y = ydata[mask].flatten()

    if len(values_x) == 0 or len(values_y) == 0:
        raise ValueError("No valid data after masking NaN/Inf values")

    # Compute 2D histogram
    try:
        hist_rho, xedges, yedges = np.histogram2d(values_x, values_y, bins=bins)
    except ValueError as e:
        raise ValueError(f"Histogram computation failed: {str(e)}")

    # Compute correlation vectors (assumes compute_correlation_vector is defined)
    try:
        from .analysis import compute_correlation_vector
        Ex, Ey = compute_correlation_vector(xdata, ydata, xedges, yedges)
    except ImportError:
        raise ImportError("compute_correlation_vector not found in .analysis module")
    except Exception as e:
        raise ValueError(f"Error in compute_correlation_vector: {str(e)}")

    # Set plot extent
    myextent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Configure colormap
    cmap = mpl.colormaps.get_cmap(cmap)
    cmap.set_bad(color=color_bad)

    # Plot histogram
    if lognorm:
        # Ensure positive values for log scaling
        hist_rho_safe = np.where(hist_rho > 0, hist_rho, 1e-10)
        im = ax.imshow(np.log10(hist_rho_safe).T, origin='lower', extent=myextent, 
                      interpolation='nearest', aspect='auto', cmap=cmap, **kwargs)
    else:
        im = ax.imshow(hist_rho.T, origin='lower', extent=myextent, 
                      interpolation='nearest', aspect='auto', cmap=cmap, **kwargs)

    # Add colorbar
    if colorbar:
        plt.colorbar(im, ax=ax, label='Log(Count)' if lognorm else 'Count')

    # Create grid for quiver plot
    xx = np.linspace(xedges[0], xedges[-1], len(xedges)-1)
    yy = np.linspace(yedges[0], yedges[-1], len(yedges)-1)
    x_grid, y_grid = np.meshgrid(xx, yy)

    # Plot quiver arrows
    ax.quiver(x_grid, y_grid, -Ex.T, -Ey.T, headaxislength=headaxislength, 
              headlength=headlength, facecolor=facecolor, scale=scale, 
              pivot='middle', angles='xy', **kwargs)

    # Set labels
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Compute correlation metric
    p = np.sqrt(Ex**2 + Ey**2)
    R = np.nansum(p * hist_rho) / np.nansum(hist_rho) if np.nansum(hist_rho) > 0 else np.nan

    return Ex, Ey, xedges, yedges, R