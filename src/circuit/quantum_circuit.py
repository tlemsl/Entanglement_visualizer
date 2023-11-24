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
import qubit.gates as qg
import util.utils as ut


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
        self._shape = self._qubit._n, gate_num

    def __len__(self):
        """return the shape of the gate list
        Returns: 
            set of gate list shape
        """
        return self._shape

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
        qubit_num, gate_num = self._shape        
        self._gate_list.append([None for _ in range(gate_num)]) # add new qubit list.
        self._shape = qubit_num + 1, gate_num # update the circuit shape
        
        v = ut.qubitmat2int(self._qubit._mat)
        
        self._qubit = qb.Qubit(qubit_num+1, v) # update the qubit        

        # update gate format(qubit_num)
        for row, gate_sequence in enumerate(self._gate_list):
            for col, gate in enumerate(gate_sequence):
                if gate != None:
                    if isinstance(gate, qg.H):
                        self._gate_list[row][col] = qg.H(qubit_num+1, gate._target, gate._control)
                    elif isinstance(gate, qg.X):
                        self._gate_list[row][col] = qg.X(qubit_num+1, gate._target, gate._control)
                    elif isinstance(gate, qg.Y):
                        self._gate_list[row][col] = qg.Y(qubit_num+1, gate._target, gate._control)
                    elif isinstance(gate, qg.Z):
                        self._gate_list[row][col] = qg.Z(qubit_num+1, gate._target, gate._control)

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
        
        qubit_num, gate_num = self._shape
        if qubit_num == 0:
            raise IndexError("no rows to delete.")
        self._shape = qubit_num-1, gate_num

        self._gate_list.pop()
                
        v = ut.qubitmat2int(self._qubit._mat)        
        v = int(v%(len(self._qubit._mat)/2))        
        self._qubit = qb.Qubit(qubit_num-1, v)

        for row, gate_sequence in enumerate(self._gate_list):
            for col, gate in enumerate(gate_sequence):
                if gate != None:
                    if isinstance(gate, qg.H):
                        self._gate_list[row][col] = qg.H(qubit_num-1, gate._target, gate._control)
                    elif isinstance(gate, qg.X):
                        self._gate_list[row][col] = qg.X(qubit_num-1, gate._target, gate._control)
                    elif isinstance(gate, qg.Y):
                        self._gate_list[row][col] = qg.Y(qubit_num-1, gate._target, gate._control)
                    elif isinstance(gate, qg.Z):
                        self._gate_list[row][col] = qg.Z(qubit_num-1, gate._target, gate._control)
        

    def calculate_qubit_state(self):
        """Calculates the qubit state of the circuit.

        Returns:
            list: Quantum states calculated for each column.
        """
        quantum_states = []        
        row_num, col_num = self._shape
        n = self._qubit._n        
        for col in range(col_num):    
            G = None # stacking gates column wize(axis 0) by tensor product.                        
            for row in range(row_num):                       
                gate = self._gate_list[row][col]                
                if gate == None:
                    continue
                else:
                    if G == None:
                        G = gate
                    else:
                        G = G*gate
            # apply G to qubit
            if G == None:
                if col == 0:
                    quantum_states.append(self._qubit)
                elif col >= 1:
                    quantum_states.append(quantum_states[col-1])
            else:
                if col==0:
                    quantum_states.append(G*self._qubit)
                elif col >= 1:
                    quantum_states.append(G*quantum_states[col-1])
        return quantum_states

            

    def calculate_entanglement(self):
        """Calculates entangled qubit sets in each quantum state.

        Returns:
            list: 2D list containing lists of entangled qubits.
        """
        pass
