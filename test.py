# import mitiq as mi
from mitiq.zne.scaling import fold_gates_at_random, fold_global
# import numpy as np
# import cmath as c
from math import sqrt, pi
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import CRZGate

import cirq


"""
plik testowy
nie usowajcie w nim nic
wszystko komentujcie

"""

# Starting_state = "000"
# Initial_state = Statevector.from_label(Starting_state)
# noise=0.005

# q = QuantumRegister(5,'q')
# c = ClassicalRegister(5,'c')
# alfa=pi/2
# qc = QuantumCircuit(2)
# # qc.crz(alfa, 0, 1)
# CRZGate(alfa, qc[0],qc[1])
# qc=fold_gates_at_random(qc, scale_factor=3)
# print(qc)
qubits=cirq.LineQubits.range(1)
qc=cirq.Circuit()
qc.append(cirq.H(qubits[0]))
qc.append(cirq.H(qubits[0]))
print(qc)

# def qft_circuit(num_qubits):
#     qubits = cirq.LineQubit.range(num_qubits)
#     circuit = cirq.Circuit()

#     for target_qubit in range(num_qubits):
#         circuit.append(cirq.H(qubits[target_qubit]))
#         for control_qubit in range(target_qubit + 1, num_qubits):
#             angle = pi / (2 ** (control_qubit - target_qubit))
#             circuit.append(cirq.CZ(qubits[control_qubit], qubits[target_qubit])**(angle))
    
#     circuit.append([cirq.SWAP(qubits[i], qubits[num_qubits - i - 1]) for i in range(num_qubits // 2)])

#     return circuit

# num_qubits = 5
# qft_circuit_example = qft_circuit(num_qubits)
# print("Quantum Fourier Transform Circuit for", num_qubits, "qubits:")
# print(qft_circuit_example)
# # print(len(qc), len(q))

# n=len(q)
# for i in range(n):
#     qc.h(q[i])
    
#     j=1
#     while n>i+j:
#         theta=pi/(2**j)
#         qc.crx(theta, q[i], q[i+j])
#         j+=1
# # print(n//2)
# for k in range(n//2):
#     # print(k, n-k-1)
#     qc.swap(q[k], q[n-k-1])
# print(qc)
# qc.h(q[0])
# qc.crx(pi/2, q[0],q[1])
# print(qc)
# fqc=fold_gates_at_random(qc, scale_factor=2)

# print(fqc)
# qc.draw("mpl")

# print(mitiq.__version__)