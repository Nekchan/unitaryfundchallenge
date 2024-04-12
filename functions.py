from math import pi
import numpy as np
import cirq
from cirq import Circuit, LineQubit, DensityMatrixSimulator, amplitude_damp
from mitiq import zne, benchmarks, ddd, MeasurementResult, Executor, Observable, PauliString
from mitiq.interface import convert_to_mitiq


def QFT(q:LineQubit, n:int)->Circuit:
    qc = Circuit()
    for i in range(n):
        qc.append(cirq.H(q[i]))
        for j in range(i + 1, n):
            alfa = 1 / (2 ** (j - i))
            qc.append(cirq.CZ(q[j], q[i])**(alfa))
    qc.append([cirq.SWAP(q[i], q[n - i - 1]) for i in range(n // 2)])
    return qc

def noisy_sampler(circuit, noise_level=0.1, shots=1000) ->MeasurementResult: #tutaj jest symulacja zaszumniona
    noisy_circuit = circuit.with_noise(cirq.depolarize(p=noise_level))
    noisy_circuit = noisy_circuit.with_noise(cirq.amplitude_damp(gamma=0.1))
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

def execute_ddd(circuit, noise_level=0.1):
    """Returns Tr[ρ |0⟩⟨0|] where ρ is the state prepared by the circuit
    executed with amplitude damping noise.
    """
    # Replace with code based on your frontend and backend.
    mitiq_circuit, _ = convert_to_mitiq(circuit)
    noisy_circuit = mitiq_circuit.with_noise(amplitude_damp(gamma=noise_level))
    rho = DensityMatrixSimulator().simulate(noisy_circuit).final_density_matrix
    return rho[0, 0].real
