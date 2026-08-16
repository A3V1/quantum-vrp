import numpy as np

from qiskit_optimization import QuadraticProgram


def create_vrp_qubo(
    distance_matrix,
    num_customers,
    num_vehicles,
    penalty=100.0
):
    """
    Create a QUBO representation of a small VRP.

    Binary variable:

        x_i_j_k = 1

    means vehicle k travels directly from
    location i to location j.

    Location 0 = depot.
    Locations 1..N = customers.
    """

    num_nodes = num_customers + 1
    depot = 0

    qp = QuadraticProgram(
        name="VRP_QUBO"
    )

    # =========================================================
    # 1. CREATE BINARY VARIABLES
    # =========================================================

    for vehicle in range(num_vehicles):

        for i in range(num_nodes):

            for j in range(num_nodes):

                if i != j:

                    qp.binary_var(
                        name=f"x_{i}_{j}_{vehicle}"
                    )

    # =========================================================
    # 2. OBJECTIVE: MINIMIZE TRAVEL DISTANCE
    # =========================================================

    objective = {}

    for vehicle in range(num_vehicles):

        for i in range(num_nodes):

            for j in range(num_nodes):

                if i != j:

                    variable = f"x_{i}_{j}_{vehicle}"

                    objective[variable] = (
                        distance_matrix[i][j]
                    )

    # =========================================================
    # 3. CUSTOMER VISITED EXACTLY ONCE
    #
    # For every customer:
    #
    # sum(incoming edges) = 1
    #
    # In QUBO:
    #
    # penalty * (sum(x) - 1)^2
    # =========================================================

    for customer in range(1, num_nodes):

        variables = []

        for vehicle in range(num_vehicles):

            for i in range(num_nodes):

                if i != customer:

                    variables.append(
                        f"x_{i}_{customer}_{vehicle}"
                    )

        # Add penalty for:
        # sum(x) != 1

        for variable in variables:

            objective[variable] = (
                objective.get(variable, 0)
                - penalty
            )

        for a in range(len(variables)):

            for b in range(a + 1, len(variables)):

                key = (
                    variables[a],
                    variables[b]
                )

                objective[key] = (
                    objective.get(key, 0)
                    + 2 * penalty
                )

    # =========================================================
    # 4. FLOW CONSERVATION
    #
    # For every customer and vehicle:
    #
    # incoming = outgoing
    #
    # We enforce:
    #
    # penalty * (incoming - outgoing)^2
    #
    # =========================================================

    for vehicle in range(num_vehicles):

        for customer in range(1, num_nodes):

            incoming = [
                f"x_{i}_{customer}_{vehicle}"
                for i in range(num_nodes)
                if i != customer
            ]

            outgoing = [
                f"x_{customer}_{j}_{vehicle}"
                for j in range(num_nodes)
                if j != customer
            ]

            # Linear terms from:
            #
            # (incoming - outgoing)^2

            for variable in incoming:

                objective[variable] = (
                    objective.get(variable, 0)
                    + penalty
                )

            for variable in outgoing:

                objective[variable] = (
                    objective.get(variable, 0)
                    + penalty
                )

            # Incoming-incoming quadratic terms

            for a in range(len(incoming)):

                for b in range(a + 1, len(incoming)):

                    key = (
                        incoming[a],
                        incoming[b]
                    )

                    objective[key] = (
                        objective.get(key, 0)
                        + 2 * penalty
                    )

            # Outgoing-outgoing quadratic terms

            for a in range(len(outgoing)):

                for b in range(a + 1, len(outgoing)):

                    key = (
                        outgoing[a],
                        outgoing[b]
                    )

                    objective[key] = (
                        objective.get(key, 0)
                        + 2 * penalty
                    )

            # Incoming-outgoing terms have -2 coefficient

            for incoming_variable in incoming:

                for outgoing_variable in outgoing:

                    key = (
                        incoming_variable,
                        outgoing_variable
                    )

                    objective[key] = (
                        objective.get(key, 0)
                        - 2 * penalty
                    )

    # =========================================================
    # 5. EACH VEHICLE LEAVES DEPOT ONCE
    #
    # penalty * (sum(x) - 1)^2
    # =========================================================

    for vehicle in range(num_vehicles):

        variables = [
            f"x_{depot}_{customer}_{vehicle}"
            for customer in range(1, num_nodes)
        ]

        for variable in variables:

            objective[variable] = (
                objective.get(variable, 0)
                - penalty
            )

        for a in range(len(variables)):

            for b in range(a + 1, len(variables)):

                key = (
                    variables[a],
                    variables[b]
                )

                objective[key] = (
                    objective.get(key, 0)
                    + 2 * penalty
                )

    # =========================================================
    # 6. EACH VEHICLE RETURNS TO DEPOT ONCE
    #
    # penalty * (sum(x) - 1)^2
    # =========================================================

    for vehicle in range(num_vehicles):

        variables = [
            f"x_{customer}_{depot}_{vehicle}"
            for customer in range(1, num_nodes)
        ]

        for variable in variables:

            objective[variable] = (
                objective.get(variable, 0)
                - penalty
            )

        for a in range(len(variables)):

            for b in range(a + 1, len(variables)):

                key = (
                    variables[a],
                    variables[b]
                )

                objective[key] = (
                    objective.get(key, 0)
                    + 2 * penalty
                )

    # =========================================================
    # 7. BUILD QUBO
    # =========================================================

    linear = {}
    quadratic = {}

    # Separate linear and quadratic terms

    for key, coefficient in objective.items():

        if isinstance(key, str):

            linear[key] = coefficient

        else:

            quadratic[key] = coefficient

    qp.minimize(
        linear=linear,
        quadratic=quadratic
    )

    return qp

