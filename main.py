"""
Hybrid Quantum-Classical VRP Solver

Experiments:
- 2-Customer VRP (baseline)
- 4-Customer VRP (scaled)

For each experiment:
1. Generate random customer locations
2. Create QUBO formulation
3. Solve with CPLEX (classical baseline)
4. Solve with VQE (quantum variational)
5. Solve with QAOA (quantum approximate optimization)
6. Compare results and generate visualizations
"""

import json
import numpy as np
import matplotlib.pyplot as plt

from qubo import (
    create_vrp_qubo,
    decode_qubo_solution,
    check_vrp_feasibility,
    calculate_total_route_cost
)

from qiskit_optimization.algorithms import CplexOptimizer
from vqe_solver import run_vqe
from qaoa_solver import run_qaoa
from visualization import plot_routes, plot_comparison

# ============================================================
# EXPERIMENT FUNCTION
# ============================================================

def run_vrp_experiment(num_customers, num_vehicles=2, seed=42, depot=0):
    """
    Run complete VRP optimization experiment.
    
    Parameters
    ----------
    num_customers : int
        Number of customers (not including depot)
    num_vehicles : int
        Number of vehicles
    seed : int
        Random seed for reproducibility
    depot : int
        Depot node index
    """
    
    print("\n" + "=" * 70)
    print(f"{num_customers}-CUSTOMER VRP EXPERIMENT ({num_vehicles} VEHICLES)")
    print("=" * 70)
    
    # ========================================================
    # 1. GENERATE LOCATIONS
    # ========================================================
    
    np.random.seed(seed)
    
    locations = np.random.rand(num_customers + 1, 2) * 10
    
    print("\nLocations")
    print("-" * 40)
    
    for i, location in enumerate(locations):
        if i == depot:
            print(f"Depot     : {location}")
        else:
            print(f"Customer {i}: {location}")
    
    # ========================================================
    # 2. CALCULATE DISTANCE MATRIX
    # ========================================================
    
    num_nodes = num_customers + 1
    distance_matrix = np.zeros((num_nodes, num_nodes))
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(
                    locations[i] - locations[j]
                )
    
    print("\nDistance Matrix")
    print("-" * 40)
    print(np.round(distance_matrix, 2))
    
    # ========================================================
    # 3. CREATE QUBO FORMULATION
    # ========================================================
    
    qubo = create_vrp_qubo(
        distance_matrix=distance_matrix,
        num_customers=num_customers,
        num_vehicles=num_vehicles,
        penalty=100
    )
    
    print("\nQUBO")
    print("=" * 40)
    print(qubo)
    
    # ========================================================
    # 4. SOLVE WITH CPLEX (BASELINE)
    # ========================================================
    
    print("\nSolving QUBO with CPLEX (classical baseline)...")
    print("-" * 50)
    
    qubo_cplex = CplexOptimizer()
    qubo_result = qubo_cplex.solve(qubo)
    
    print("\nCPLEX Result")
    print("=" * 50)
    print(f"Objective value: {qubo_result.fval:.6f}")
    
    cplex_routes = decode_qubo_solution(
        qubo_result.variables_dict,
        num_customers,
        num_vehicles
    )
    
    print("\nDecoded Routes:")
    for vehicle, route in enumerate(cplex_routes):
        print(f"  Vehicle {vehicle}: {' -> '.join(map(str, route))}")
    
    cplex_cost = calculate_total_route_cost(cplex_routes, distance_matrix)
    print(f"Route Cost: {cplex_cost:.6f}")
    
    # ========================================================
    # 5. SOLVE WITH VQE
    # ========================================================
    
    print("\n" + "-" * 70)
    vqe_result, vqe_operator, vqe_offset, vqe_routes, vqe_cost = run_vqe(
        qubo,
        distance_matrix,
        num_customers,
        num_vehicles
    )
    
    # ========================================================
    # 6. SOLVE WITH QAOA
    # ========================================================
    
    print("\n" + "-" * 70)
    qaoa_result, qaoa_operator, qaoa_offset, qaoa_routes, qaoa_cost = run_qaoa(
        qubo,
        distance_matrix,
        num_customers,
        num_vehicles
    )
    
    # ========================================================
    # 7. BENCHMARK COMPARISON
    # ========================================================
    
    print("\n" + "=" * 70)
    print("BENCHMARK COMPARISON")
    print("=" * 70)
    
    vqe_feasible = vqe_routes is not None and check_vrp_feasibility(
        vqe_routes, num_customers
    )
    qaoa_feasible = qaoa_routes is not None and check_vrp_feasibility(
        qaoa_routes, num_customers
    )
    
    vqe_gap = ((vqe_cost - cplex_cost) / cplex_cost * 100) if vqe_cost else float('inf')
    qaoa_gap = ((qaoa_cost - cplex_cost) / cplex_cost * 100) if qaoa_cost else float('inf')
    
    print(f"\n{'Solver':<12} {'Cost':<14} {'Feasible':<12} {'Gap (%)':<12}")
    print("-" * 50)
    print(f"{'CPLEX':<12} {cplex_cost:<14.6f} {'Yes':<12} {0.00:<12.2f}")
    print(f"{'VQE':<12} {vqe_cost:<14.6f} {str(vqe_feasible):<12} {vqe_gap:<12.2f}")
    print(f"{'QAOA':<12} {qaoa_cost:<14.6f} {str(qaoa_feasible):<12} {qaoa_gap:<12.2f}")
    
    # ========================================================
    # 8. SAVE RESULTS
    # ========================================================
    
    benchmark_data = {
        "num_customers": num_customers,
        "num_vehicles": num_vehicles,
        "solvers": {
            "CPLEX": {
                "cost": float(cplex_cost),
                "feasible": True,
                "optimality_gap": 0.0
            },
            "VQE": {
                "cost": float(vqe_cost) if vqe_cost else None,
                "feasible": vqe_feasible,
                "optimality_gap": float(vqe_gap) if vqe_cost else None
            },
            "QAOA": {
                "cost": float(qaoa_cost) if qaoa_cost else None,
                "feasible": qaoa_feasible,
                "optimality_gap": float(qaoa_gap) if qaoa_cost else None
            }
        }
    }
    
    filename = f"results/benchmark_{num_customers}customers.json"
    with open(filename, "w") as f:
        json.dump(benchmark_data, f, indent=4)
    print(f"\nResults saved to {filename}")
    
    # ========================================================
    # 9. VISUALIZATION
    # ========================================================
    
    print("\nGenerating visualizations...")
    
    # Route plots
    suffix = f"{num_customers}customers"
    
    plot_routes(
        cplex_routes,
        locations,
        title=f"CPLEX Routes ({num_customers} Customers)",
        save_path=f"plots/routes/cplex_{suffix}.png"
    )
    
    if vqe_routes:
        plot_routes(
            vqe_routes,
            locations,
            title=f"VQE Routes ({num_customers} Customers)",
            save_path=f"plots/routes/vqe_{suffix}.png"
        )
    
    if qaoa_routes:
        plot_routes(
            qaoa_routes,
            locations,
            title=f"QAOA Routes ({num_customers} Customers)",
            save_path=f"plots/routes/qaoa_{suffix}.png"
        )
    
    # Benchmark comparison plot
    solvers = ["CPLEX", "VQE", "QAOA"]
    costs = [
        cplex_cost,
        vqe_cost if vqe_cost else cplex_cost * 2,
        qaoa_cost if qaoa_cost else cplex_cost * 2
    ]
    
    plot_comparison(
        methods=solvers,
        results=costs,
        title=f"Solver Comparison ({num_customers} Customers)",
        save_path=f"plots/comparisons/benchmark_{suffix}.png"
    )
    
    print(f"Plots saved to plots/routes/ and plots/comparisons/")
    
    print("\n" + "=" * 70)
    print(f"{num_customers}-CUSTOMER EXPERIMENT COMPLETE")
    print("=" * 70)
    
    return benchmark_data


