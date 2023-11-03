import unittest
import numpy as np
import qubit.qubit as qb

class TestQubit(unittest.TestCase):
    def test_init(self):
        # Test qubit initialization
        q = qb.Qubit()
        expected_mat = np.array([[1], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(q.mat, expected_mat))

        q = qb.Qubit(2, 2)
        expected_mat = np.array([[0], [0], [1], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(q.mat, expected_mat))

        with self.assertRaises(ValueError):
            # Value must be smaller than 2^n
            qb.Qubit(2, 4)

    def test_tensor_product(self):
        q1 = qb.Qubit(2, 1)  # |01>
        q2 = qb.Qubit(2, 2)  # |10>
        q3 = q1 * q2  # Expected: |0110>
        expected_mat = np.array([[0], [0], [0], [0], [0], [0], [1], [0], [0], [0], [0], [0], [0], [0], [0], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(q3.mat, expected_mat))

        with self.assertRaises(TypeError):
            # Tensor product defined between qubits
            q1.tensor_product(2)

    def test_str(self):
        q = qb.Qubit(2, 3)
        expected_str = "[[0.+0.j]\n [0.+0.j]\n [0.+0.j]\n [1.+0.j]]"
        actual_str = str(q)
        self.assertEqual(actual_str, expected_str)

    def test_mat_property(self):
        q = qb.Qubit(4, 3)  # 4 qubits
        new_mat = np.array([[1], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]], dtype=np.complex128)
        q.mat = new_mat
        self.assertTrue(np.allclose(q.mat, new_mat))
        self.assertEqual(len(q), 4)  # Ensure the number of qubits is a power of 2

        with self.assertRaises(ValueError):
            # Qubit must be a column vector
            q.mat = np.array([[1, 0], [0, 1]], dtype=np.complex128)

    def test_add(self):
        q1 = qb.Qubit(2, 1)  # |01>
        q2 = qb.Qubit(2, 2)  # |10>
        q_sum = q1 + q2 
        expected_mat = np.array([[0], [1], [1], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(q_sum.mat, expected_mat))

        with self.assertRaises(TypeError):
            # Addition defined between qubits
            q1 + 2

    def test_sub(self):
        q1 = qb.Qubit(2, 2)  # |01>
        q2 = qb.Qubit(2, 2)  # |10>
        q_diff = q1 - q2 
        expected_mat = np.array([[0], [0], [0], [0]], dtype=np.complex128)
        self.assertTrue(np.allclose(q_diff.mat, expected_mat))

        with self.assertRaises(TypeError):
            # Subtraction defined between qubits
            q1 - 2

if __name__ == '__main__':
    unittest.main()
