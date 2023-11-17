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
        print(f"init _n: {self._n}")
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
                print(f"binary in __str__: {binary}")
                print(f"n: {len(self)}") # Why this is 2?
                print(f"n: {self._n}")
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
        print(f"mat setter _n: {int(math.sqrt(self._mat.shape[0]))}")
        self._n = int(math.sqrt(self._mat.shape[0]))

    @property
    def T(self):
        """Getter for the qubit's conjugate transpose (Hermitian conjugate)"""
        return self._mat.conjugate().T
