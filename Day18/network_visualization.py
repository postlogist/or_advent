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


def visualize_network(nodes, edges, hubs):
    """
    Visualize the network using Graphviz.

    Args:
        nodes (int): Number of nodes in the network.
        edges (list): List of edges as (start_node, end_node, cost).
        hubs (list): List of hub nodes.
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
        dot.edge(str(start), str(end), penwidth=str(cost / 10))

    # Render the graph
    dot.render('network_graph', format='png', cleanup=True)


# Change working directory to 'Day18'
os.chdir('Day18')

# File path to the instance file
file_path = 'instance.txt'

# Load data and visualize
nodes, edges, hubs = load_network_data(file_path)
visualize_network(nodes, edges, hubs)
