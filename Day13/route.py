import os
import re
import time
from collections import defaultdict
from graphviz import Digraph


def load_instance(file_path):
    arcs = defaultdict(dict)
    demand = {}

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Filter and clean lines
    lines = [line.strip()
             for line in lines if not line.startswith('#') and line.strip()]

    # Number of vertices
    n_plus_one = int(lines[0])
    n = n_plus_one - 1

    # Demand for customers
    demands = list(map(int, lines[1:n_plus_one]))
    for i, d in enumerate(demands):
        demand[i] = d

    # Cost components
    total_coefficients = 3  # Aij, Bij, Cij
    coefficient_length = n_plus_one * n

    Aij_lines = lines[n_plus_one:n_plus_one+coefficient_length]
    Bij_lines = lines[n_plus_one +
                      coefficient_length:n_plus_one+2*coefficient_length]
    Cij_lines = lines[n_plus_one+2 *
                      coefficient_length:n_plus_one+3*coefficient_length]

    # Parse coefficients
    Aij = list(map(int, Aij_lines))
    Bij = list(map(int, Bij_lines))
    Cij = list(map(int, Cij_lines))

    # Create arcs dictionary
    for i in range(n_plus_one):
        for j in range(n):
            index = i * n + j
            a, b, c = Aij[index], Bij[index], Cij[index]
            if b != 50000000 and i != j:
                arcs[i][j] = (a, b, c)

    # Add reverse arcs from clients to warehouse
    # Warehouse is the next index after all clients
    warehouse_index = len(demand)
    for client in range(n):
        if warehouse_index in arcs and client in arcs[warehouse_index]:
            arcs[client][warehouse_index] = arcs[warehouse_index][client]

    # Add outgoing arcs for nodes with no outgoing arcs
    new_arcs = []  # Temporary storage for new arcs
    for node in range(n_plus_one):
        if node not in arcs or not arcs[node]:
            for incoming_node in arcs:
                if node in arcs[incoming_node]:
                    new_arcs.append(
                        (node, incoming_node, arcs[incoming_node][node]))

    # Apply new arcs after iteration
    for node, incoming_node, arc_data in new_arcs:
        arcs[node][incoming_node] = arc_data

    return arcs, demand


def visualize_network(arcs, demand):
    dot = Digraph(format='png')

    # Add nodes
    for node in range(len(demand) + 1):
        if node == len(demand):  # Warehouse node
            dot.node(str(node), label="Warehouse", shape="box")
        else:
            label = f"Client {node}\nDemand: {demand.get(node, 0)}"
            dot.node(str(node), label=label, shape="ellipse")

    # Add edges
    for i in arcs:
        for j, (a, b, c) in arcs[i].items():
            cost = -a**2 + b + c
            dot.edge(str(i), str(j), penwidth=str(max(1, cost / 10000)))

    dot.render("network", view=False)


def visualize_solution(arcs, demand, best_route):
    dot = Digraph(format='png')

    # Add nodes
    for node in range(len(demand) + 1):
        if node == len(demand):  # Warehouse node
            dot.node(str(node), label="Warehouse", shape="box")
        else:
            label = f"Client {node}\nDemand: {demand.get(node, 0)}"
            dot.node(str(node), label=label, shape="ellipse")

    # Add edges
    for i in arcs:
        for j, (a, b, c) in arcs[i].items():
            cost = -a**2 + b + c
            if best_route and i in best_route and j in best_route and best_route.index(j) == best_route.index(i) + 1:
                dot.edge(str(i), str(j), penwidth=str(
                    max(1, cost / 10000)), color="green")
            else:
                dot.edge(str(i), str(j), penwidth=str(max(1, cost / 10000)))

    dot.render("network_solution", view=True)


def calculate_cost(route, arcs, demand):
    total_cost = 0
    weight = sum(demand.values())
    for i in range(len(route) - 1):
        start, end = route[i], route[i + 1]
        a, b, c = arcs[start][end]
        segment_cost = -a * weight**2 + b * weight + c
        total_cost += segment_cost
        weight -= demand.get(end, 0)  # Reduce weight after delivery
    return total_cost


def find_best_route(arcs, demand, time_limit=1800, improvement_limit=300):
    start_time = time.time()
    last_improvement_time = start_time

    # Warehouse index is explicitly set based on demand size
    warehouse = len(demand)
    clients = list(demand.keys())

    best_route = None
    best_cost = float('inf')

    def branch_and_bound(route, visited, current_cost, remaining_weight):
        nonlocal best_route, best_cost, last_improvement_time

        # Check time limits
        if time.time() - start_time > time_limit:
            return
        if time.time() - last_improvement_time > improvement_limit:
            return

        # If all clients are visited and back to the warehouse
        if route[-1] == warehouse and visited == set(clients + [warehouse]):
            if current_cost < best_cost:
                best_cost = current_cost
                best_route = route[:]
                last_improvement_time = time.time()
                print(f"New best route at {
                      last_improvement_time - start_time:.2f}s: {best_route} with cost {best_cost}")
            return

        # Branch out to all possible next nodes
        for next_node in arcs[route[-1]].keys():  # Use only accessible nodes
            # Skip return to warehouse until all clients are visited
            if next_node == warehouse and visited != set(clients + [warehouse]):
                continue
            if next_node != warehouse and next_node in visited:
                continue  # Skip already visited clients
            a, b, c = arcs[route[-1]][next_node]
            segment_cost = -a * remaining_weight**2 + b * remaining_weight + c
            print(f"Testing route: {
                  route + [next_node]}, cost: {current_cost + segment_cost}")
            branch_and_bound(
                route + [next_node],
                visited | {next_node},
                current_cost + segment_cost,
                remaining_weight - demand.get(next_node, 0)
            )

    # Start the search
    branch_and_bound([warehouse], set([warehouse]), 0, sum(demand.values()))

    return best_route, best_cost


# Usage example
os.chdir("Day13")
file_path = "instance.txt"
arcs, demand = load_instance(file_path)

# Print demand and arcs for debugging
print("Demand:", demand)
print("Arcs:", dict(arcs))

visualize_network(arcs, demand)

# Find the best route
best_route, best_cost = find_best_route(arcs, demand)
print("Best route:", best_route)
print("Best cost:", best_cost)

# Visualize solution
if best_route is None:
    print("No valid route found. Unable to visualize the solution.")
else:
    visualize_solution(arcs, demand, best_route)
