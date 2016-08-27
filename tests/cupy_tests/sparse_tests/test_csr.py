import unittest

import numpy
import scipy.sparse

import cupy
import cupy.sparse
from cupy import testing


class TestCsrMatrix(unittest.TestCase):

    def setUp(self):
        data = cupy.array([1, 2, 3, 4], 'f')
        indices = cupy.array([0, 1, 3, 2], 'i')
        indptr = cupy.array([0, 2, 3, 4], 'i')
        self.m = cupy.sparse.csr_matrix((data, indices, indptr), shape=(3, 4))

    def test_nnz(self):
        self.assertEqual(self.m.nnz, 4)

    def test_str(self):
        self.assertEqual(str(self.m), '''  (0, 0)\t1.0
  (0, 1)\t2.0
  (1, 3)\t3.0
  (2, 2)\t4.0''')

    def test_toarray(self):
        m = self.m.toarray()
        expect = [
            [1, 2, 0, 0],
            [0, 0, 0, 3],
            [0, 0, 4, 0]
        ]
        cupy.testing.assert_allclose(m, expect)


class TestCsrMatrixScipyComparison(unittest.TestCase):

    def make(self, xp, sp):
        data = xp.array([1, 2, 3, 4], 'f')
        indices = xp.array([0, 1, 3, 2], 'i')
        indptr = xp.array([0, 2, 3, 4], 'i')
        return sp.csr_matrix((data, indices, indptr), shape=(3, 4))

    @testing.scipy_cupy_allclose(accept_error=False)
    def test_dot(self, xp, sp):
        m = self.make(xp, sp)
        x = xp.arange(4).astype('f')
        return m.dot(x)