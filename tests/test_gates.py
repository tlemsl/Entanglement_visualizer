import unittest
import math
import numpy as np
import qubit.gates as qg
import qubit.qubit as qb


class TestQuantumGates(unittest.TestCase):

    def test_base_gate(self):
        base_gate = qg.Base(2, 0)
        qubit = qb.Qubit(2, 0)
        result = base_gate * qubit
        expected = qb.Qubit(2, 0)
        self.assertTrue(np.allclose(result.mat, expected.mat))

    def test_x_gate(self):
        x_gate = qg.X(2, 0)
        qubit = qb.Qubit(2, 0)
        result = x_gate * qubit
        expected = qb.Qubit(2, 1)
        self.assertTrue(np.allclose(result.mat, expected.mat))

    def test_z_gate(self):
        z_gate = qg.Z(2, 0)
        qubit = qb.Qubit(2, 1)
        result = z_gate * z_gate * qubit
        expected = qb.Qubit(2, 1)
        self.assertTrue(np.allclose(result.mat, expected.mat))

    def test_h_gate(self):
        h_gate = qg.H(1, 0)
        qubit = qb.Qubit(1, 0)
        result = h_gate * qubit
        expected = qb.Qubit()
        expected.mat = np.array([[1], [1]], dtype=np.complex128) / math.sqrt(2)
        self.assertTrue(np.allclose(result.mat, expected.mat))

    def test_multiple_gates(self):
        x_gate = qg.X(2, 0)
        z_gate = qg.Z(2, 1)
        h_gate = qg.H(2, 0)

        qubit = qb.Qubit(2, 0)
        result = z_gate * h_gate * x_gate * qubit

        expected = qb.Qubit(2, 0)
        expected.mat = np.array(
            [[0.70710678 + 0.j], [-0.70710678 + 0.j], [0], [0]],
            dtype=np.complex128)
        self.assertTrue(np.allclose(result.mat, expected.mat))


if __name__ == '__main__':
    unittest.main()
