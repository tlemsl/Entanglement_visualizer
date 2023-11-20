import circuit.quantum_circuit as qc
import qubit.gates as qg
import qubit.qubit as qb

print("2 qubit example")
qubit = qb.Qubit(2, 0)
circuit = qc.QuantumCircuit(qubit, 2)
circuit.add_gate(0, 0, qg.X(2, 0))
circuit.add_gate(1, 1, qg.H(2, 1))

print(f"circiut:\ndarray{circuit._gate_list}")

states = circuit.calculate_qubit_state()

print(f"states:\n{states}")
print(states[0])
print(states[1])

print("3 qubit example")

qubit3 = qb.Qubit(3, 0)
print(len(qubit3))
circuit3 = qc.QuantumCircuit(qubit3, 4)

circuit3.add_gate(0, 0, qg.H(3, 0))
circuit3.add_gate(0, 1, qg.X(3, 0))
circuit3.add_gate(1, 0, qg.X(3, 1))
circuit3.add_gate(2, 0, qg.X(3, 2))

print(f"circiut:\ndarray{circuit3._gate_list}")

states = circuit3.calculate_qubit_state()

print(f"states:\n{states}")
for i in range(len(states)):
    print(len(states[i]))
    print(states[i])

print("4 qubit example")

qubit4 = qb.Qubit(4, 0)
print(len(qubit4))
circuit4 = qc.QuantumCircuit(qubit4, 4)

circuit4.add_gate(0, 0, qg.H(4, 0))
circuit4.add_gate(0, 1, qg.X(4, 0))
circuit4.add_gate(1, 0, qg.X(4, 1))
circuit4.add_gate(2, 0, qg.X(4, 2))

print(f"circiut:\ndarray{circuit4._gate_list}")

states = circuit4.calculate_qubit_state()

print(f"states:\n{states}")
for i in range(len(states)):
    print(len(states[i]))
    print(states[i])
