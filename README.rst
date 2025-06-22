.. -*- mode: rst -*-

.. image:: images/aca_logo.png
  :width: 600
  :alt: ACA logo
  :align: center

======================================================================
Adjacent Correlation Analysis: Revealing Regularities in Image Data
======================================================================

Adjacent Correlation Analysis (ACA) is a Python package designed to uncover
hidden regularities and relationships within image datasets by analyzing
localized correlations. It provides tools for both **Adjacent Correlation
Analysis** (visualizing correlations in phase space) and **Adjacent Correlation
Map** (spatial mapping of correlation properties). 

Documentation Available at: `ReadTheDocs <https://adjacent-correlation-analysis.readthedocs.io/en/latest/>`_.

---

Features & Design
------------------
ACA helps you analyze relationships between two images (Numpy arrays of the same size) by comparing them through correlations. The core idea is to reveal **adjacency-induced correlations** that might be obscured when looking at global statistics.

.. image:: images/illus_website.jpg
   :alt: Adjacent Correlation Analysis
   :align: center
   :width: 600px

The *adjacent correlation analysis* process involves calculating and visualizing the *adjacency-induced correlation* within the phase space defined by the two images. The *adjacent correlation map* then provides a spatially-resolved representation of these correlations.

These methods are specifically designed to represent data using correlations, facilitating powerful visualization and interactive data exploration.

---

Adjacent Correlation Analysis: Spatially-aware 2D histograms for data visualization
------------------------------------------------------------------------------------
The **adjacent correlation analysis** is a method which allow users to
visualize the local correlations between two images in a more intuitive way.
By comparing two images using  2D histograms, the spatial information is lost.
The *adjacent correlation analysis* allows for the evaluation of vectors
representing *locally-induced correlations* in the phase space.



.. The **Adjacent Correlation Analysis** method derives correlation vectors that can be plotted on top of the Probability Density Function (PDF) of the two image datasets. These vectors indicate the local correlation strength and direction within the phase space.

.. image:: images/aca_illus_climate.001.png
   :alt: Example of adjacent correlation analysis
   :align: center
   :width: 600px

**Application to MHD Turbulence Simulation Data:** This example shows correlation vector fields overlaid on a density map (density PDF). The **correlation degree** represents the normalized length of the vector, and both the length and orientation are clearly visible in the *adjacent correlation plot*.

.. image:: images/pdf_aca_lorentz.png
   :alt: Example of adjacent correlation analysis
   :align: center
   :width: 600px

**Application to the Lorentz System:** Here, vectors derived using adjacent correlation analysis provide a projected view of the vector field in the phase space on the x-y plane, illustrating the system's dynamic regularities.

---

Adjacent Correlation Map: Visualizing Correlations between Quantities
---------------------------------------------------------------------------------
The **Adjacent Correlation Map** provides spatially-resolved maps of the correlations between two images. It generates a correlation angle map, a correlation degree map, and a correlation coefficient map.

.. image:: images/acm_climate_example.001.png
   :alt: Example of adjacent correlation map
   :align: center
   :width: 600px

**Application to Temperature and Precipitation Data:** This output demonstrates the correlation angle map, correlation degree map, and correlation coefficient map (available as program output). The **correlation angle map** indicates the direction of the correlation in phase space, while the **correlation degree map** shows the strength of the correlation. Different colors highlight distinct correlation patterns between temperature (T) and log(precipitation).




Installation & Usage 
-----------------------

Requirements:
-------------

* Python 3.0 or higher
* NumPy
* SciPy
* Matplotlib

Installation can be done using pip:

.. code:: bash

   pip install -i https://test.pypi.org/simple/ adjacent-correlation-analysis==0.1.1

Alternatively, you can clone the repository and install it in editable mode:

.. code:: bash

  git clone https://github.com/gxli/Adjacent-Correlation-Analysis
  cd Adjacent-Correlation-Analysis
  pip install -e .

How to Use
-----------

To perform the **adjacent correlation analysis** and generate a plot of the correlation vectors overlaid on the density map:

.. code-block:: python

   import adjacent_correlation_analysis as aca
   import matplotlib.pyplot as plt

   # xdata and ydata are your two image arrays
   aca.adjacent_correlation_plot(xdata, ydata)
   plt.show()

Available parameters for `adjacent_correlation_plot`:

* ``bins``: Number or sequence of bins used for density estimation. If `None`, an optimal bin size is automatically determined. Defaults to `None`.
* ``ax``: Matplotlib axes object to plot on. Defaults to `plt.gca()`.
* ``scale``, ``cmap``, etc.: Plotting parameters for customization.
* ``**kwargs``: Additional arguments passed to `matplotlib.pyplot.imshow` and `matplotlib.pyplot.quiver`.
* ``cmap``: Colormap to be used for the density map. Defaults to 'viridis'.
* ``facecolor``: Face color of the quiver arrows. Defaults to 'w'.
* ``scale``: Scaling factor for the quiver arrows. Defaults to 20.
* ``lognorm``: Whether to use logarithmic normalization for the density map. Defaults to `False`.

