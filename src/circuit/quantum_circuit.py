"""
Defines the QuantumCircuit class to represent the structure of a user-created 
quantum circuit.

Author: Chanyu Moon
Email: moonchanyu@gmail.com
Website: https://github.com/tlemsl/Entanglement_visualizer

Classes:
    QuantumCircuit: Represents a user-created quantum circuit.
"""

import numpy as np
import qubit.qubit as qb


class QuantumCircuit:
    """A class representing a quantum circuit.

    Attributes:
        gate_list (list): 2D list of gates. Each row vector has the same length.
        qubit (qubit.qubit.Qubit): Qubit object of the circuit.

    Args:
        qubit (qubit.qubit.Qubit): Qubit object.
        gate_num (int): Number of gates.
    """

    def __init__(self, qubit, gate_num):
        """Initializes the quantum circuit.

        Args:
            qubit (qubit.qubit.Qubit): Qubit object.
            gate_num (int): Number of gates.
        """
        self._qubit = qubit
        self._gate_list = [[None for _ in range(gate_num)]
                           for _ in range(self._qubit._n)]

    def add_gate(self, row, col, gate):
        """Adds a gate to the circuit.

        Args:
            row (int): Row index for the gate (0-indexed).
            col (int): Column index for the gate (0-indexed).
            gate (qubit.gates.X, Y, Z, H): Gate object to be added.

        Raises:
            IndexError: If row or column index is out of range.
        """
        if not (0 <= row < len(self._gate_list)):
            raise IndexError(f"row not in [0, {len(self._gate_list)-1}]")
        if not (0 <= col < len(self._gate_list[0])):
            raise IndexError(f"column not in [0, {len(self._gate_list[0])-1}]")

        self._gate_list[row][col] = gate

    def add_circuit_row(self):
        """Adds a new row at the bottom of the circuit and updates the qubit."""
        gate_num = len(self._gate_list[0])
        self._gate_list.append([None for _ in range(gate_num)])

        qubit_num = len(self._gate_list)     
        qubit_mat = self._qubit._mat 
        v = 0
        for i in range(1, len(qubit_mat)+1):
            v += qubit_mat[-i][0].real * (2**(len(qubit_mat)-i))        
        v = int(v)
        
        self._qubit = qb.Qubit(qubit_num, v)        

    def change_qubit_value(self, v):
        """Changes the qubit value.

        Args:
            v (int): New value for the qubit.
        """
        n = self._qubit._n
        data = np.zeros((2**n, 1), dtype=np.complex128)
        data[v, 0] = 1
        self._qubit.mat = data

    def del_gate(self, row, col):
        """Deletes a gate from the circuit.

        Args:
            row (int): Row index of the gate to delete (0-indexed).
            col (int): Column index of the gate to delete (0-indexed).

        Raises:
            IndexError: If row or column index is out of range.
        """
        if not (0 <= row < len(self._gate_list)):
            raise IndexError(f"row not in [0, {len(self._gate_list)-1}]")
        if not (0 <= col < len(self._gate_list[0])):
            raise IndexError(f"column not in [0, {len(self._gate_list[0])-1}]")

        self._gate_list[row][col] = None

    def del_circuit_row(self):
        """Deletes the bottom row of the circuit."""
        self._gate_list.pop()

    def calculate_qubit_state(self):
        """Calculates the qubit state of the circuit.

        Returns:
            list: Quantum states calculated for each column.
        """
        quantum_states = []
        for col_i in range(len(self._gate_list[0])):
            #TODO(@changyu): 중간에 비어있는 경우 어떻게 처리할 지 생각. idea) 사이 비워 두면 
            #그냥 Identity matrix 처리.
            G = None
            for row_i in range(len(self._gate_list)):
                gate = self._gate_list[row_i][col_i]
                if gate is None:
                    continue
                G = gate if G is None else G * gate
            print(col_i)
            print(G)
            if G is None:
                quantum_states.append(self._qubit if col_i ==
                                      0 else quantum_states[col_i - 1])
            else:
                quantum_states.append(G * self._qubit if col_i == 0 else G *
                                      quantum_states[col_i - 1])
            print(quantum_states[-1].mat)
        return quantum_states

    def calculate_entanglement(self):
        """Calculates entangled qubit sets in each quantum state.

        Returns:
            list: 2D list containing lists of entangled qubits.
        """
        pass
