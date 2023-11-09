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
    def __init__(self, qubit)->None:
        """Initialize the quantum circuit
        Args:
            qubit (qubit.qubit.Qubit): qubit object.
        Attributes:
            gate_list (list): 2D list of gates from quantum circuit. All row vectors(for each rows in circuit) maintains the same length.
            qubit (qubit.qubit.Qubit): qubit object of quantum circuit.        
        """                
        self._qubit = qubit
        self._gate_list = [[] for _ in range(self.qubit._n)]    
        
    def add_gate(self, row, col)->None:
        """Add gate object to circuit_matrix.
        Args:
            row (int): row of gates at the circuit position(index starts from 0).
            col (int): col of gates at the circuit position(index starts from 0).
        """
        if len(self._gate_list) < row:

        try:
            self._gate_list[row][col]
    
    def add_circuit_row(self)->None:
        """Add new row at the bottom of the circuit(which represents the highest digit). Redefine the qubit object with increased qubit number. Initial qubit value is maintained.
        """    

    def change_qubit_value(self, v)->None:
        """change the qubit value.
        Args:
            v (int): decimal value that circuit qubit will be initialized.
        """

    def del_gate(self, row, col)->None:
        """Delete the selected gate in circuit. 
        Args:
            row (int): row of gates at the circuit position(index starts from 0).
            col (int): col of gates at the circuit position(index starts from 0).
        """

    def del_circuit_row(self, row)->None:
        """delete the seleceted circuit row. Redefined the qubit object with decreased qubit number. Inital qubit value is also modified.
        Args:
            row (int): row of gates at the circuit position(index starts from 0).
        """

    def calculate_qubit_state(self, col)->None:
        """calculate the selected qubit state of the circuit. 
        Args:
            col (int): Column of desired circuit position. Function calculates the qubit states that has been operated up to the selected gate(index starts from 0).
        """
        
    def calculate_entanglement(self)->list:
        """for each quantum state, find the qubit set that are entangled. 
        Returns:
            2 dimension list that contains the list of entangled qubits pygame objs.
        """

        