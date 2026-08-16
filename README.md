# quantum-vrp

Quantum Computing-Based Vehicle Routing Problem Solver

A small-scale hybrid quantum-classical implementation of the Vehicle
Routing Problem (VRP) using QUBO-based combinatorial optimization,
VQE, QAOA, and IBM ILOG CPLEX. The project also evaluates
the robustness of quantum solutions under simulated quantum noise and
visualizes route and performance comparisons.

1. Project Overview

The Vehicle Routing Problem (VRP) is an NP-hard combinatorial
optimization problem in which a set of vehicles must deliver goods to a
set of customers while satisfying routing constraints and minimizing a
cost such as total travel distance.

Classical optimization methods such as IBM ILOG CPLEX can solve small
VRP instances efficiently and provide high-quality or optimal reference
solutions. Quantum computing provides an alternative approach in which
the combinatorial optimization problem is transformed into a binary
optimization problem and then mapped to a quantum Hamiltonian.

This project investigates that approach on small-scale VRP instances
with 3--4 customers and one depot, using two quantum optimization
algorithms:

Variational Quantum Eigensolver (VQE)

Quantum Approximate Optimization Algorithm (QAOA)

The quantum solutions are compared against a classical CPLEX solution.
The project is then extended with simulated quantum noise to study how
two different noise sources (depolarizing and amplitude damping) affect
solution quality and the probability of recovering an optimal or feasible route.

Important: This project is intended as a small-scale
experimental/educational implementation. It does not claim quantum
advantage over CPLEX.

2. Project Objectives

The project has five main objectives:

Model a small multi-vehicle VRP using randomly generated customer
locations.

Formulate the routing problem as a QUBO (Quadratic Unconstrained
Binary Optimization) problem.

Solve the QUBO using VQE and QAOA through Qiskit.

Benchmark quantum solutions against IBM ILOG CPLEX.

Evaluate quantum-solution robustness under depolarizing and amplitude
damping noise models and visualize the results.

3. Final Project Scope

Problem size

The core experiments use:

1 depot

3 customers for the first experiment

4 customers for the second experiment

2 vehicles

Randomly generated 2-D customer coordinates

Euclidean distance as the travel-cost metric

The project deliberately keeps the problem small because the number of
binary variables and quantum resources can grow rapidly as the routing
problem becomes larger.

Included constraints

The optimization model enforces:

Every customer is visited exactly once.

Each customer is assigned to a vehicle.

Vehicle routes remain consistent.

Vehicles start from the depot.

Vehicles return to the depot.

Self-loops are prohibited.

Objective

The primary objective is:

[ \min {=tex}\text{Total Route Distance}{=tex} ]

where the total distance is calculated from the selected vehicle routes.

Not included in the core version

To keep the quantum formulation manageable, the initial implementation
does not include:

Vehicle capacity constraints

Customer demand

Time windows

Multiple depots

Dynamic traffic

Real road-network distances

Real-time routing

Fuel consumption

Large-scale instances

These can be considered future extensions.

4.  High-Level Architecture

                         VRP Instance
                    Depot + Customers
                            |
                            v
                   Distance Matrix
                            |
              +-------------+-------------+
              |                           |
              v                           v

    Classical Formulation QUBO Formulation
    | |
    v QuadraticProgram
    CPLEX |
    | +--------+--------+
    | | |
    | v v
    | VQE QAOA
    | | |
    | +--------+--------+
    | |
    +-------------+-------------+
    |
    v
    Route/Cost Comparison
    |
    v
    Qiskit Aer Simulation
    |
    +-------+-------+
    | | |
    v v v
    Ideal Depolarizing Bit Flip
    \ | /
    \ | /
    v v v
    Robustness Analysis
    |
    v
    Visualization/Results

    Note: Two noise models are simulated: depolarizing noise and
    amplitude damping noise.

5.  Technology Stack

Technology Role

Python Main programming language

Qiskit Quantum computing framework

Qiskit Optimization Mathematical optimization and QUBO
modeling

Qiskit Algorithms VQE and QAOA

Qiskit Aer Quantum circuit simulation and
noise modeling

IBM ILOG CPLEX Classical optimization benchmark

NumPy Numerical calculations and distance
matrices

NetworkX Route/graph representation and
visualization

Matplotlib Route and performance plots

6. Why Each Technology Is Used

Python

