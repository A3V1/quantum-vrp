# Quantum Vehicle Routing Problem Solver

A hybrid quantum-classical implementation of the **Vehicle Routing Problem (VRP)** using QUBO-based combinatorial optimization, VQE, QAOA, and IBM ILOG CPLEX. This project solves small-scale VRP instances and compares quantum algorithms against classical methods, including robustness evaluation under simulated quantum noise.

## 🎯 Overview

The Vehicle Routing Problem is an NP-hard combinatorial optimization problem where a fleet of vehicles must deliver goods to customers while minimizing total travel distance. This project demonstrates quantum computing approaches to this problem by:

- **Formulating VRP as QUBO** (Quadratic Unconstrained Binary Optimization)
- **Solving with Quantum Algorithms**: VQE (Variational Quantum Eigensolver) and QAOA (Quantum Approximate Optimization Algorithm)
- **Comparing with Classical Methods**: IBM ILOG CPLEX solver as baseline
- **Evaluating Robustness**: Testing quantum solutions under depolarizing and amplitude damping noise models
- **Visualizing Results**: Route maps and performance comparisons across solvers

## 📋 Table of Contents

- [Features](#features)
- [Project Scope](#project-scope)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Results](#results)
- [Algorithms](#algorithms)
- [Contributing](#contributing)
- [References](#references)

## ✨ Features

- ✅ **Multi-Vehicle VRP Solver**: Handles 2 vehicles with 3-4 customers
- ✅ **Quantum Optimization**: VQE and QAOA implementations via Qiskit
- ✅ **Classical Baseline**: IBM ILOG CPLEX for performance comparison
- ✅ **Noise Simulation**: Depolarizing and amplitude damping noise models
- ✅ **Visualization**: Route plots, cost comparisons, and performance metrics
- ✅ **Reproducible**: Configurable random seeds for experiment repeatability
- ✅ **Result Logging**: JSON-based result storage and analysis

## 📐 Project Scope

### Problem Configuration

- **Depot**: 1 (fixed starting point)
- **Customers**: 2-4 (randomly distributed in 2D space)
- **Vehicles**: 2
- **Distance Metric**: Euclidean distance
- **Coordinates**: Random 2D coordinates

### Constraints

- ✓ Every customer visited exactly once
- ✓ Each customer assigned to exactly one vehicle
- ✓ Vehicles start and return to depot
- ✓ No self-loops
- ✓ Consistent vehicle routes

### Objective

Minimize total route distance across all vehicles.

## 📦 Requirements

- **Python**: >= 3.10
- **Quantum Computing**: Qiskit 2.5.2, Qiskit Aer, Qiskit Algorithms
- **Classical Optimization**: IBM CPLEX 22.2+ (Community Edition)
- **Scientific Stack**: NumPy, SciPy, NetworkX
- **Visualization**: Matplotlib

See `requirements.txt` for complete dependency list.

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd quantum-vrp
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install IBM CPLEX (Required for Classical Baseline)

- Download Community Edition from [IBM CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio)
- Follow installation instructions for your OS
- Verify installation: `python -c "import cplex; print(cplex.Cplex().get_version())"`

## 📂 Project Structure

```
quantum-vrp/
├── README.md                 # This file
├── IMPLEMENTATION.md         # Detailed implementation notes
├── requirements.txt          # Python dependencies
├── main.py                   # Main experiment runner
├── qubo.py                   # QUBO formulation and utilities
├── vqe_solver.py             # VQE quantum solver
├── qaoa_solver.py            # QAOA quantum solver
├── noise.py                  # Noise models (depolarizing, damping)
├── visualization.py          # Plotting and result visualization
├── results/                  # Experiment results (JSON)
│   ├── benchmark_2customers.json
│   ├── cplex_results.json
│   ├── qaoa_results.json
│   ├── vqe_results.json
│   ├── qubo_results.json
│   └── noise_results.json
└── plots/                    # Generated visualizations
    ├── routes/               # Route maps
    └── comparisons/          # Performance comparisons
```

## 🚀 Usage

### Run Complete Experiments

```bash
python main.py
```

This executes:

1. 2-customer VRP benchmark (baseline)
2. 4-customer VRP experiment
3. Solves each with CPLEX, VQE, and QAOA
4. Generates route visualizations and comparisons
5. Evaluates robustness under noise

### Run Specific Solver

**VQE Solver**:

```python
from vqe_solver import run_vqe
from qubo import create_vrp_qubo

num_customers = 2
Q, offset = create_vrp_qubo(num_customers)
vqe_result = run_vqe(Q, num_customers)
```

**QAOA Solver**:

```python
from qaoa_solver import run_qaoa
from qubo import create_vrp_qubo

num_customers = 2
Q, offset = create_vrp_qubo(num_customers)
qaoa_result = run_qaoa(Q, num_customers)
```

**CPLEX Solver**:

```python
from qubo import create_vrp_qubo, solve_with_cplex

num_customers = 2
Q, offset = create_vrp_qubo(num_customers)
cplex_solution = solve_with_cplex(Q, offset)
```

### Custom Experiments

Modify `main.py` to adjust:

- Number of customers: `num_customers = 3`
- Number of vehicles: `num_vehicles = 2`
- Random seed: `seed = 42`
- Problem instances: Add more experiments in `run_vrp_experiment()`

## 📊 Results

Experiment results are stored in `results/` directory:

- **cplex_results.json**: Classical CPLEX solutions
- **vqe_results.json**: VQE quantum solutions
- **qaoa_results.json**: QAOA quantum solutions
- **noise_results.json**: Solutions with noise simulation
- **qubo_results.json**: QUBO formulation parameters

Generated visualizations in `plots/`:

- **routes/**: Individual route maps for each solver
- **comparisons/**: Side-by-side cost and feasibility comparisons

## 🧮 Algorithms

### QUBO Formulation

The VRP is transformed into a QUBO problem using binary variables encoding vehicle-customer assignments.

**Decision Variables**:
$$x_{i,v} \in \{0,1\}$$

- 1 if customer $i$ assigned to vehicle $v$
- 0 otherwise

**Objective**: Minimize total distance with penalties for constraint violations.

### VQE (Variational Quantum Eigensolver)

- Uses parameterized quantum circuits (ansatz)
- Classical optimizer adjusts parameters to minimize energy
- Suitable for NISQ (Noisy Intermediate-Scale Quantum) devices

### QAOA (Quantum Approximate Optimization Algorithm)

- Applies alternating parameterized operations (mixers/problems)
- Tunable circuit depth via $p$ parameter
- Effective for combinatorial problems on quantum hardware

### Classical CPLEX

- Exact optimization solver using branch-and-cut
- Provides optimal or near-optimal reference solutions
- Benchmark for quantum algorithm performance

## 📈 Noise Models

The project evaluates quantum solution robustness under:

1. **Depolarizing Noise**: Random bit-flip errors
2. **Amplitude Damping**: Energy dissipation (T1 relaxation)

Configurable noise parameters in `noise.py`:

- Error rates: 0.1% to 5%
- Channel: single-qubit or two-qubit gates

## ⚙️ Configuration

Edit `main.py` to customize experiments:

```python
def run_vrp_experiment(num_customers, num_vehicles=2, seed=42, depot=0):
    """
    Parameters:
    - num_customers: Problem size (2-4 recommended)
    - num_vehicles: Fleet size (typically 2)
    - seed: Random seed for reproducibility
    - depot: Depot node index (default 0)
    """
```

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Larger problem instances (5+ customers)
- Additional quantum algorithms (VQC, etc.)
- Advanced noise models
- Performance optimizations
- Documentation enhancements

## 📚 References

1. Kochol, P. (2004). "Polynomial-time approximation algorithms for vehicle routing problems."
2. Goemans, M. X., & Williamson, D. P. (1995). "Improved approximation algorithms for max cut and max satisfiability problems using SDP rounding."
3. Qiskit Documentation: https://qiskit.org/documentation/
4. IBM ILOG CPLEX: https://www.ibm.com/products/ilog-cplex-optimization-studio

---

**Note**: This is an educational/experimental implementation demonstrating quantum computing applications to combinatorial optimization. It does not claim quantum advantage over classical methods on current hardware.
