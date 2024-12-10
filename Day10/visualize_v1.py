# Load instance data
import numpy as np
import os
import matplotlib.pyplot as plt


# Load instance data


def load_instance(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        num_components, num_connections = map(int, lines[1].strip().split())
        connections = []
        for line in lines[1:]:
            if line.strip() and not line.startswith("#"):
                connections.append(tuple(map(int, line.strip().split())))
    return num_components, num_connections, connections

# Load solution data


def load_solution(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        positions = {}
        for line in lines:
            if line.strip() and line.startswith("Component"):
                parts = line.strip().split()
                component = int(parts[1])
                position = int(parts[-1])
                positions[component] = position
    return positions

# Visualization function


def visualize_solution(num_components, connections, positions, output_file="solution_arcs.png"):
    # Plot components on a line
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0.5, max(positions.values()) + 0.5)
    ax.set_ylim(-1, 1 + len(connections) * 0.1)
    ax.axis("off")

    # Draw connections as arcs
    for conn in connections:
        comp1, comp2 = conn
        pos1, pos2 = positions.get(comp1), positions.get(comp2)
        if pos1 is not None and pos2 is not None:
            # Compute the middle point and height of the arc
            mid = (pos1 + pos2) / 2
            # Height of the arc proportional to the distance
            height = abs(pos2 - pos1) * 0.2

            # Draw the arc
            x = np.linspace(pos1, pos2, 100)
            y = height - (4 * height / (pos2 - pos1)**2) * (x - mid)**2
            ax.plot(x, y, color="gray", alpha=0.5, zorder=1, linewidth=1)

    # Draw components
    for comp, pos in positions.items():
        ax.plot(
            pos, 0, 'o',
            color="blue",
            markersize=8,
            zorder=2
        )
        ax.text(
            pos, 0.2, str(comp),
            ha="center", va="bottom",
            fontsize=8, color="black"
        )

    plt.title("Components and Connections Visualization with Arcs")

    # Save the plot to a file
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()  # Close the plot to free memory


# Load data
os.chdir('Day10')

instance_file = "instance_clean.txt"  # Replace with your input file path
solution_file = "solution.txt"  # Replace with your solution file path
image_file = "solution.png"

num_components, num_connections, connections = load_instance(instance_file)
positions = load_solution(solution_file)

# Visualize and save to file
visualize_solution(num_components, connections, positions,
                   output_file=image_file)
print(connections)
