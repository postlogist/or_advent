import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import os


# Function to parse the file and extract data
def parse_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Remove any empty or irrelevant lines
        lines = [line.strip() for line in lines if line.strip()]

        # Extracting instance name
        if not lines[0].startswith("Solving instance:"):
            raise ValueError(
                "First line does not contain the expected instance name format.")
        instance_name = lines[0].split(":")[1].strip()

        # Extracting the makespan
        if not lines[1].startswith("Makespan:"):
            raise ValueError(
                "Second line does not contain the expected makespan format.")
        makespan = int(lines[1].split(":")[1].strip())

        # Extracting the job schedule, skipping the header row
        schedule = []
        for line in lines[2:]:
            if line.startswith("Job schedule"):
                continue

            # Split the line into parts
            parts = line.split()
            if len(parts) != 5:
                raise ValueError(
                    f"Invalid schedule format: '{line}'. Expected 5 values (job, stage, machine, start, end).")

            job, stage, machine, start, end = map(int, parts)
            schedule.append((job, stage, machine, start, end))

        return instance_name, makespan, schedule

    except FileNotFoundError:
        raise FileNotFoundError(
            f"File '{file_path}' not found. Please check the path.")
    except ValueError as e:
        raise ValueError(f"Error parsing file '{file_path}': {e}")


# Function to plot the Gantt chart and save to file
def plot_gantt(instance_name, makespan, schedule, output_file):
    colors = {}
    color_map = plt.colormaps.get_cmap("tab10")

    fig, ax = plt.subplots(figsize=(12, 6))

    machines = sorted(set(machine for _, _, machine, _, _ in schedule))
    y_min, y_max = min(machines) - 1, max(machines) + 1  # Adjust Y-axis range

    # Adding patches for each operation
    for job, stage, machine, start, end in schedule:
        if job not in colors:
            colors[job] = color_map(job % 10)

        duration = end - start
        rect = patches.Rectangle((start, machine - 0.4), duration, 0.8,
                                 linewidth=1, edgecolor='black', facecolor=colors[job])
        ax.add_patch(rect)

        # Add job and stage number inside the rectangle
        ax.text(start + duration / 2, machine, f'{job}-{stage}',
                ha='center', va='center', color='white', fontsize=8)

    # Configure Y-axis
    ax.set_yticks(machines)
    ax.set_yticklabels([f"Machine {m}" for m in machines])
    ax.set_ylim(y_min, y_max)
    ax.set_ylabel("Machines", fontsize=12)

    # Configure X-axis and title
    ax.set_xlabel("Time", fontsize=12)
    ax.set_xlim(0, makespan)
    ax.set_title(f"Gantt Chart: {instance_name}\nTotal Makespan: {
                 makespan}", fontsize=14)

    # Add grid for better readability
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)

    # Save the figure to a file
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Gantt chart saved to {output_file}")

    plt.show()


# Main function
def main():
    parser = argparse.ArgumentParser(
        description="Generate Gantt chart from solution file.")
    parser.add_argument("file", type=str, help="Path to the solution file.")
    args = parser.parse_args()
    file_path = args.file
    output_file = os.path.splitext(file_path)[0] + ".png"

    try:
        instance_name, makespan, schedule = parse_file(file_path)
        plot_gantt(instance_name, makespan, schedule, output_file)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