def decode_qubo_solution(
    variables_dict,
    num_customers,
    num_vehicles,
    depot=0
):
    """
    Convert selected QUBO binary variables into
    vehicle routes.
    """

    num_nodes = num_customers + 1

    selected_edges = []

    # Find selected edges
    for variable, value in variables_dict.items():

        if value > 0.5 and variable.startswith("x_"):

            parts = variable.split("_")

            i = int(parts[1])
            j = int(parts[2])
            vehicle = int(parts[3])

            selected_edges.append(
                (vehicle, i, j)
            )

    routes = []

    # Build route for each vehicle
    for vehicle in range(num_vehicles):

        vehicle_edges = [
            (i, j)
            for v, i, j in selected_edges
            if v == vehicle
        ]

        route = [depot]
        current = depot

        visited = set()

        while True:

            next_nodes = [
                j
                for i, j in vehicle_edges
                if i == current
            ]

            if not next_nodes:
                break

            next_node = next_nodes[0]

            route.append(next_node)

            if next_node == depot:
                break

            # Prevent infinite loops
            if next_node in visited:
                break

            visited.add(next_node)

            current = next_node

        routes.append(route)

    return routes

def check_vrp_feasibility(
    routes,
    num_customers,
    depot=0
):
    """
    Check whether every customer is visited
    exactly once and every route starts/ends
    at the depot.
    """

    customers = []

    for route in routes:

        # Route must start at depot
        if route[0] != depot:
            return False

        # Route must end at depot
        if route[-1] != depot:
            return False

        # Collect customers
        for node in route:

            if node != depot:
                customers.append(node)

    # Every customer must appear exactly once
    expected = set(
        range(1, num_customers + 1)
    )

    actual = set(customers)

    if actual != expected:
        return False

    if len(customers) != len(set(customers)):
        return False

    return True

def calculate_total_route_cost(
    routes,
    distance_matrix
):
    """
    Calculate the actual travel distance
    of decoded routes.
    """

    total_cost = 0.0

    for route in routes:

        for i in range(len(route) - 1):

            current = route[i]
            next_node = route[i + 1]

            total_cost += distance_matrix[
                current
            ][
                next_node
            ]

    return total_cost