Python is used to build the complete experiment.

It handles:

Generating customer locations

Calculating distances

Building optimization models

Calling Qiskit algorithms

Calling CPLEX

Processing solutions

Calculating metrics

Creating visualizations

Qiskit

Qiskit is the quantum-computing framework used to construct and simulate
the quantum portion of the project.

It provides the tools required to:

Construct quantum circuits

Represent optimization problems

Run VQE

Run QAOA

Simulate quantum circuits

Work with quantum noise

Potentially execute circuits on IBM Quantum hardware

The conceptual role of Qiskit is:

Python
|
+-- Qiskit
|
+-- QUBO
+-- VQE
+-- QAOA
+-- Aer simulation
+-- Noise simulation

QUBO

QUBO stands for:

Quadratic Unconstrained Binary Optimization

It expresses an optimization problem using binary variables:

[ x_i \in {=tex}{0,1} ]

The general form is:

[ \min{=tex}_x x^T Qx ]

For this project, the QUBO combines:

The routing cost.

Penalty terms for violating VRP constraints.

Conceptually:

[ H_{\text{QUBO}{=tex}} = H_{\text{distance}{=tex}} + A
H_{\text{constraints}{=tex}} ]

where (A) is a penalty coefficient.

The purpose of the QUBO is to transform the original constrained VRP
into a form that can be mapped to a quantum optimization problem.

7. VRP Mathematical Formulation

A binary decision variable represents whether a particular routing
decision is selected.

Depending on the implementation, variables can encode:

Customer/vehicle assignments

Vehicle transitions between locations

Position-based city assignments

For example:

[ x\_{i,j,k} =

\begin{cases}
1 & \text{if vehicle } k \text{ travels from } i \text{ to } j\\
0 & \text{otherwise}
\end{cases}

]

The objective can be represented as:

[ \min{=tex} \sum{=tex}_{k} \sum{=tex}i \sum{=tex}j
d{ij}x{i,j,k} ]

where (d\_{ij}) is the distance between locations (i) and (j).

Constraints are converted into penalty terms so that invalid solutions
have a higher QUBO energy.

8. Classical Baseline --- IBM ILOG CPLEX

IBM ILOG CPLEX is used as the classical optimization benchmark.

The classical workflow is:

VRP
|
v
Mathematical Optimization Model
|
v
CPLEX
|
v
Reference Route
|
v
Reference Cost

For small instances, CPLEX can provide an optimal or very strong
reference solution.

This reference allows us to evaluate the quantum algorithms.

For example:

Solver Route Cost Feasible

CPLEX 18.42 Yes
VQE 18.42 Yes
QAOA 19.01 Yes

The values above are illustrative only; the actual project will generate
the results.

9. Quantum Algorithm --- VQE

What is VQE?

The Variational Quantum Eigensolver (VQE) is a hybrid
quantum-classical algorithm.

The goal is to find a low-energy state of a Hamiltonian.

The process is:

Initial Parameters
|
v
Parameterized Quantum Circuit
|
v
Measure Expectation Value
|
v
Classical Optimizer
|
v
Update Parameters
|
+------> Repeat

The optimization continues until the expectation value is minimized.

For this project, the QUBO is transformed into a Hamiltonian and VQE
attempts to find a low-energy state corresponding to a good routing
solution.

VQE Ansatz

A fixed variational ansatz such as TwoLocal is used.

Conceptually:

Rotation Gates
|
Entangling Gates
|
Rotation Gates
|
Entangling Gates
|
...

The ansatz contains trainable parameters.

The initial implementation can use:

Ry and Rz rotation gates

CZ entanglement

reps = 1

An optional experiment can investigate reps = 2.

VQE Classical Optimizer

The VQE loop uses a classical optimizer to update the circuit
parameters.

Possible optimizers include:

SPSA

COBYLA

SPSA is particularly relevant for noisy quantum optimization because it
estimates parameter gradients using a small number of function
evaluations.

10. Quantum Algorithm --- QAOA

What is QAOA?

The Quantum Approximate Optimization Algorithm (QAOA) is a hybrid
quantum-classical algorithm specifically designed for combinatorial
optimization.

It uses two main components:

Cost Hamiltonian

Represents the optimization objective.

Mixer Hamiltonian

Allows the quantum state to explore different candidate configurations.

Conceptually:

