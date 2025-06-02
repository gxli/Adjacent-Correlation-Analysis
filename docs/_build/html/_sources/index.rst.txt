.. Adjacent-Correlation-Analysis documentation master file, created by
   sphinx-quickstart on Sun Jun  1 16:04:03 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Adjacent-Correlation-Analysis documentation
===========================================


.. image:: _static/aca_logo.png
  :width: 600
  :alt: ACA logo
  :align: center


Welcome to the Adjacent-Correlation-Analysis documentation!


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   feature.rst
   concept.rst
   installation.rst
   adjacent_correlation_analysis.rst
   adjacent_correlation_mapping.rst
   time_series.rst
   interactive.rst
   manifold.rst
   contribute.rst
   credit.rst



Features & Design
------------------
A Python package for performing adjacent correlation analysis on image data. 

The input are images 1 and image 2, in the form of Numpy arrays of the same size. The method is designed to reveal regularities by comparing these images through correlations.

.. image:: _static/illus_website.jpg
   :alt: Adjacent Correlation Analysis
   :align: center
   :width: 500px


The **adjacent correlation analysis** is performed by calculating and visualizing the **adjacency-induced correlation** in the phase space. The **adjacent correlation map** is a spatially-resolved representation of the correlation between the two images.

The methods are designed to represent the data using correlations, which can be used to perform visualization and interactive data explorations. 

