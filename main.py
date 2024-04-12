import numpy as np
from functions import QFT, noisy_sampler, not_noisy_sampler, execute_ddd
from mitiq.zne.scaling import fold_gates_at_random, fold_global
import cirq
from cirq import Circuit, LineQubit
from mitiq import zne, benchmarks, ddd, MeasurementResult, Executor, Observable, PauliString
import matplotlib.pyplot as plt


if __name__=="__main__":

    qreg1 = cirq.LineQubit.range(3)
    qreg2 = cirq.LineQubit.range(3,6) #tworze 2 registery, 1 do liczby a, 2 do liczby b
    #po algorytmie na registerze 1 jest liczba a, a na drugim liczba a+b (mod 8)

    circuit = cirq.Circuit(
        cirq.X.on(qreg2[0]),
        cirq.X.on(qreg1[1])) #tutaj przygotowanie stanu na wejscie tylko zeby zrobic z kilku zer jedynki
        #|100>|001>

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


    circuit_with_m = circuit.copy()
    circuit_with_m.append(cirq.measure(*circuit.all_qubits()))

    out_number = Observable(PauliString("IIIZII", coeff=-2.0), PauliString("IIIIZI", coeff=-1.0), PauliString("IIIIIZ", coeff=-0.5))
    #nie pytajcie czemu tak wyzej xD, to jest zamienianie qubitow odczytanych na liczbe zeby bylo latwiej potem analizowanc
    #zamienia np odczytane 0011 na 3

    executor = Executor(noisy_sampler)
    ideal_executor = Executor(not_noisy_sampler)
    results = executor.evaluate(circuit, out_number)[0].real + 3.5 #srednia z odczytanych liczb, idealnie a+b
    ideal_results = ideal_executor.evaluate(circuit, out_number)[0].real + 3.5 #niezaszumiona jw

    ### DDD

    # rule_for_ddd = ddd.rules.xx 
    # rule_for_ddd = ddd.rules.yy 
    rule_for_ddd = ddd.rules.xyxy

    mitigated_result = ddd.execute_with_ddd(
        circuit=circuit,
        executor=execute_ddd,
        rule=rule_for_ddd
    )
    circuit_ddd=ddd.insert_ddd_sequences(circuit, rule_for_ddd)

    # print(circuit_ddd) #printowanie cirqutu robionego

    ### ZNE
    linear_fac = zne.inference.PolyFactory(scale_factors=[1,2,3,4], order=1)

    zne_value = zne.execute_with_zne(circuit, executor, out_number, factory=linear_fac).real + 3.5  # Noisy quantum computer + Mitiq
    zne_value_with_ddd = zne.execute_with_zne(circuit_ddd, executor, out_number, factory=linear_fac).real + 3.5  # Noisy quantum computer + Mitiq
    #srednia z odczytanych liczb z zastosowaniem zne, ekstrapolacja f. kwadratowa



    print("Unmitigated result: " + str(results))
    print("Ideal result: " + str(ideal_results))
    print(ideal_executor.quantum_results) #tutaj mozna sobie zobaczyc nie srednie tylko jawnie jaka kombinacja ile razy zostala zmierzona

    for num in linear_fac.get_expectation_values():
        print(num.real+3.5)


    print(f"Mitigated resoult without DDD: {zne_value}")
    print(f"Mitigated resoult with DDD: {zne_value_with_ddd}")
    print(f"Error with mitigation (DDD): {abs(ideal_results - zne_value_with_ddd) :.3}")



