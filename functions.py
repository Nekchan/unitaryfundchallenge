from math import pi
import cirq
from cirq import Circuit, LineQubit

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

def QFT(q:LineQubit, n:int)->Circuit:
    qc = Circuit()
    for i in range(n):
        qc.append(cirq.H(q[i]))
        for j in range(i + 1, n):
            alfa = pi / (2 ** (j - i))
            qc.append(cirq.CZ(q[j], q[i])**(alfa))
    qc.append([cirq.SWAP(q[i], q[n - i - 1]) for i in range(n // 2)])
    return qc
