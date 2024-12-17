import os
import matplotlib.pyplot as plt
import numpy as np
import re


def load_data(filepath):
    """
    Load landing times and safety gaps from the input file.
    """
    with open(filepath, 'r') as file:
        data = file.read()

    # Extract Landing list data
    landing_section = re.search(
        r'Landing list:\s*\(landing, earliest, target, latest\)([\s\S]*?)\n\n', data)
    landing_lines = landing_section.group(1).strip().split('\n')
    landings = []
    for line in landing_lines:
        landings.append([int(x) for x in line.split()])

    # Extract Safety gaps matrix
    safety_section = re.search(r'Safety gaps:([\s\S]*?)$', data)
    safety_lines = safety_section.group(1).strip().split('\n')
    safety_matrix = [list(map(int, re.findall(r'\d+', line)))
                     for line in safety_lines]

    return landings, np.array(safety_matrix)


def determine_sequence(landings, safety_matrix):
    """
    Determine landing sequence based on the earliest landing time (simple heuristic).
    """
    # Sort landings by the planned landing time (column 1)
    landings.sort(key=lambda x: x[1])
    sequence = [l[0] for l in landings]
    return sequence, landings


def plot_gantt(landings, safety_matrix, sequence):
    """
    Plot Gantt chart for the landings.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    y_positions = range(len(landings))
    colors = plt.cm.tab10.colors
    target_label_added = False
    planned_label_added = False

    for idx, landing in enumerate(landings):
        plane_id, planned, earliest, target, latest = landing
        y = y_positions[idx]
        # Draw landing window (earliest to latest)
        ax.barh(y, latest - earliest, left=earliest, height=0.6,
                color=colors[idx % len(colors)], alpha=0.3)

        # Target landing time as dashed vertical line limited to the rectangle height
        ax.vlines(x=target, ymin=y - 0.3, ymax=y + 0.3, colors='black', linestyles='--',
                  linewidth=1, label='Target Time' if not target_label_added else "")
        target_label_added = True

        # Planned landing time as marker 'x'
        ax.scatter(planned, y, color='red', marker='x', s=100,
                   label='Planned Time' if not planned_label_added else "")
        planned_label_added = True

        # Safety interval
        if idx < len(landings) - 1:
            gap = safety_matrix[plane_id - 1][landings[idx + 1][0] - 1]
            ax.hlines(y, planned, planned + gap, colors='black', linewidth=1)

    # Formatting the chart
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f'Plane {landing[0]}' for landing in landings])
    ax.set_xlabel('Time')
    ax.set_ylabel('Planes')
    ax.set_title('Landing Schedule Gantt Chart')
    ax.grid(True)

    # Add legend
    ax.legend()

    plt.tight_layout()
    plt.savefig('solution.png')
    plt.close()


def main():
    os.chdir('Day17')
    filepath = 'solution.txt'
    landings, safety_matrix = load_data(filepath)
    sequence, sorted_landings = determine_sequence(landings, safety_matrix)
    plot_gantt(sorted_landings, safety_matrix, sequence)
    print("Gantt chart saved as solution.png")


if __name__ == "__main__":
    main()