Initial Quantum State
|
v
Cost Hamiltonian
|
v
Mixer Hamiltonian
|
v
Cost Hamiltonian
|
v
Mixer Hamiltonian
|
v
Measurement

The number of repeated cost/mixer layers is controlled by the QAOA depth
(p).

The initial experiment uses:

p = 1

and can optionally compare:

p = 2

11. VQE vs QAOA

Feature VQE QAOA

Type Hybrid Hybrid
quantum-classical quantum-classical

Main purpose Variational Combinatorial
ground-state estimation optimization

Ansatz General parameterized Structured cost/mixer
ansatz ansatz

Parameters Circuit parameters Cost/mixer parameters

Classical optimizer Required Required

The project uses both to compare two different variational approaches to
the same VRP/QUBO formulation.

12. Quantum Solution Decoding

A quantum optimizer does not directly return:

Depot -> Customer 1 -> Customer 3 -> Depot

Instead, it returns a binary configuration representing the values of
the decision variables.

The project therefore needs a decoding stage:

Quantum Measurement
|
v
Binary Bit String
|
v
Decision Variables
|
v
Vehicle Assignments
|
v
Customer Sequence
|
v
Vehicle Routes

The decoded routes are then checked for feasibility and their total
distance is calculated.

13. Quantum Simulation

The project initially runs on a simulator rather than requiring physical
quantum hardware.

Qiskit Aer is used to:

Simulate quantum circuits

Run repeated measurements/shots

Build custom noise models

Compare ideal and noisy execution

This makes the experiments reproducible on a local machine.

14. Noise Analysis

Quantum computers are affected by errors.

The project evaluates how noise changes the quality of the quantum
optimization result.

The basic workflow is:

 QAOA/VQE Circuit
 |
 +---------> Ideal Simulation
 |
 +---------> Noisy Simulation
 |
 +---------+---------+
 | |
 v v
 Depolarizing Amplitude
 Noise Damping

15. Noise Models

Two noise models are implemented using Qiskit Aer.

15.1 Depolarizing Noise

Depolarizing noise represents a general class of quantum errors that can
move a qubit state toward a completely mixed state. It is applied to
single-qubit gates (rx, ry, rz) and two-qubit gates (cx, cz).

The experiment varies the depolarizing rate and measures how the
optimal-solution probability changes.

15.2 Amplitude Damping

Amplitude damping models energy dissipation, i.e. spontaneous emission
from excited to ground state. It is applied at the measurement stage and
represents a realistic physical error mechanism where a qubit loses
energy to its environment.

This affects the reliability of the final measurement and therefore
changes how often the correct route is recovered.

16. Noise Experiment

For each noise level, the QAOA circuit is run and the optimal-solution
probability is recorded.

Error rates tested:

0.00 (ideal)
0.01
0.05
0.10

For each level, run multiple shots and calculate:

[ P_{\text{optimal}{=tex}} =
\frac{\text{Number of optimal-solution measurements}}{=tex}
{\text{Total number of shots}{=tex}} ]

This provides a quantitative measure of robustness.

17. Evaluation Metrics

The project evaluates the following metrics.

17.1 Route Cost

Total travel distance:

[ C = \sum {=tex}d_{ij} ]

Lower is better.

17.2 Feasibility

Checks whether the decoded solution satisfies all VRP constraints.

A solution is considered feasible only if:

Every customer is visited exactly once.

Vehicle routes are valid.

Depot constraints are satisfied.

No prohibited transitions occur.

17.3 Optimality Gap

Quantum solution cost can be compared with the CPLEX reference:

[ \text{Optimality Gap}{=tex} =
\frac{C_{\text{quantum}}-C_{\text{CPLEX}}}{=tex}
{C_{\text{CPLEX}{=tex}}} \times100{=tex} ]

A value near zero indicates that the quantum solution is close to the
CPLEX reference.

17.4 Runtime

Measure:

CPLEX runtime

VQE runtime

QAOA runtime

Runtime is reported for comparison, but the project does not claim
quantum speedup from these small simulations.

17.5 Optimal-Solution Probability

For shot-based quantum simulations:

[ P_{\text{optimal}{=tex}} =
\frac{\text{optimal bitstring counts}}{=tex}
{\text{total shots}{=tex}} ]

This is especially useful in the noise experiments.

18. Experimental Plan

Experiment 1 --- 3-Customer VRP

