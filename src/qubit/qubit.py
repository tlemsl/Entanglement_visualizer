"""
entanglement_visualizer.qubits.qubits

Defines the Qubit class for quantum qubits and operations.

Author: Minjong Kim
Email: tlemsl@dgist.ac.kr
Website: https://github.com/tlemsl/Entanglement_visualizer

Classes:
    Qubit: Represents quantum qubits and their operations.
"""

import math
import numpy as np
import qubit.entanglment
Threshold = complex(0.0001)


class Qubit:
    """A class representing a quantum qubit.

    Args:
        n (int, optional): The number of qubits (default is 1).
        v (int, optional): The value of the qubit (default is 1).

    Raises:
        ValueError: If the specified value is not smaller than 2^n.

    Attributes:
        mat (numpy.ndarray): The column vector 
                             representation of the qubit state.
        n (int): The number of qubits in the state.
    """

    def __init__(self, n: int = 1, v: int = 0):
        """Initialize a quantum qubit.

        Args:
            n (int, optional): The number of qubits (default is 1).
            v (int, optional): The value of the qubit (default is 0).

        Raises:
            ValueError: If the specified value is not smaller than 2^n.
        """
        if 2**n <= v:
            raise ValueError("Value must be smaller than 2^n")

        self._n = n
        self._mat = np.zeros((2**n, 1), dtype=np.complex128)
        self._mat[v, 0] = 1

    def tensor_product(self, other):
        """Compute the tensor product of two qubits.

        Args:
            other (Qubit): The other qubit to compute the tensor product with.

        Returns:
            Qubit: A new Qubit instance representing the tensor product state.

        Raises:
            TypeError: If the input is not a Qubit instance.
        """
        if not isinstance(other, Qubit):
            raise TypeError("Qubit tensor product is defined between qubits")
        ret = Qubit()
        ret.mat = np.kron(self.mat, other.mat)
        return ret

    def __mul__(self, other):
        """Multiply two qubits using the tensor product.

        Args:
            other (Qubit): The other qubit to multiply with.

        Returns:
            Qubit: A new Qubit instance representing 
                   the result of the multiplication.
        """
        return self.tensor_product(other)

    def __add__(self, other):
        """Add two qubits element-wise.

        Args:
            other (Qubit): The other qubit to add with.

        Returns:
            Qubit: A new Qubit instance representing the element-wise sum.
        """
        if not isinstance(other, Qubit):
            raise TypeError("Qubit addition is defined between qubits")
        ret = Qubit()
        ret.mat = self.mat + other.mat
        return ret

    def __sub__(self, other):
        """Subtract two qubits element-wise.

        Args:
            other (Qubit): The other qubit to subtract.

        Returns:
            Qubit: A new Qubit instance representing the 
                   element-wise difference.
        """
        if not isinstance(other, Qubit):
            raise TypeError("Qubit subtraction is defined between qubits")
        ret = Qubit()
        ret.mat = self.mat - other.mat
        return ret

    def __str__(self) -> str:
        """Return a string representation of the qubit state."""
        ret = ""
        for i in range(2**self._n):
            if self.mat[i, 0]:
                binary = str(bin(i))[2:]
                ret += f"{self.mat[i,0]}|{binary.zfill(self._n)}>"
                ret += " + "
        return ret[:-3]

    def __len__(self) -> int:
        """Return the number of qubits in the state."""
        return self._n

    @property
    def mat(self):
        """Getter for the qubit's state matrix."""
        return self._mat

    @mat.setter
    def mat(self, data):
        """Setter for the qubit's state matrix.

        Args:
            data (numpy.ndarray): The new state matrix.

        Raises:
            ValueError: If the input matrix is not a valid column vector.
        """
        if data.shape[1] != 1:
            raise ValueError("Qubit must be a column vector!")
        self._mat = data
        self._n = int(math.log2(self._mat.shape[0]))

    @property
    def T(self):
        """Getter for the qubit's conjugate transpose (Hermitian conjugate)"""
        return self._mat.conjugate().T

    def entangled(self):
        """Determines if the qubit state is entangled.

        Entanglement is a fundamental property of quantum mechanics, where the
        state of one qubit is correlated with the state of another. This method
        checks if such entanglement exists in the qubit state.

        Returns:
            list: Indices of qubits that are part of an entanglement set.
        """

        return qubit.entanglment.entanglement(self.mat)

    @staticmethod
    def base(n, k):
        """Create a base state vector for a given qubit configuration.

        This static method creates a state vector representing a base state
        in a quantum system with a specified number of qubits. The base state
        has a value of 1 in the k-th position and 0 elsewhere.

        Args:
            n (int): The number of qubits.
            k (int): The position in the state vector to be set to 1.

        Returns:
            numpy.ndarray: A state vector representing the base state.
        """

        ret = np.zeros((n, 1), dtype=np.complex128)
        ret[k, 0] = 1
        return ret