To compute the adjacent correlation vectors directly:

.. code:: python

   import numpy as np
   import adjacency_correlation_analysis as aca

   # xdata and ydata are your two image arrays
   H, xedges, yedges = np.histogram2d(xdata, ydata)
   ex, ey = aca.compute_correlation_vector(xdata, ydata, xedges, yedges)

**Inputs:**

* ``xdata`` and ``ydata``: The two input images (Numpy arrays) to be compared.
* ``xedges`` and ``yedges``: The bin edges used to compute the histogram for density estimation.

**Outputs (tuple):**

* ``p``: Degree of correlation.
* ``nx``: Normalized x-component of the correlation vector.
* ``ny``: Normalized y-component of the correlation vector.
* ``i``: Total intensity of the correlation vector, $i = \sqrt{Ex^2 + Ey^2}$, where $Ex = \frac{d p_1}{d x}$ and $Ey = \frac{d p_2}{d x}$.

To visualize the computed vectors:

.. code:: python

   import matplotlib.pyplot as plt
   import numpy as np

   # Assuming ex, ey, xedges, yedges are already computed
   xx = np.linspace(xedges[0], xedges[-1], len(xedges)-1)
   yy = np.linspace(yedges[0], yedges[-1], len(yedges)-1)
   x_grid, y_grid = np.meshgrid(xx, yy)

   # Plotting the result
   plt.quiver(x_grid, y_grid, ex.T, ey.T, facecolor='w', angles='xy', scale=30, headaxislength=0)
   plt.show()

To compute the **adjacent correlation map**:

.. code:: python

   import adjacency_correlation_analysis as aca

   # xdata and ydata are your two image arrays
   p, angle, corr_coef, i = aca.compute_correlation_map(xdata, ydata)

**Inputs:**

* ``xdata`` and ``ydata``: The two input images (Numpy arrays) to be compared.

**Outputs (tuple):**

* ``p``: The **correlation degree map**, which is the normalized length of the correlation vector, $p = \frac{l_{max}}{(l_{min}^2 + l_{max}^2)^{1/2}}$.
* ``angle``: The **correlation angle map**, representing the direction of the correlation in phase space, $angle = \arctan2(Ey, Ex)$.
* ``corr_coef``: The **correlation coefficient map**, equivalent to the Pearson correlation coefficient.
* ``i``: The **intensity map**, representing the total gradient in the phase space, $i = \sqrt{Ex^2 + Ey^2}$, where $Ex = \frac{d p_1}{d x}$ and $Ey = \frac{d p_2}{d x}$.

To visualize the map results:

.. code:: python

   import matplotlib.pyplot as plt

   # Assuming p and angle are already computed
   plt.imshow(p)
   plt.imshow(angle)
   plt.show()

---

Foundation of Adjacent Correlation Analysis
--------------------------------------------

Adjacency-induced Correlations:
--------------------------------
The methodology is rooted in the observation that image values measured in **adjacent locations** often exhibit stronger, more discernible correlations compared to values measured across an entire region. Consider the example of temperature and precipitation data across North America: when plotted globally, they may appear weakly correlated. However, by selecting localized regions (R1, R2, R3), distinct local correlations emerge—ranging from negative to positive to weak—that are otherwise obscured by the overall global average.

.. image:: images/adjacency_induced.png
   :alt: Adjacency-induced Correlations
   :align: center
   :width: 600px

**Adjacency-induced correlations:** Values measured in small boxes (R1, R2, and R3) demonstrate stronger correlations than those measured over the entire region.

The *adjacent correlation analysis* is designed to reveal these localized correlations within the phase space, while the *adjacent correlation map* provides a spatial representation of these correlations in the measurement domain.

Given two images, $p_1(x, y)$ and $p_2(x, y)$, the *adjacency correlation map* comprises:

* A **correlation angle map**:
    .. math::
      \theta(x,y) = \arctan\left(\frac{ d p_2}{d p_1}\right)

* A **correlation degree map**:
    .. math::
       p(x,y) = \frac{l_{max}}{(l_{min}^2 + l_{max}^2)^{1/2}}

    where $l_{min}$ and $l_{max}$ are the minimum and maximum lengths of the correlation ellipse.

* A **correlation coefficient map**:
    .. math::
       r(x,y) = \frac{\sigma(p_1 p_2)}{ \sigma(p_1) \sigma(p_2)}

    which is equivalent to the Pearson correlation coefficient.