Problem:

1 Depot
3 Customers
2 Vehicles

Run:

CPLEX
VQE
QAOA

Compare:

Route

Cost

Feasibility

Runtime

Optimality gap

Experiment 2 --- 4-Customer VRP

Problem:

1 Depot
4 Customers
2 Vehicles

Run:

CPLEX
VQE
QAOA

Repeat the same evaluation.

Experiment 3 --- VQE Optimizer Comparison

Optional experiment:

VQE + SPSA
VQE + COBYLA

Compare route cost and convergence.

Experiment 4 --- QAOA Depth

Optional experiment:

QAOA p=1
QAOA p=2

Compare solution quality and circuit complexity.

Experiment 5 --- Noise Robustness

Use QAOA under:

Ideal (rate = 0.00)
Depolarizing + Amplitude Damping (rates = 0.01, 0.05, 0.10)

Measure optimal-solution probability as noise increases.

19. Visualizations

The project produces three major categories of visualizations.

19.1 Customer Map

Displays:

Depot

Customer locations

Problem geometry

19.2 Optimized Routes

Displays routes produced by:

CPLEX

VQE

QAOA

The depot is clearly marked and vehicle routes are shown separately.

19.3 Performance Comparison

Possible plots include:

Route cost by solver

Optimality gap

Runtime

VQE optimizer comparison

QAOA depth comparison

Noise vs optimal-solution probability

20. Proposed Repository Structure

quantum-vrp/
│
├── main.py
├── requirements.txt
├── README.md
│
├── vrp/
│ ├── **init**.py
│ ├── problem.py
│ ├── classical.py
│ ├── quantum.py
│ ├── noise.py
│ ├── evaluation.py
│ └── visualization.py
│
└── results/
├── routes/
├── solver_comparison/
└── noise_analysis/

During initial development, all functionality can be kept in main.py.
Once the implementation works, it can be separated into modules.

21. Expected Workflow

The complete implementation follows:

1. Generate depot and customers
   |
   v
2. Calculate pairwise distances
   |
   v
3. Create classical VRP model
   |
   v
4. Solve using CPLEX
   |
   v
5. Create QUBO formulation
   |
   v
6. Convert QUBO to quantum Hamiltonian
   |
   +----------------+
   | |
   v v
   VQE QAOA
   | |
   +-------+--------+
   |
   v
7. Decode binary solution into routes
   |
   v
8. Validate feasibility
   |
   v
9. Calculate route cost
   |
   v
10. Compare with CPLEX
    |
    v
11. Run ideal quantum simulation
    |
    v
12. Add quantum noise
    |
    v
13. Measure robustness
    |
    v
14. Generate visualizations

15. Installation

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the required packages:

pip install qiskit qiskit-aer qiskit-optimization qiskit-algorithms
pip install cplex numpy matplotlib networkx

Save the environment:

pip freeze > requirements.txt

23. Development Phases

Phase 1 --- Problem Setup

Generate locations.

Generate distance matrix.

Plot customers.

Define vehicles.

Phase 2 --- Classical Baseline

Create VRP optimization model.

Solve with CPLEX.

Decode route.

Validate feasibility.

Calculate route cost.

Phase 3 --- QUBO

Define binary variables.

Add objective.

Add penalty terms.

Create QuadraticProgram.

Validate the QUBO formulation.

Phase 4 --- VQE

Convert optimization problem to the required quantum representation.

Define fixed ansatz.

Configure classical optimizer.

Run VQE.

Decode solution.

Phase 5 --- QAOA

Configure QAOA.

Select classical optimizer.

Run QAOA.

Decode solution.

Phase 6 --- Benchmarking

Compare:

CPLEX
VQE
QAOA

using:

Cost

Feasibility

Optimality gap

Runtime

Phase 7 --- Noise

Build Aer noise models.

Run noisy simulations.

Vary noise probabilities.

Calculate optimal-solution probability.

Plot robustness.

Phase 8 --- Documentation

Clean code.

Save experiment results.

Create visualizations.

Document methodology.

Document limitations.

Add reproducibility instructions.

24. Important Scientific Limitations

This project is intentionally small.

1. No quantum advantage claim

A 3--4 customer problem is far too small to demonstrate practical
quantum advantage.

The purpose is to investigate:

Quantum optimization formulation

VQE/QAOA behavior

