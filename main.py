
from functions import QFT
from mitiq.zne.scaling import fold_gates_at_random, fold_global
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

if __name__=="__main__":
    """
    tak zwykle się pisze w pliku głównym żeby ludzie którzy przeglądają jakiś projekt
    mogli rozpoznać któryjest główny.
    dzieki temu program załaduje się tylko gdy będzie bezpośrednio uruchomiony a nie wywołany przez funkcje zewnetrzna.
    """
    q = QuantumRegister(5,'q')
    c = ClassicalRegister(5,'c')
    qc = QuantumCircuit(q, c)
    noise=0.005

    qc=QFT(qc, q, c)

    print(qc)
