

.. _installation-usage:

Installation & Usage
-----------------------

-------------
Requirements:
-------------

* Python 3.0 or higher
* NumPy
* SciPy
* Matplotlib


Installation can be done using pip:

.. code:: bash
  
  pip install adjacent-correlation-analysis


or by cloning the repository and running:

.. code:: bash
  
  git clone

-----------
How to use 
-----------


To perform the **adjacent correlation analysis**, you can use the following code:

.. code-block:: python

   import adjacency_correlation_analysis as aca
   aca.adjacent_correlation_plot(xdata, ydata)
   plt.show()

which computes the corelation vector, and generates a plot of the correlation vectors overlaid on the density density constructed from the two images.

There are a number of parameters

 - ``bins:`` Number or sequence of bins used to compute the histogram for density estimation. 
              If None, an optimal bin size is automatically determined. Defaults to None.
 -   ``ax:`` matplotlib axes object. Defaults to plt.gca().
 -   ``scale, cmap, etc.``: plotting parameters.
 -    ``**kwargs:`` additional arguments for ``matplotlib.pyplot.imshow`` and ``quiver``.


To compute the adjacent correlation vectors, one can also use

.. code:: python

   import numpy as np
   import adjacency_correlation_analysis as aca
   H, xedges, yedges = np.histogram2d(xdata, ydata)
   p, nx, ny, i = aca.compute_correlation_vector(xdata, ydata, xedges, yedges)

where the input

- ``xdata`` and ``ydata`` are the two images (Numpy arrays) to be compared.
- ``xedges`` and ``yedges`` are the edges of the bins used to compute the histogram for density estimation.

The output is a tuple containing:

- ``p``: Degree of correlation 
- ``nx``: x-component of the correlation vector (normalized)
- ``ny``: y-component of the correlation vector (normalized)

- ``i``: total intensity of the correlation vector. i = (Ex**2 + Ey**2)**0.5, Ex = d p_1 / d x, Ey = d p_2 / d x

To visualize the result:

.. code:: python

   import matplotlib.pyplot as plt
   Ey = ny * p 
   Ex = nx * p
   plt.quiver(Ex, Ey)
   plt.show()

To compute the **adjacent correlation map**

.. code:: python

   import adjacency_correlation_analysis as aca
   p, angle, corr_coef, i = aca.compute_correlation_map(xdata, ydata)

where the input
- ``xdata`` and ``ydata`` are the two images (Numpy arrays) to be compared.

The output is a tuple containing:

 - ``p``: the correlation degree map, which is the normalized length of the correlation vector, p = (l_max / (l_min**2 + l_max**2)**0.5)
 - ``angle``: the correlation angle map, which is the direction of the correlation in the phase space, angle = np.arctan2(Ey, Ex)
 - ``corr_coef``: the correlation coefficient map, which is equivalent to the Pearson correlation coefficient.
 - ``i``: the intensity map, which is the total gradient in the phase space,  i = (Ex**2 + Ey**2)**0.5, Ex = d p_1 / d x, Ey = d p_2 / d x



To visualize the result:

.. code:: python

   import matplotlib.pyplot as plt
   plt.imshow(p)
   plt.imshow(angle)
   plt.show()