Solution quality

Hybrid optimization

Noise sensitivity

2. Classical solvers are very strong

CPLEX is expected to perform extremely well on these small instances.

Therefore, a quantum solution being slower than CPLEX is not a failure.

The meaningful comparison is whether the quantum method can recover
good/optimal routes and how its performance changes with noise.

3. Simulation is not a real quantum processor

Ideal and noisy Aer simulations do not perfectly reproduce every aspect
of a physical quantum computer.

If hardware execution is added later, it should be treated as an
additional experiment.

4. Small QUBO size

Quantum resources grow quickly with the number of customers and routing
variables.

This is why the initial project focuses on 3--4 customers.

25. Expected Final Results

The final project should produce:

Route results

CPLEX → Route + Cost
VQE → Route + Cost
QAOA → Route + Cost

Benchmark results

Solver
Route Cost
Feasibility
Optimality Gap
Runtime

Noise results

Noise Model (Depolarizing + Amplitude Damping)
Noise Level (0.00, 0.01, 0.05, 0.10)
Optimal-Solution Probability
Route Quality

Visual results

Customer Map
CPLEX Route
VQE Route
QAOA Route
Solver Comparison
Noise Robustness

26. Project Deliverables

The completed repository should contain:

Working Python implementation

VRP generator

Distance matrix calculation

CPLEX solver

QUBO formulation

VQE implementation

QAOA implementation

Quantum solution decoder

Feasibility checker

Noise simulation

Performance evaluation

Route visualizations

Benchmark plots

Noise robustness plots

requirements.txt

Detailed README

27. Resume Mapping

The final project is designed to directly support the following resume
description:

Developed a hybrid quantum-classical VRP solver for 3--4 cities
using VQE/QAOA, optimizing delivery routes through QUBO-based
combinatorial optimization. Compared quantum solutions with IBM CPLEX
and evaluated robustness under different quantum noise models,
visualizing optimized routes and performance.

Claim → Implementation

Resume claim Project implementation

Hybrid quantum-classical Quantum algorithms + classical optimizers
VRP Multi-vehicle routing with depot/customers
3--4 cities 3- and 4-customer experiments
VQE Variational quantum optimization
QAOA Combinatorial quantum optimization
QUBO Binary quadratic formulation of VRP
IBM CPLEX Classical benchmark
Noise models Depolarizing + amplitude damping via Qiskit Aer
Robustness Optimal-solution probability and cost under noise
Optimized routes Route decoding and visualization
Performance Cost, gap, feasibility, runtime and robustness plots

28. Interview Explanation

A concise explanation of the project is:

"I implemented a small-scale multi-vehicle VRP with three and four
customers. I first generated customer locations and calculated their
pairwise Euclidean distances. I formulated the routing constraints and
distance objective as a QUBO and used IBM CPLEX to obtain a classical
reference solution. I then mapped the same optimization problem to
quantum form and solved it using VQE and QAOA in Qiskit. I decoded the
resulting binary solutions into vehicle routes and compared them with
CPLEX using route cost, feasibility, runtime and optimality gap.
Finally, I used Qiskit Aer to introduce depolarizing and amplitude
damping noise and measured how the probability of recovering the
optimal solution changed as noise increased."

29. Core Concept in One Diagram

                          PYTHON
                            |
              +-------------+-------------+
              |                           |
              v                           v
         VRP Generation             Visualization
              |
              v

    Distance Matrix
    |
    +-----+-----+
    | |
    v v
    CPLEX QUBO
    | |
    | +----+----+
    | | |
    | v v
    | VQE QAOA
    | | |
    | +----+----+
    | |
    +-----------+
    |
    v
    Route Comparison
    |
    v
    Qiskit Aer
    |
    +------+------+
    | |
    v v
    Ideal Depol. +
             Amp. Damping
    \ /
    \ /
    v v
    Robustness
    Analysis
    |
    v
    Final Results

30. Final Project Goal

The goal is not:

"Build a quantum computer that beats CPLEX."

The goal is:

"Build and experimentally evaluate a hybrid quantum-classical
approach to a small VRP, compare VQE/QAOA against a classical CPLEX
baseline, and study how quantum noise affects the quality and
reliability of the resulting solutions."

That is the scope we should implement. It is technically defensible,
directly aligned with your resume bullet, and close to the reference
project you are trying to replicate.
