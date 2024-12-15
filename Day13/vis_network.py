import numpy as np
import os


def load_data_from_file(file_path):
    """
    Load network data from a file into numpy arrays for demand, A, B, and C matrices.

    Parameters:
        file_path (str): Path to the input data file.

    Returns:
        tuple: (demand, A, B, C)
            demand: numpy array of shape (n, 1)
            A, B, C: numpy arrays of shape (n+1, n)
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove comments and empty lines
    lines = [line.strip() for line in lines if line.strip()
             and not line.startswith('#')]

    # Parse number of vertices (n+1)
    num_vertices = int(lines[0])

    # Parse demand vector (n elements)
    demand = np.array([int(lines[i + 1])
                      for i in range(num_vertices - 1)]).reshape(-1, 1)

    # Locate cost components
    a_start = lines.index("1st Variable Cost Component, Aij") + 1
    b_start = lines.index("2nd Variable Cost Component, Bij") + 1
    c_start = lines.index("Fixed Cost Component, Cij") + 1

    # Function to parse cost matrices
    def parse_matrix(start_index, size):
        return np.array([int(lines[start_index + i]) for i in range(size)]).reshape(num_vertices, num_vertices - 1)

    # Parse A, B, and C matrices
    A = parse_matrix(a_start, (num_vertices) * (num_vertices - 1))
    B = parse_matrix(b_start, (num_vertices) * (num_vertices - 1))
    C = parse_matrix(c_start, (num_vertices) * (num_vertices - 1))

    return demand, A, B, C


def generate_graphviz(A, B, C):
    """
    Generate a GraphViz representation of the network based on cost matrices A, B, and C.

    Parameters:
        A, B, C (numpy.ndarray): Cost matrices of shape (n+1, n).

    Returns:
        str: GraphViz description of the network.
    """
    num_vertices = A.shape[0]
    edges = []

    # Adjusting for depot-client edges from the last row
    for j in range(A.shape[1]):
        if not (A[-1, j] == 0 and C[-1, j] == 0 and B[-1, j] == 50000000):
            weight = -A[-1, j] * 5**2 + B[-1, j] * 5 + C[-1, j]
            edges.append((0, j + 1, weight))

    # Client-to-client edges
    for i in range(num_vertices - 1):
        for j in range(A.shape[1]):
            if not (A[i, j] == 0 and C[i, j] == 0 and B[i, j] == 50000000):
                weight = -A[i, j] * 5**2 + B[i, j] * 5 + C[i, j]
                edges.append((i + 1, j + 1, weight))

    graphviz_repr = "digraph G {\n"

    # Define node shapes
    graphviz_repr += "    0 [shape=box, label=\"Depot\"];"
    for i in range(1, num_vertices):
        graphviz_repr += f'    {i} [shape=circle, label="Client {i}"];'

    # Define edges
    for i, j, weight in edges:
        log_weight = np.log10(abs(weight)) if weight != 0 else 0
        graphviz_repr += f'    {i} -> {
            j} [penwidth={max(log_weight / 2, 0.1):.2f}];'

    graphviz_repr += "}"

    return graphviz_repr


def greedy_route(demand, A, B, C):
    """
    Find an approximate route using a greedy algorithm to minimize cost.

    Parameters:
        demand (numpy.ndarray): Demand vector of shape (n, 1).
        A, B, C (numpy.ndarray): Cost matrices of shape (n+1, n).

    Returns:
        tuple: (route, total_cost)
            route: List of visited nodes in order, including depot at start and end.
            total_cost: Total transportation cost of the route.
    """
    num_clients = demand.shape[0]
    remaining_demand = demand.flatten()
    visited = [False] * num_clients

    route = [0]  # Start at the depot
    total_cost = 0
    current_node = 0
    current_weight = remaining_demand.sum()  # Start with full load

    while len(route) <= num_clients:
        min_cost = float('inf')
        next_node = None

        for j in range(1, num_clients + 1):
            if not visited[j - 1]:
                if current_node == 0:  # From depot to client
                    if B[-1, j - 1] == 50000000 and B[j - 1, -1] != 50000000:
                        cost = -A[j - 1, -1] * current_weight**2 + \
                            B[j - 1, -1] * current_weight + C[j - 1, -1]
                    else:
                        cost = -A[-1, j - 1] * current_weight**2 + \
                            B[-1, j - 1] * current_weight + C[-1, j - 1]
                else:  # Between clients
                    if B[current_node - 1, j - 1] == 50000000 and B[j - 1, current_node - 1] != 50000000:
                        cost = -A[j - 1, current_node - 1] * current_weight**2 + B[j - 1,
                                                                                   current_node - 1] * current_weight + C[j - 1, current_node - 1]
                    else:
                        cost = -A[current_node - 1, j - 1] * current_weight**2 + \
                            B[current_node - 1, j - 1] * \
                            current_weight + C[current_node - 1, j - 1]

                if cost < min_cost:
                    min_cost = cost
                    next_node = j

        if next_node is None:
            break

        # Visit the next node
        route.append(next_node)
        total_cost += min_cost
        # Reduce load by demand
        current_weight -= remaining_demand[next_node - 1]
        visited[next_node - 1] = True
        current_node = next_node

    # Return to depot
    if current_node != 0:
        if B[-1, current_node - 1] == 50000000 and B[current_node - 1, -1] != 50000000:
            total_cost += -A[current_node - 1, -1] * current_weight**2 + \
                B[current_node - 1, -1] * \
                current_weight + C[current_node - 1, -1]
        else:
            total_cost += -A[-1, current_node - 1] * current_weight**2 + \
                B[-1, current_node - 1] * \
                current_weight + C[-1, current_node - 1]
        route.append(0)

    return route, total_cost


os.chdir('Day13')
file_path = "instance.txt"
# np.set_printoptions(edgeitems=30)
# np.core.arrayprint._line_width = 1000
np.set_printoptions(edgeitems=10, linewidth=180)

demand, A, B, C = load_data_from_file(file_path)
print("Demand:\n", demand)
print("A:\n", A)
print("B:\n", B)
print("C:\n", C)
graphviz_output = generate_graphviz(A, B, C)
print(graphviz_output)
route, total_cost = greedy_route(demand, A, B, C)
print("Route:", route)
print("Total cost:", total_cost)
