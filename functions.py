from math import pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

"""
szablon pisania funkcji:

def funkcja(a:int, b:float, c:string, d:bool)->int:
    return a

przy argumentach stawiamy dwukropek i typ zmiennej.
po nawiasie i przed dwukropkiem stawiamy strzałkę i typ funkcji jaki zwraca funkcja.
jeśli funkcja nic nie zwraca nie stawiamy strzałki.
są to techniki czysto informacyjne dla programistów - nie mają wpływ na pracę programu.
można napisać A:int a wprowadzić string ale to jest zmyłka dla innych - nie rób tak.
"""

def QFT(qc:QuantumCircuit, q:QuantumRegister, c:ClassicalRegister)->QuantumCircuit:
    n=len(q)
    for i in range(n):
        qc.h(q[i])

        j=1
        while n>i+j:
            theta=pi/(2**j)
            qc.crx(theta, q[i], q[i+j])
            j+=1
    for k in range(n//2):
        qc.swap(q[k], q[n-k-1])
    qc.measure(q,c)
    return qc