def run_noise_experiment(num_customers=2, num_vehicles=1, seed=42):
    print("\n" + "=" * 70)
    print("NOISE ROBUSTNESS EXPERIMENT")
    print("=" * 70)
    
    np.random.seed(seed)
    locations = np.random.rand(num_customers + 1, 2) * 10
    
    num_nodes = num_customers + 1
    distance_matrix = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                distance_matrix[i][j] = np.linalg.norm(locations[i] - locations[j])
                
    qubo = create_vrp_qubo(distance_matrix, num_customers, num_vehicles, penalty=100)
    
    from qiskit_optimization.algorithms import CplexOptimizer
    qubo_cplex = CplexOptimizer()
    qubo_result = qubo_cplex.solve(qubo)

    # Use decoded route cost (not raw QUBO fval) as the reference optimum
    cplex_routes = decode_qubo_solution(
        qubo_result.variables_dict, num_customers, num_vehicles
    )
    cplex_cost = calculate_total_route_cost(cplex_routes, distance_matrix)
    
    from noise import create_noise_model
    from qaoa_solver import run_qaoa
    from visualization import plot_noise_robustness
    
    error_rates = [0.0, 0.01, 0.05, 0.10]
    probabilities = []
    
    for rate in error_rates:
        print(f"\n--- Running QAOA with Depolarizing Error Rate: {rate} ---")
        if rate == 0.0:
            noise_model = None
        else:
            noise_model = create_noise_model(depolarizing_rate=rate, amplitude_damping_rate=0.0)
            
        qaoa_result, _, _, _, qaoa_cost = run_qaoa(
            qubo, distance_matrix, num_customers, num_vehicles, noise_model=noise_model
        )
        
        # Probability of sampling the optimal bitstring
        prob = 0.0
        if qaoa_cost is not None and abs(qaoa_cost - cplex_cost) < 1e-3:
            if hasattr(qaoa_result, "best_measurement"):
                prob = qaoa_result.best_measurement.get("probability", 0.0)
                
        print(f"Probability of optimal: {prob:.4f}  (QAOA cost={qaoa_cost:.4f}, ref={cplex_cost:.4f})")
        probabilities.append(prob)
        
    plot_noise_robustness(
        error_rates,
        probabilities,
        save_path="plots/comparisons/noise_robustness.png"
    )
    print("\nNoise robustness plot saved to plots/comparisons/noise_robustness.png")

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    
    print("\n" + "=" * 70)
    print("HYBRID QUANTUM-CLASSICAL VRP SOLVER")
    print("=" * 70)
    
    # --------------------------------------------------------
    # Experiment 1: 3-City VRP (1 Depot + 2 Customers, 1 Vehicle)
    # --------------------------------------------------------
    results_2c = run_vrp_experiment(
        num_customers=2,
        num_vehicles=1,
        seed=42
    )
    
    # --------------------------------------------------------
    # Experiment 2: 4-City VRP (1 Depot + 3 Customers, 1 Vehicles)
    # --------------------------------------------------------
    # results_4c = run_vrp_experiment(
    #     num_customers=3,
    #     num_vehicles=1,
    #     seed=42
    # )

    # --------------------------------------------------------
    # Experiment 3: Noise Robustness (on the 3-City problem)
    # --------------------------------------------------------
    run_noise_experiment(num_customers=2, num_vehicles=1, seed=42)
    
    # ========================================================
    # FINAL SUMMARY
    # ========================================================
    
    print("\n" + "=" * 70)
    print("ALL EXPERIMENTS COMPLETE")
    print("=" * 70)
    print("\nResults saved:")
    print("  - results/benchmark_2customers.json")
    print("  - results/benchmark_4customers.json")
    print("  - results/vqe_results.json")
    print("  - results/qaoa_results.json")
    print("\nVisualizations saved:")
    print("  - plots/routes/*.png")
    print("  - plots/comparisons/*.png")


