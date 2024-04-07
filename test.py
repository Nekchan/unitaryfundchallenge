# import mitiq as mi
from mitiq.zne.scaling import fold_gates_at_random, fold_global
# import numpy as np
# import cmath as c
from math import sqrt, pi
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

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

# qc = QuantumCircuit(q, c)
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