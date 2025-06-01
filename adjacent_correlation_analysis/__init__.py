"""
Adjacent Correlation Analysis
A Python package for computing Stokes parameters and adjacent correlation plots.
"""
__version__ = "0.1.0"

from .analysis import compute_correlation_map, compute_correlation_vector, compute_correlation_matrix, compute_correlation_vector_p_nx_ny

from .plotting import adjacent_correlation_plot