The *adjacent correlation plot* then provides a visual representation of these correlations within the phase space.

---

Superimposing Correlations Using Stokes Parameters
--------------------------------------------------
To effectively superimpose the adjacent correlation vectors, we leverage **Stokes parameters**, commonly used to describe the polarization state of light. Here, they are adapted to represent the correlation vectors.

In the $p_1-p_2$ phase space, the correlation vector is defined as:

.. math::
       \vec{E} = (E_x, E_y) = (dp_1, dp_2)

The pseudo-Stokes parameters are then defined as:

.. math::
  I = \frac{1}{2} (E_x^2 + E_y^2) \\
  Q = \frac{1}{2} (E_x^2 - E_y^2)\\
  U = E_x E_y\\

These Stokes parameters are used to combine and represent multiple correlation vectors. The correlation angle and degree can subsequently be computed from the Stokes parameters using:

.. math::
      \theta = \frac{1}{2} \arctan \left( \frac{U}{Q} \right)

    p = \left( \left( Q/I\right)^2 + \left(U/I\right)^2  \right)^{1/2}

From these, $E_x$ and $E_y$ can be re-derived.

.. image:: images/stokes.png
   :alt: Stokes Parameters
   :align: center
   :width: 600px

---

Manifold Interpretation
-------------------------
.. image:: images/interpretation.png
   :alt: Manifold Interpretation
   :align: center
   :width: 600px

What do the lines observed in the adjacent correlation plot signify?

For systems governed by partial differential equations (PDEs), rapid processes can constrain the system to a low-dimensional **manifold** within the phase space. On this manifold, local variations can be described by a vector field. The presence of slowly evolving variables ($C$) might play a role in separating different trajectories, which in turn correspond to distinct spatially coherent regions.

Consider the correlation between income and apartment size. When measured in localized regions, higher income often correlates with larger apartments, and vice versa. However, across an entire country, this correlation might appear weak. This is because apartment size is influenced not only by income but also by other **hidden, slow-changing parameters** such as GDP per capita, city size, etc. When these unmeasured parameters vary slowly across space, they can induce the observed local correlations.

Thus, the correlation vectors observed in the adjacent correlation plot tend to follow lines of constant $C$, where $C$ represents a hidden, slow-varying parameter.



Interactive Data Exploration
----------------------------
Adjacent Correlation Analysis is designed to be highly compatible with interactive visualization tools. We recommend using software like `Glue <https://glueviz.org/>`_ to explore your data interact capabilities.

.. image:: images/interactive.png
   :alt: Interactive Data Exploration
   :align: center
   :width: 600px

**Interactive Data Exploration:** ACA facilitates interactive exploration of complex datasets, revealing insights that might be missed with static visualizations.



Contribute
----------
We welcome contributions to the Adjacent Correlation Analysis project!


* **Issue Tracker:** `github.com/gxli/Adjacent-Correlation-Analysis/issues <https://github.com/gxli/Adjacent-Correlation-Analysis/issues>`_
* **Source Code:** `github.com/gxli/Adjacent-Correlation-Analysis <https://github.com/gxli/Adjacent-Correlation-Analysis>`_




References
------------------------------
If you utilize this software in your research, we kindly request you cite the following papers:

**Adjacent Correlation Analysis:**

* *Revealing hidden correlations from complex spatial distributions: Adjacent Correlation Analysis*, Li (2025), `arXiv:2506.05759 <https://arxiv.org/abs/2506.05759>`_

.. code:: bibtex

   @article{li2025revealinghiddencorrelationscomplex,
         title={Revealing hidden correlations from complex spatial distributions: Adjacent Correlation Analysis}, 
         author={Guang-Xing Li},
         year={2025},
         eprint={2506.05759},
         archivePrefix={arXiv},
         primaryClass={physics.comp-ph},
         url={https://arxiv.org/abs/2506.05759}, 
   }


**Adjacent Correlation Map:**

* *Mapping correlations and coherence: adjacency-based approach to data visualization and regularity discovery*, Li (2025), `arXiv:2506.05758 <https://arxiv.org/abs/2506.05758>`_


.. code:: bibtex


   @article{li2025mappingcorrelationscoherenceadjacencybased,
         title={Mapping correlations and coherence: adjacency-based approach to data visualization and regularity discovery}, 
         author={Guang-Xing Li},
         year={2025},
         eprint={2506.05758},
         archivePrefix={arXiv},
         primaryClass={physics.comp-ph},
         url={https://arxiv.org/abs/2506.05758}, 
   }



Support
----------
If you encounter any issues or have questions, please reach out. We have a mailing list available at: `https://groups.google.com/g/adjacentcorrelationanalysis <https://groups.google.com/g/adjacentcorrelationanalysis>`_




License
-------
The project is licensed under the GPLv3. 
