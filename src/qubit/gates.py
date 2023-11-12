"""
Quantum Gates and Operations

This module defines quantum gates and operations for quantum computing. It includes the
base quantum gate class `Base`, X gate `X`, Y gate `Y`, Z gate `Z`, and Hadamard gate `H`.

Author: Minjong Kim
Email: tlemsl@dgist.ac.kr
Website: https://github.com/tlemsl/Entanglement_visualizer

Classes:
    Base: Base class representing a quantum gate.
    X: Class representing an X gate.
    Y: Class representing a Y (Pauli-Y) gate.
    Z: Class representing a Z gate.
    H: Class representing an H (Hadamard) gate.
"""

import math
import numpy as np
import qubit.qubit as qb

Identity_matrix = np.identity(2, dtype=np.complex128)
Base0 = np.array([[1, 0], [0, 0]], dtype=np.complex128)
Base1 = np.array([[0, 0], [0, 1]], dtype=np.complex128)


class Base(object):
    """Base class representing a quantum gate.

    This class serves as the base for quantum gate implementations.

    Attributes:
        _n (int): The number of qubits.
        _target (int): The target qubit index.
        _base_mat (numpy.ndarray): The base matrix representing the gate.
    """

    def __init__(self, n: int = 1, target: int = 0, control: int = -1) -> None:
        """Initialize a base quantum gate.

        Args:
            n (int, optional): The number of qubits (default is 1).
            target (int, optional): The target qubit index (default is 0).
            control (int, optional): The index of the control qubit
                                     (default is -1, which means uncontrolled).

        Raises:
            ValueError: If the target qubit is not smaller than n.
        """
        if n <= target:
            raise ValueError(f"Target({target}) must be smaller than n({n})")
        self._base_mat = Identity_matrix
        self._n = n
        self._target = target
        self._control = control
        self._mat = self._form_matrix()

    def __mul__(self, other):
        """Multiply two quantum gates using matrix multiplication.

        Args:
            other (Base or qb.Qubit): The other gate or qubit to multiply with.

        Returns:
            Base or qb.Qubit: A new gate or qubit representing 
                              the result of the multiplication.
        """
        if isinstance(other, qb.Qubit):
            ret = qb.Qubit()
        else:
            ret = Base()
        ret.mat = np.dot(self.mat, other.mat)
        return ret

    def __len__(self):
        """Get the number of qubits affected by the gate.

        Returns:
            int: The number of qubits.
        """
        return self._n

    def __str__(self) -> str:
        return self._mat.__str__()

    @property
    def mat(self):
        """Getter for the gate's matrix form.

        Returns:
            numpy.ndarray: The matrix representation of the gate.
        """
        return self._mat

    @mat.setter
    def mat(self, data):
        """Setter for the gate's matrix form.

        Args:
            data (numpy.ndarray): The new matrix.

        Raises:
            ValueError: If the input matrix is not a valid square matrix.
        """
        if data.shape[0] != data.shape[1]:
            raise ValueError("Matrix must be a square matrix")
        self._mat = data
        self._n = int(math.sqrt(self._mat.shape[0]))

    def _form_matrix(self):
        """Form the matrix representation of the gate.

        Returns:
            numpy.ndarray: The matrix representation of the gate.
        """
        ret = Identity_matrix
        if self._control == -1:
            if self._target == (self._n - 1):
                ret = self._base_mat
            for i in range(self._n - 2, -1, -1):
                if i == self._target:
                    ret = np.kron(ret, self._base_mat)
                else:
                    ret = np.kron(ret, Identity_matrix)

        else:
            base0 = base1 = Identity_matrix
            if self._target == self._n - 1:
                base0 = Identity_matrix
                base1 = self._base_mat
            elif self._control == self._n - 1:
                base0 = Base0
                base1 = Base1
            for i in range(self._n - 2, -1, -1):
                if i == self._target:
                    base0 = np.kron(base0, Identity_matrix)
                    base1 = np.kron(base1, self._base_mat)
                elif i == self._control:
                    base0 = np.kron(base0, Base0)
                    base1 = np.kron(base1, Base1)
                else:
                    base0 = np.kron(base0, Identity_matrix)
                    base1 = np.kron(base1, Identity_matrix)
            ret = base0 + base1

        return ret


class X(Base):
    """Class representing an X gate.

    This class inherits from the Base class and represents the X gate.

    Attributes:
        _base_mat (numpy.ndarray): The base matrix representing the X gate.
    """

    def __init__(self, n: int = 1, target: int = 0, control: int = -1) -> None:
        """
        Initialize an X gate.

        Args:
            n (int, optional): The number of qubits (default is 1).
            target (int, optional): The target qubit index (default is 0).
            control (int, optional): The index of the control qubit (
                                     default is -1, which means uncontrolled).
        """
        super().__init__(n, target, control)
        self._base_mat = np.array([[0, 1], [1, 0]], dtype=np.complex128)
        self._mat = self._form_matrix()


class Y(Base):
    """Class representing an Y gate.

    This class inherits from the Base class and represents the Y gate.

    Attributes:
        _base_mat (numpy.ndarray): The base matrix representing the Y gate.
    """

    def __init__(self, n: int = 1, target: int = 0, control: int = -1) -> None:
        """
        Initialize a Y gate.

        Args:
            n (int, optional): The number of qubits (default is 1).
            target (int, optional): The target qubit index (default is 0).
            control (int, optional): The index of the control qubit 
                                     (default is -1, which means uncontrolled).
        """
        super().__init__(n, target, control)
        self._base_mat = np.array([[0, -1.j], [1.j, 0]], dtype=np.complex128)
        self._mat = self._form_matrix()


class Z(Base):
    """Class representing a Z gate.

    This class inherits from the Base class and represents the Z gate.

    Attributes:
        _base_mat (numpy.ndarray): The base matrix representing the Z gate.
    """

    def __init__(self, n: int = 1, target: int = 0, control: int = -1) -> None:
        """
        Initialize a Z gate.

        Args:
            n (int, optional): The number of qubits (default is 1).
            target (int, optional): The target qubit index (default is 0).
            control (int, optional): The index of the control qubit
                                     (default is -1, which means uncontrolled).
        """
        super().__init__(n, target, control)
        self._base_mat = np.array([[1, 0], [0, -1]], dtype=np.complex128)
        self._mat = self._form_matrix()


class H(Base):
    """Class representing an H gate.

    This class inherits from the Base class and represents the H (Hadamard) gate.

    Attributes:
        _base_mat (numpy.ndarray): The base matrix representing the H gate.
    """

    def __init__(self, n: int = 1, target: int = 0, control: int = -1) -> None:
        """
        Initialize an H gate.

        Args:
            n (int, optional): The number of qubits (default is 1).
            target (int, optional): The target qubit index (default is 0).
            control (int, optional): The index of the control qubit
                                     (default is -1, which means uncontrolled).
        """
        super().__init__(n, target, control)
        temp = 1 / math.sqrt(2)
        self._base_mat = np.array([[temp, temp], [temp, -temp]],
                                  dtype=np.complex128)
        self._mat = self._form_matrix()
