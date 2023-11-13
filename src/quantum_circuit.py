"""
Defines circuit class that saves the quantum circuit structure that user made.

Author: Chanyu Moon
Email: moonchanyu@gmail.com
Website: https://github.com/tlemsl/Entanglement_visualizer

Classes:
    Circuit: Represents the quantum circuit.
"""

import qubit.qubit as qb

class QuantumCircuit:
    """A class that represents the quantum circuit constructed user using GUI.
    Args:
        qubit (qubit.qubit.Qubit): qubit object.
    Raises:

    Attributes:
        gate_list (list): 2D list of gates from quantum circuit. All row vectors(for each rows in circuit) maintains the same length.
        qubit (qubit.qubit.Qubit): qubit object of quantum circuit.                        
    """
    def __init__(self, qubit, gate_num)->None:
        """Initialize the quantum circuit
        Args:
            qubit (qubit.qubit.Qubit): qubit object.
            gate_num (int): number of gates.
        Attributes:
            gate_list (list): 2D list of gates from quantum circuit. All row vectors(for each rows in circuit) maintains the same length.
            qubit (qubit.qubit.Qubit): qubit object of quantum circuit.        
        """                
        self._qubit = qubit
        self._gate_list = [[None for _ in range(gate_num)] for _ in range(self._qubit._n)]
        
    def add_gate(self, row, col, gate)->None:
        """Add gate object to circuit_matrix.
        Args:
            row (int): row of gates at the circuit position(index starts from 0).
            col (int): col of gates at the circuit position(index starts from 0).
            gate (qubit.gates.X,Y,Z,H): gate object that will be added.
        """
        if (row >= len(self._gate_list))&(row<0):
            raise IndexError(f"row not in [0,{len(self._gate_list)-1}]")
        
        if (col >= len(self._gate_list[0]))&(col<0):
            raise IndexError(f"column not in [0, {len(self._gate_list[0])-1}]")

        self._gate_list[row][col] = gate
    
    def add_circuit_row(self)->None:
        """Add new row at the bottom of the circuit(which represents the highest digit). Redefine the qubit object with increased qubit number. Initial qubit value is maintained.
        """    
        gate_num = len(self._gate_list[0])  
        self._gate_list.append([None for _ in range(gate_num)])

        qubit_num = len(self.gate_list)     
        qubit_mat = self._qubit.mat() 
        qubit_value = qubit_mat.index(1)
        self._qubit = qb.Qubit(qubit_num+1, qubit_value)

    def change_qubit_value(self, v)->None:
        """change the qubit value.
        Args:
            v (int): decimal value that circuit qubit will be initialized.
        """
        n = self._qubit._n
        data = np.zeros((2**n, 1), dtype=np.complex128)
        data[v, 0] = 1
        self._qubit.mat(data)

    def del_gate(self, row, col)->None:
        """Delete the selected gate in circuit. 
        Args:
            row (int): row of gates at the circuit position(index starts from 0).
            col (int): col of gates at the circuit position(index starts from 0).
        """
        if (row >= len(self._gate_list) )&(row<0):
            raise IndexError(f"row not in [0,{len(self._gate_list)-1}]")

        if (col >= len(self._gate_list[0])):
            raise IndexError(f"column not in [0, {len(self._gate_list[0])-1}]")

        self._gate_list[row][col] = None            

    def del_circuit_row(self)->None:
        """delete the bottom row.
        """
        if (row >= len(self._gate_list) )&(row<0):
            raise IndexError(f"row not in [0,{len(self._gate_list)-1}]")           
        del self._gate_list[-1]

    def calculate_qubit_state(self)->None:
        """calculate the qubit state of the circuit. 
        Returns: list of the calcuated quantum state by each columns.         
        """
        quantum_states = []
        for col_i in range(len(self._gate_list[0])): # repeat by col 
            G = None
            for row_i in range(len(self._gate_list)): # repeat by row                
                print(self._gate_list[row_i][col_i])
                if (self._gate_list[row_i][col_i] == None):
                    continue

                if (row_i == 0):
                    G = self._gate_list[row_i][col_i]
                elif (row_i >= 1):
                    G = G * self._gate_list[row_i][col_i]
            print(f"G:\n{G}")
            # TODO: 중간에 비어있는 경우 어떻게 처리할 지 생각. idea) 사이 비워 두면 그냥 Identity matrix 처리. 
            if (G == None):
                if col_i == 0:
                    quantum_states.append(self._qubit)
                elif col_i >= 1:
                    quantum_states.append(quantum_states[col_i-1])
            else:
                if col_i == 0:
                    quantum_states.append(G * self._qubit)
                elif col_i >= 1:
                    quantum_states.append(G * quantum_states[col_i-1])
        return quantum_states
                                
    def calculate_entanglement(self)->list:
        """for each quantum state, find the qubit set that are entangled. 
        Returns:
            2 dimension list that contains the list of entangled qubits pygame objs.
        """
        pass    
        