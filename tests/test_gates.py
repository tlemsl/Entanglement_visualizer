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

    def test_y_gate(self):
        y_gate = qg.Y(2, 0)
        qubit = qb.Qubit(2, 1)  # |01>
        result = y_gate * qubit
        expected = qb.Qubit(2, 0)  # Expected to be -|00> after Y gate
        # Y gate applies iσy, so the result should be multiplied by i
        expected.mat = np.array([[-1j], [0], [0], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(result.mat, expected.mat))

    def test_y_gate_squared(self):
        y_gate = qg.Y(1, 0)
        qubit = qb.Qubit(1, 0)  # |0>
        result = y_gate * y_gate * qubit
        # Applying Y gate twice should be equivalent to applying a I.
        expected = qb.Qubit(1, 0)  # |0>
        self.assertTrue(np.allclose(result.mat, expected.mat))

    def test_controlled_x_gate(self):
        cx_gate = qg.X(
            n=2, target=0,
            control=1)  # CNOT with control on qubit 0 and target on qubit 1
        qubit = qb.Qubit(2, 0b10)  # |10>
        result = cx_gate * qubit
        expected = qb.Qubit(2, 0b11)  # Should be |11> after CNOT
        self.assertTrue(np.allclose(result.mat, expected.mat))

    def test_controlled_z_gate(self):
        cz_gate = qg.Z(
            n=2, target=0,
            control=1)  # CZ with control on qubit 0 and target on qubit 1
        qubit = qb.Qubit(2, 0b11)  # |11>
        result = cz_gate * qubit
        # CZ flips the phase of the target qubit if the control qubit is |1>
        expected = qb.Qubit(2, 0b11)
        expected.mat = np.array([[0], [0], [0], [-1]], dtype=np.complex128)
        self.assertTrue(np.allclose(result.mat, expected.mat))

    def test_controlled_h_gate(self):
        ch_gate = qg.H(
            n=2, target=0,
            control=1)  # CH gate with control on qubit 0 and target on qubit 1
        qubit = qb.Qubit(2, 0b10)  # |10>
        result = ch_gate * qubit
        # CH should apply Hadamard on the target qubit if the control qubit is |1>
        expected = qb.Qubit(2, 0b10)
        expected.mat = np.array([[0], [0], [1], [1]],
                                dtype=np.complex128) / math.sqrt(2)
        self.assertTrue(np.allclose(result.mat, expected.mat))


if __name__ == '__main__':
    unittest.main()
