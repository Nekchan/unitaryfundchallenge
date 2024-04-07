
from functions import QFT
from mitiq.zne.scaling import fold_gates_at_random, fold_global
import cirq
from cirq import Circuit, LineQubit

if __name__=="__main__":

    n=5
    q = cirq.LineQubit.range(n)
    qc=QFT(q,n)
    qc2=fold_gates_at_random(qc, scale_factor=1)
    print(qc2)

