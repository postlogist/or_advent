import os
import numpy as np
import matplotlib.pyplot as plt


# Load instance data
def load_instance(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        num_components, num_connections = map(int, lines[1].strip().split())
        connections = []
        for line in lines[2:]:  # Считываем со второй строки, пропуская заголовок
            if line.strip() and not line.startswith("#"):
                connections.append(tuple(map(int, line.strip().split())))
    return num_components, num_connections, connections


# Load solution data
def load_solution(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        positions = {}
        instance_file = ""
        max_crossings = None
        for line in lines:
            if line.startswith("Solving instance:"):
                # Извлекаем имя файла без пути
                instance_file = line.split(":")[1].strip().split("/")[-1]
            elif line.startswith("Max number of crossings:"):
                # Извлекаем значение максимального количества пересечений
                max_crossings = int(line.split(":")[1].strip())
            elif line.startswith("Component"):
                # Извлекаем позиции компонентов
                parts = line.strip().split()
                component = int(parts[1])
                position = int(parts[-1])
                positions[component] = position
        return instance_file, max_crossings, positions


# Visualization function
def visualize_solution(num_components, connections, positions, max_crossings, output_file="solution_arcs.png"):
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

    # Add max crossings as text
    # plt.text(
    #     0.5, 1.2, f"Max crossings: {max_crossings}",
    #     transform=ax.transAxes,
    #     fontsize=12, ha="left", va="center", color="red"
    # )

    plt.title(f"Max crossings: {max_crossings}")

    # Save the plot to a file
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()  # Close the plot to free memory


# Main logic
os.chdir('Day10')
solution_file = "solution.txt"  # Replace with your solution file path
image_file = "solution.png"

# Load solution to extract instance filename and max crossings
instance_file, max_crossings, positions = load_solution(solution_file)

# Load the corresponding instance file
num_components, num_connections, connections = load_instance(instance_file)

# Visualize and save to file
visualize_solution(num_components, connections, positions,
                   max_crossings, output_file=image_file)

print(connections)
