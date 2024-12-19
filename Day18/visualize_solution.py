import os
import graphviz


def load_network_data(file_path):
    """
    Load network data from a file and parse it into a usable format.

    Args:
        file_path (str): Path to the input file.

    Returns:
        tuple: (nodes, edges, hubs) where:
            - nodes (int): Number of nodes in the network.
            - edges (list): List of edges as (start_node, end_node, cost).
            - hubs (list): List of hub nodes.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Skip comments and empty lines, then extract data
    data = [line.strip() for line in lines if line.strip()
            and not line.startswith('#')]

    # Parse number of nodes and edges
    nodes, edges_count = map(int, data[0].split())

    # Parse edges
    edges = []
    for i in range(1, edges_count + 1):
        start, end, cost = map(int, data[i].split())
        edges.append((start, end, cost))

    # Parse hubs
    hub_count = int(data[edges_count + 1])
    hubs = list(map(int, data[edges_count + 2].split()))

    return nodes, edges, hubs


def load_solution_edges(file_path):
    """
    Load selected edges from a solution file.

    Args:
        file_path (str): Path to the solution file.

    Returns:
        list: List of selected edges as (start_node, end_node, cost).
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Extract lines after 'Selected edges:'
    data = [line.strip() for line in lines if line.strip()]
    start_index = data.index("Selected edges:") + 1
    selected_edges = []
    for line in data[start_index:]:
        start, end, cost = map(int, line.split())
        selected_edges.append((start, end, cost))

    return selected_edges


def visualize_network(nodes, edges, hubs, selected_edges):
    """
    Visualize the network using Graphviz.

    Args:
        nodes (int): Number of nodes in the network.
        edges (list): List of edges as (start_node, end_node, cost).
        hubs (list): List of hub nodes.
        selected_edges (list): List of edges to highlight as (start_node, end_node, cost).
    """
    dot = graphviz.Graph()  # Changed to Graph for undirected edges

    # Add nodes with different shapes for hubs and regular nodes
    for node in range(1, nodes + 1):
        if node in hubs:
            dot.node(str(node), shape='square',
                     style='filled', fillcolor='lightblue')
        else:
            dot.node(str(node), shape='circle')

    # Add edges with thickness proportional to cost
    for start, end, cost in edges:
        if (start, end, cost) in selected_edges or (end, start, cost) in selected_edges:
            dot.edge(str(start), str(end), penwidth=str(cost / 5), color='red')
        else:
            dot.edge(str(start), str(end), penwidth=str(cost / 5))

    # Render the graph
    dot.render('network_graph', format='png', cleanup=True)


# Change working directory to 'Day18'
os.chdir('Day18')

# File paths to the instance and solution files
instance_file_path = 'instance.txt'
solution_file_path = 'solution.txt'

# Load data and visualize
nodes, edges, hubs = load_network_data(instance_file_path)
selected_edges = load_solution_edges(solution_file_path)
visualize_network(nodes, edges, hubs, selected_edges)
