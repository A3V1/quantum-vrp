import json
import time
import numpy as np

from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import RealAmplitudes

from qiskit_algorithms import SamplingVQE
from qiskit_algorithms.optimizers import SPSA

from qiskit_optimization.converters import QuadraticProgramToQubo

from qubo import (
    decode_qubo_solution,
    check_vrp_feasibility,
    calculate_total_route_cost
)


def run_vqe(qubo, distance_matrix, num_customers, num_vehicles):

    print("\nStarting VQE...")
    print("=" * 60)

    start_time = time.time()

    # --------------------------------------------------------
    # QUBO
    # --------------------------------------------------------

    converter = QuadraticProgramToQubo()
    qubo_problem = converter.convert(qubo)

    num_qubits = qubo_problem.get_num_vars()

    print(f"QUBO variables: {num_qubits}")
    print(f"Number of qubits: {num_qubits}")

    # --------------------------------------------------------
    # Ising
    # --------------------------------------------------------

    operator, offset = qubo_problem.to_ising()

    print(f"Ising offset: {offset}")

    # --------------------------------------------------------
    # Sampler
    # --------------------------------------------------------

    sampler = StatevectorSampler(seed=42)

    # --------------------------------------------------------
    # Ansatz
    # --------------------------------------------------------

    ansatz = RealAmplitudes(
        num_qubits=num_qubits,
        reps=1,
        entanglement="linear"
    )

    print(
        f"Ansatz parameters: "
        f"{ansatz.num_parameters}"
    )

    # --------------------------------------------------------
    # Optimizer
    # --------------------------------------------------------

    optimizer = SPSA(
        maxiter=5
    )

    history = []

    # --------------------------------------------------------
    # Callback
    # --------------------------------------------------------

    def callback(
        eval_count,
        parameters,
        mean,
        metadata
    ):

        energy = float(np.real(mean))

        history.append(energy)

        print(
            f"Evaluation {eval_count} | "
            f"Energy: {energy:.6f}"
        )

    # --------------------------------------------------------
    # VQE
    # --------------------------------------------------------

    vqe = SamplingVQE(
        sampler=sampler,
        ansatz=ansatz,
        optimizer=optimizer,
        callback=callback
    )

    vqe.initial_point = np.zeros(
        ansatz.num_parameters
    )

    result = vqe.compute_minimum_eigenvalue(
        operator
    )

    runtime = time.time() - start_time

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    print("\nVQE completed")
    print("=" * 60)

    energy = float(
        np.real(result.eigenvalue)
    )

    print(
        f"VQE energy: {energy:.6f}"
    )

    print(
        f"Runtime: {runtime:.2f} seconds"
    )

    # --------------------------------------------------------
    # Best measurement
    # --------------------------------------------------------

    measurement = None
    decoded_routes = None
    is_feasible = False
    actual_route_cost = None

    if hasattr(result, "best_measurement"):

        measurement = result.best_measurement

        print("\nBest measurement:")
        print(measurement)

        # ====================================================
        # Decode bitstring to routes
        # ====================================================

        # Get variable names from QUBO
        var_names = [v.name for v in qubo_problem.variables]

        # Extract bitstring from measurement
        if isinstance(measurement, dict) and "bitstring" in measurement:
            bitstring = measurement["bitstring"]
        elif hasattr(measurement, "bitstring"):
            bitstring = measurement.bitstring
        else:
            bitstring = measurement  # Fallback if it's already a string

        # Map bitstring to variable assignments
        variables_dict = {
            var_names[i]: float(bitstring[i])
            for i in range(len(bitstring))
        }

        # Decode to routes
        decoded_routes = decode_qubo_solution(
            variables_dict,
            num_customers,
            num_vehicles
        )

        print("\nDecoded VQE routes:")
        for vehicle, route in enumerate(decoded_routes):
            print(
                f"Vehicle {vehicle}: "
                + " -> ".join(map(str, route))
            )

        # Check feasibility
        is_feasible = check_vrp_feasibility(
            decoded_routes,
            num_customers
        )

        print(f"\nFeasible: {is_feasible}")

        # Calculate actual route cost
        actual_route_cost = calculate_total_route_cost(
            decoded_routes,
            distance_matrix
        )

        print(f"Route cost: {actual_route_cost:.6f}")

    # --------------------------------------------------------
    # Save result
    # --------------------------------------------------------

    data = {
        "algorithm": "VQE",
        "num_qubits": num_qubits,
        "num_parameters": ansatz.num_parameters,
        "iterations": 5,
        "energy": energy,
        "offset": float(offset),
        "runtime_seconds": runtime,
        "energy_history": history,
        "best_measurement": str(measurement),
        "decoded_routes": decoded_routes,
        "is_feasible": is_feasible,
        "actual_route_cost": actual_route_cost
    }

    with open(
        "results/vqe_results.json",
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )

    print(
        "\nSaved to "
        "results/vqe_results.json"
    )

    return result, operator, offset, decoded_routes, actual_route_cost