class Circuit():
    def __init__(self):
        self.circuit_matrix = []
        
    def add_gate(self, row, col):
        """Add gate object to circuit_matrix
        row: row of gates circuit position.
        col: col of gates circuit position.
        """
    
    def add_circuit_row(self):
        """Add new circuit row. Initalized qubit will be inside of new added list.
        """

    def change_qubit_value(self, v):
        """change the qubit value.
        v: decimal value that circuit qubit will be initialized.
        """

    def del_gate(self, row, col):
        """Deleted the selected gate in circuit.
        """

    def del_circuit_row(self, row):
        """delete the seleceted circuit row
        """

    def calculate_qubit_state(self, col):
        """calculate the selected qubit of the circuit. 
        col: col of circuit position. calculate the qubit states that passes the gates under selected col.
        """
        
    def calculate_entanglement(self)->list:
        """for each quantum state, find the qubit set that are entangled state. 
        
        returns the 2 dimension list that contains the list of entangled qubits pygame objs.        
        """

        