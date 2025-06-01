Concept & Methods
*******************************************



--------------------------------
Adjacency-induced correlations:
--------------------------------

The method is based on the observation that image values measured in adjacent locations often exhibit stronger correlations compared to image values measured over the whole region. Take the following example of the temperature and perception data from the North America:  When plotted together, we reveal a phase space where temperature and precipitation are not well-correlated. To reveal regularities, we choose three boxes (R1, R2 and R3) at different locations. From the west to the east, the temperature and precipitation exhibit correlations ranging from negative, to positive, then to weak correlations. These local correlations are undermined in the global correlation plot. 


.. image:: _static/adjacency_induced.png
   :alt: Adjacent Correlation Map
   :align: center
   :width: 500px

**Adjacency-induced correlations:** Values measured in small boxes, R1, R2, and R3 are stronger than correlations measured over the whole region.  


The *adjacent correlation analysis* is a method to reveal these local correlations in the phase space. The *adjacent correlation map* provide maps of correlations in the space were the quantities are measured. 

Given two images, :math:`p_1(x, y)` and :math:`p_2(x, y)`, the *adjacency correlation map* contains a correlation angle map,

.. math::
  \theta(x,y) = \arctan(\frac{ d p_2}{d p_1})

a map of the correlation degree:

.. math::
   p(x,y) = \frac{l_{max}}{(l_{min}^2 + l_{max}^2)^{1/2}}

where :math:`l_{min}` and :math:`l_{max}` are the minimum and maximum lengths of the correlation ellipse, and a correlation coefficient map:

.. math::
   r(x,y) = \frac{\sigma(p_1 p_2)}{ \sigma(p_1) \sigma(p_2)}


which is the equivalent to the Pearson correlation coefficient.

The *adjacent correlation plot* is a representation of these correlations in the phase space.

-------------------------------------------------
Superimpose correlations using Stokes parameters
-------------------------------------------------

To superimpose the adjacent correlation vectors, we can use Stokes parameters. The Stokes parameters are a set of four parameters that describe the polarization state of light. In this case, we can use them to represent the correlation vectors.

.. image:: _static/stokes.png
   :alt: Stokes Parameters
   :align: center
   :width: 500px


In the :math:`p_1-p_2` space, the correlation vector is 

.. math::
       \vec{E} = (E_x, E_y) = ({d} p_1, {d} p_2)

where the pseudo-Stokes parameters are defined as:

.. math::
  I = \frac{1}{2} (E_x^2 + E_y^2) \\
  Q = \frac{1}{2} (E_x^2 - E_y^2)\\
  U = E_x E_y\\

The stokes parameters are used to superimpose these correlation vectors, and in the last step, the correlation angle and degree can be computed from the stokes parameter using 


.. math::
      \theta = \frac{1}{2} \arctan \left( \frac{U}{Q} \right)

    p = \left( \left( Q/I\right)^2 + \left(U/I\right)  \right)^{1/2}


From which, :math:`E_x` and :math:`E_y` can be computed. 

