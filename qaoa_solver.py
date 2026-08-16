"""
QAOA Solver for VRP

Implements a Quantum Approximate Optimization Algorithm (QAOA)
solver for the Vehicle Routing Problem.
"""

import json
import time
import numpy as np

from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import SPSA

from qubo import (
    decode_qubo_solution,
    check_vrp_feasibility,
    calculate_total_route_cost
)


def run_qaoa(qubo, distance_matrix, num_customers, num_vehicles, noise_model=None):
    """
    Run QAOA to solve the VRP optimization problem.
    
    Parameters
    ----------
    qubo : QuadraticProgram
        The QUBO formulation of the VRP
    distance_matrix : np.ndarray
        Distance matrix for route cost calculation
    num_customers : int
        Number of customers
    num_vehicles : int
        Number of vehicles
    noise_model : NoiseModel, optional
        Optional Qiskit Aer noise model for noisy simulation
        
    Returns
    -------
    result : MinimumEigensolverResult
        The QAOA result
    operator : SparsePauliOp
        The Ising operator
    offset : float
        The Ising offset
    routes : list
        Decoded vehicle routes
    route_cost : float
        Total route cost
    """
    
    print("\nStarting QAOA...")
    print("=" * 60)
    
    start_time = time.time()
    
    # ========================================================
    # Convert QUBO to Ising
    # ========================================================
    
    from qiskit_optimization.converters import QuadraticProgramToQubo
    
    converter = QuadraticProgramToQubo()
    qubo_problem = converter.convert(qubo)
    
    num_qubits = qubo_problem.get_num_vars()
    print(f"Number of qubits: {num_qubits}")
    
    operator, offset = qubo_problem.to_ising()
    print(f"Ising offset: {offset}")
    
    # ========================================================
    # Sampler and optimizer
    # ========================================================
    
    if noise_model is not None:
        from qiskit_aer import AerSimulator
        from qiskit_aer.primitives import SamplerV2 as AerSamplerV2
        from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

        print("Using Noisy Sampler (AerSamplerV2 with noise model)")

        # AerSamplerV2 does NOT auto-transpile circuits — it passes them raw to
        # the Aer backend, which fails with 'unknown instruction: QAOA' because
        # qiskit_algorithms.QAOA wraps its ansatz in a high-level gate.
        # Fix: subclass AerSamplerV2 and transpile every circuit before running.
        backend = AerSimulator(noise_model=noise_model)
        pm = generate_preset_pass_manager(
            optimization_level=0, backend=backend
        )

        class _TranspilingAerSampler(AerSamplerV2):
            """AerSamplerV2 wrapper that transpiles circuits to basis gates first."""
            def __init__(self, pass_manager, **kwargs):
                super().__init__(**kwargs)
                self._pm = pass_manager

            def run(self, pubs, **kwargs):
                transpiled = []
                for pub in pubs:
                    if isinstance(pub, tuple):
                        circ, *rest = pub
                        transpiled.append(
                            (self._pm.run(circ), *rest)
                        )
                    else:
                        transpiled.append(pub)
                return super().run(transpiled, **kwargs)

        sampler = _TranspilingAerSampler(pass_manager=pm, seed=42)
        sampler.options.backend_options['noise_model'] = noise_model
    else:
        sampler = StatevectorSampler(seed=42)
        
    optimizer = SPSA(maxiter=5)
    
    # ========================================================
    # Create QAOA
    # ========================================================
    
    qaoa = QAOA(
        sampler=sampler,
        optimizer=optimizer,
        reps=1
    )
    
    # ========================================================
    # Run QAOA
    # ========================================================
    
    result = qaoa.compute_minimum_eigenvalue(operator)
    
    runtime = time.time() - start_time
    
    # ========================================================
    # Output
    # ========================================================
    
    print("\nQAOA completed")
    print("=" * 60)
    
    energy = float(np.real(result.eigenvalue))
    print(f"QAOA eigenvalue: {energy:.6f}")
    print(f"Runtime: {runtime:.2f} seconds")
    
    # ========================================================
    # Best measurement
    # ========================================================
    
    measurement = None
    decoded_routes = None
    is_feasible = False
    actual_route_cost = None
    
    if hasattr(result, "best_measurement"):
        
        measurement = result.best_measurement
        
        print("\nBest measurement:")
        print(measurement)
        
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
        
        print("\nDecoded QAOA routes:")
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
    
    # ========================================================
    # Save result
    # ========================================================
    
    data = {
        "algorithm": "QAOA",
        "num_qubits": num_qubits,
        "reps": 1,
        "iterations": 10,
        "eigenvalue": energy,
        "offset": float(offset),
        "runtime_seconds": runtime,
        "best_measurement": str(measurement),
        "decoded_routes": decoded_routes,
        "is_feasible": is_feasible,
        "actual_route_cost": actual_route_cost
    }
    
    with open(
        "results/qaoa_results.json",
        "w"
    ) as f:
        json.dump(
            data,
            f,
            indent=4
        )
    
    print(
        "\nSaved to "
        "results/qaoa_results.json"
    )
    
    return result, operator, offset, decoded_routes, actual_route_cost
