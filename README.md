# Quantum Vehicle Routing Problem Solver

A hybrid quantum-classical implementation of the **Vehicle Routing Problem (VRP)** using **QUBO, VQE, QAOA, and IBM ILOG CPLEX**.

## Overview

The project:

* Converts VRP into a **QUBO** formulation.
* Solves the QUBO using **VQE** and **QAOA**.
* Uses **CPLEX** as a classical baseline.
* Decodes quantum measurements into feasible routes.
* Compares route costs and optimality gaps.
* Evaluates QAOA under simulated **depolarizing noise**.

## Tech Stack

* Python
* Qiskit
* Qiskit Aer
* Qiskit Algorithms
* IBM ILOG CPLEX
* NumPy / SciPy
* Matplotlib

## Problem Setup

The current validated experiment uses:

* 1 depot
* 2 customers
* 1 vehicle
* Euclidean distances
* 6 QUBO variables → 6 qubits

The implementation is designed for small-scale VRP experiments.

## Results

For the validated 2-customer instance:

| Solver | Route Cost | Feasible |   Gap |
| ------ | ---------: | :------: | ----: |
| CPLEX  |  20.523580 |    Yes   | 0.00% |
| VQE    |  20.523580 |    Yes   | 0.00% |
| QAOA   |  20.523580 |    Yes   | 0.00% |

Both VQE and QAOA obtained a feasible solution matching the CPLEX route cost.

### Noise Experiment

QAOA was tested with simulated depolarizing error rates of **0%, 1%, 5%, and 10%** to evaluate the probability of sampling an optimal solution.

## Project Structure

```text
quantum-vrp/
├── main.py
├── qubo.py
├── vqe_solver.py
├── qaoa_solver.py
├── noise.py
├── visualization.py
├── requirements.txt
├── results/
└── plots/
```

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Limitations

This is a **small-scale experimental implementation**. The current results demonstrate that VQE and QAOA can obtain optimal solutions for the tested instance, but they do **not** demonstrate quantum advantage over classical optimization.

## Status

**Working prototype**
