import cirq
import mitiq
from mitiq import zne, benchmarks, ddd, MeasurementResult, Executor, Observable, PauliString, pt
from cirq import Circuit, LineQubit
import numpy as np
from numpy import pi
from mitiq.zne.inference import LinearFactory, PolyFactory
from qiskit import QuantumCircuit, transpile, Aer, IBMQ
from mitiq.interface import mitiq_qiskit
import matplotlib.pyplot as plt

def QFT(q:LineQubit, n:int)->Circuit:
    qc = Circuit()
    for i in range(n):
        qc.append(cirq.H(q[i]))
        for j in range(i + 1, n):
            alfa = 1 / (2 ** (j - i))
            qc.append(cirq.CZ(q[j], q[i])**(alfa))
    #qc.append([cirq.SWAP(q[i], q[n - i - 1]) for i in range(n // 2)])
    return qc

def noisy_sampler(circuit, noise_level=0.01, shots=1000) ->MeasurementResult: #tutaj jest symulacja zaszumniona
    noisy_circuit = circuit.with_noise(cirq.depolarize(p=noise_level))
    noisy_circuit = noisy_circuit.with_noise(cirq.amplitude_damp(gamma=0.01))
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(noisy_circuit, repetitions=shots)
    bitstrings = np.column_stack(list(result.measurements.values()))
    qubit_indices = tuple(
        int(q[2:-1])
        for k in result.measurements.keys()
        for q in k.split(",")
    )
    return MeasurementResult(bitstrings, qubit_indices)

def not_noisy_sampler(circuit, shots=1000) ->MeasurementResult: #tutaj jest symulacja niezaszumiona, zwraca ilosc odczytanych kombinacji kubitow
    """Returns Tr[ρ |0⟩⟨0|] where ρ is the state prepared by the circuit
    with depolarizing noise."""
    #noisy_circuit = circuit.with_noise(cirq.depolarize(p=0.000001))
    simulator = cirq.DensityMatrixSimulator()
    result = simulator.run(circuit, repetitions=shots)
    bitstrings = np.column_stack(list(result.measurements.values()))
    qubit_indices = tuple(
        int(q[2:-1])
        for k in result.measurements.keys()
        for q in k.split(",")
    )
    return MeasurementResult(bitstrings, qubit_indices)

qreg1 = cirq.LineQubit.range(3)
qreg2 = cirq.LineQubit.range(3,6) #tworze 2 registery, 1 do liczby a, 2 do liczby b
#po algorytmie na registerze 1 jest liczba a, a na drugim liczba a+b (mod 8)

circuit = cirq.Circuit(
    cirq.X.on(qreg2[2]),
    cirq.X.on(qreg1[0])) #tutaj przygotowanie stanu na wejscie tylko zeby zrobic z kilku zer jedynki

adder = cirq.Circuit(
    cirq.CZ(qreg1[0], qreg2[0])**1.0,
    cirq.CZ(qreg1[1], qreg2[0])**0.5,
    cirq.CZ(qreg1[2], qreg2[0])**0.25,

    cirq.CZ(qreg1[1], qreg2[1])**1.0,
    cirq.CZ(qreg1[2], qreg2[1])**0.5,

    cirq.CZ(qreg1[2], qreg2[2])**1.0) # algorytm dodawania

circuit.append(QFT(qreg2, 3))
circuit.append(adder)
circuit.append(QFT(qreg2, 3)**-1)

print(circuit) #printowanie cirqutu robionego

out_number = Observable(PauliString("IIIZII", coeff=-2.0), PauliString("IIIIZI", coeff=-1.0), PauliString("IIIIIZ", coeff=-0.5))
#nie pytajcie czemu tak wyzej xD, to jest zamienianie qubitow odczytanych na liczbe zeby bylo latwiej potem analizowanc
#zamienia np odczytane 0011 na 3

executor = Executor(noisy_sampler)
ideal_executor = Executor(not_noisy_sampler)
results = executor.evaluate(circuit, out_number)[0].real + 3.5 #srednia z odczytanych liczb, idealnie a+b
ideal_results = ideal_executor.evaluate(circuit, out_number)[0].real + 3.5 #niezaszumiona jw

linear_fac = zne.inference.PolyFactory(scale_factors=[1,2,3,4], order=1)
linear_fac_pt = zne.inference.PolyFactory(scale_factors=[1,2,3,4], order=1)

circuit_with_pt = mitiq.pt.pt.pauli_twirl_circuit(circuit, num_circuits=1)[0]
print(circuit_with_pt)

zne_value = zne.execute_with_zne(circuit, executor, out_number, factory=linear_fac).real + 3.5  # Noisy quantum computer + Mitiq
pt_zne_value = zne.execute_with_zne(circuit_with_pt, executor, out_number, factory=linear_fac_pt).real + 3.5
pt_value = executor.evaluate(circuit_with_pt, out_number)[0].real + 3.5
#srednia z odczytanych liczb z zastosowaniem zne, ekstrapolacja f. kwadratowa

print("Unmitigated result: " + str(results))
print("Ideal result: " + str(ideal_results))
print(executor.quantum_results) #tutaj mozna sobie zobaczyc nie srednie tylko jawnie jaka kombinacja ile razy zostala zmierzona
#print(*executor.executed_circuits)

for num in linear_fac.get_expectation_values():
    print(num.real+3.5)

print("\n")
for num in linear_fac_pt.get_expectation_values():
    print(num.real+3.5)


print("Mitigated result: " + str(zne_value))
print("ZNE+PT: " + str(pt_zne_value))
print("PT: " + str(pt_value))
