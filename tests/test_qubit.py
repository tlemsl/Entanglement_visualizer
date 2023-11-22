import unittest
import numpy as np
import qubit.qubit as qb


class TestQubit(unittest.TestCase):

    def test_init(self):
        """Test Qubit initialization with default/specific values."""
        q = qb.Qubit()
        expected_mat = np.array([[1], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(q.mat, expected_mat))

        q = qb.Qubit(2, 2)
        expected_mat = np.array([[0], [0], [1], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(q.mat, expected_mat))

        with self.assertRaises(ValueError):
            qb.Qubit(2, 4)

    def test_tensor_product(self):
        """Test tensor product of two qubits for correctness."""
        q1 = qb.Qubit(2, 1)  # |01>
        q2 = qb.Qubit(2, 2)  # |10>
        q3 = q1 * q2
        expected_mat = np.zeros((16, 1), dtype=np.complex128)
        expected_mat[6, 0] = 1
        self.assertTrue(np.allclose(q3.mat, expected_mat))

        with self.assertRaises(TypeError):
            q1.tensor_product(2)

    def test_str(self):
        """Test string representation of a qubit."""
        # This qubit is in state |3>, which corresponds to binary |11>

        q = qb.Qubit(2, 3)
        expected_str = "(1+0j)|11>"
        actual_str = str(q)
        self.assertEqual(actual_str, expected_str)

        # This qubit is in a superposition state with non-zero amplitudes
        # for basis states |1> and |2>. Let's simulate it by adding two qubits.
        q1 = qb.Qubit(2, 1)  # |01>
        q2 = qb.Qubit(2, 2)  # |10>
        q_super = q1 + q2
        expected_super_str = "(1+0j)|01> + (1+0j)|10>"
        actual_super_str = str(q_super)
        self.assertEqual(actual_super_str, expected_super_str)

        # A qubit with all zero amplitudes should return an empty string
        q_zero = qb.Qubit(2)
        expected_zero_str = "(1+0j)|00>"
        actual_zero_str = str(q_zero)
        self.assertEqual(actual_zero_str, expected_zero_str)

    def test_mat_property(self):
        """Test qubit's state matrix property getters/setters."""
        q = qb.Qubit(4, 3)
        new_mat = np.zeros((16, 1), dtype=np.complex128)
        new_mat[0, 0] = 1
        q.mat = new_mat
        self.assertTrue(np.allclose(q.mat, new_mat))
        self.assertEqual(len(q), 4)

        with self.assertRaises(ValueError):
            q.mat = np.array([[1, 0], [0, 1]], dtype=np.complex128)

    def test_add(self):
        """Test element-wise addition of two qubits."""
        q1 = qb.Qubit(2, 1)  # |01>
        q2 = qb.Qubit(2, 2)  # |10>
        q_sum = q1 + q2
        expected_mat = np.array([[0], [1], [1], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(q_sum.mat, expected_mat))

        with self.assertRaises(TypeError):
            q1 + 2

    def test_sub(self):
        """Test element-wise subtraction of two qubits."""
        q1 = qb.Qubit(2, 2)  # |10>
        q2 = qb.Qubit(2, 2)  # |10>
        q_diff = q1 - q2
        expected_mat = np.zeros((4, 1), dtype=np.complex128)
        self.assertTrue(np.allclose(q_diff.mat, expected_mat))

        with self.assertRaises(TypeError):
            q1 - 2

    def test_Conjugate_function(self):
        """Test the T property for correct conjugate transpose."""
        qubit = qb.Qubit(n=1, v=0)
        conjugate_transpose = qubit.T
        expected_output = np.array([[1, 0]], dtype=np.complex128)

        self.assertTrue(np.array_equal(conjugate_transpose, expected_output),
                        "T function does not produce correct result.")

    def test_not_entangled(self):
        """Test with a qubit state that is not entangled."""
        qubit = qb.Qubit(2, 0)  # Initialize a 2-qubit state |00>
        self.assertEqual(qubit.entangled(), [])

    def test_entangled(self):
        """Test with an entangled qubit state."""
        qubit = qb.Qubit(2)
        # Creating an entangled state
        # for example, Bell state |Ψ+> = (|00> + |11>)/sqrt(2)
        qubit.mat = np.array([[1 / np.sqrt(2)], [0], [0], [1 / np.sqrt(2)]],
                             dtype=np.complex128)
        self.assertEqual(qubit.entangled(),
                         [0, 1])  # Both qubits should be entangled

    def test_partial_entanglement(self):
        """Test with partially entangled qubits."""
        # Assuming the 'entangled' method returns indices of qubits 
        # that are part of an entanglement
        qubit = qb.Qubit(3)  # Initialize a 3-qubit state
        # Creating a state where first two qubits are entangled 
        # and the third is not
        # For example, |Ψ> = (|000> + |110>)/sqrt(2)
        qubit.mat = np.array(
            [[1 / np.sqrt(2)], [0], [0], [0], [0], [0], [1 / np.sqrt(2)], [0]],
            dtype=np.complex128)
        self.assertEqual(qubit.entangled(),
                         [1, 2])  # Only the first two qubits are entangled


if __name__ == '__main__':
    unittest.main()
