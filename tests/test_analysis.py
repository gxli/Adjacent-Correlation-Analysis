import unittest
import numpy as np
from adjacent_correlation_analysis.analysis import compute_stokes, compute_angle

class TestAnalysis(unittest.TestCase):
    def test_compute_stokes(self):
        ex = np.array([1.0, 0.0])
        ey = np.array([0.0, 1.0])
        i, q, u = compute_stokes(ex, ey, normed=False)
        self.assertTrue(np.allclose(i, [1.0, 1.0]))
        self.assertTrue(np.allclose(q, [1.0, -1.0]))
        self.assertTrue(np.allclose(u, [0.0, 0.0]))

    def test_compute_angle(self):
        i = np.array([1.0])
        q = np.array([0.5])
        u = np.array([0.5])
        p, ex, ey = compute_angle(i, q, u)
        self.assertTrue(np.allclose(p, [np.sqrt(0.5**2 + 0.5**2)]))
        self.assertTrue(np.allclose(ex, [np.cos(0.25 * np.pi)]))
        self.assertTrue(np.allclose(ey, [np.sin(0.25 * np.pi)]))

if __name__ == '__main__':
    unittest.main()
