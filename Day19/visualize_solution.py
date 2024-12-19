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

        # Checking if the file has enough lines
        if len(lines) < 3:
            raise ValueError(
                "File does not contain enough data. Expected at least 3 lines with relevant information.")

        # Extracting the instance name
        if not lines[0].startswith("Solving instance:"):
            raise ValueError(
                "First line does not contain the expected instance name format.")
        instance_name = lines[0].split(":")[1].strip()

        # Extracting the makespan
        if not lines[1].startswith("Makespan:"):
            raise ValueError(
                "Second non-empty line does not contain the expected makespan format.")
        makespan = int(lines[1].split(":")[1].strip())

        # Extracting the job schedule, skipping the header row
        schedule = []
        for line in lines[2:]:
            # Skip the job schedule header line ("Job schedule (job, stage, start, end):")
            if line.startswith("Job schedule"):
                continue

            # Split the line into parts and ensure it contains 4 numeric values
            parts = line.split()
            if len(parts) != 4:
                raise ValueError(f"Invalid schedule format: '{
                                 line}'. Expected 4 values (job, stage, start, end).")

            job, stage, start, end = map(int, parts)
            schedule.append((job, stage, start, end))

        return instance_name, makespan, schedule

    except FileNotFoundError:
        raise FileNotFoundError(
            f"File '{file_path}' not found. Please check the path.")
    except ValueError as e:
        raise ValueError(f"Error parsing file '{file_path}': {e}")

# Function to plot the Gantt chart and save to file


def plot_gantt(instance_name, makespan, schedule, output_file):
    colors = {}  # Dictionary to store colors for each job
    # Updated to use new colormap syntax
    color_map = plt.colormaps.get_cmap("tab10")

    fig, ax = plt.subplots(figsize=(12, 6))

    y_labels = []  # Labels for the y-axis (stages)
    # Extract unique stages
    stages = sorted(set(stage for _, stage, _, _ in schedule))

    # Adding patches for each operation
    for job, stage, start, end in schedule:
        # Assign a unique color to each job
        if job not in colors:
            colors[job] = color_map(job % 10)

        # Plot operation as a rectangle
        duration = end - start
        rect = patches.Rectangle((start, stage), duration, 0.8,  # 0.8 for rectangle height
                                 linewidth=1, edgecolor='black', facecolor=colors[job])
        ax.add_patch(rect)

        # Add job number inside the rectangle
        ax.text(start + duration / 2, stage + 0.4, f'{job}',     # Vertically align in the middle
                ha='center', va='center', color='white', fontsize=8)

    # Configure Y-axis
    ax.set_yticks(stages)
    ax.set_yticklabels([f"Stage {stage}" for stage in stages])
    ax.set_ylabel("Stages", fontsize=12)

    # Configure X-axis and title
    ax.set_xlabel("Time", fontsize=12)
    ax.set_xlim(0, makespan)
    ax.set_title(f"Gantt Chart: {instance_name}\nTotal Makespan: {
                 makespan}", fontsize=14)

    # Add grid for better readability
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)

    # Save the figure to a file
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)  # Save as PNG with high resolution
    print(f"Gantt chart saved to {output_file}")

    # Show the plot (optional)
    plt.show()

# Main function


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Generate Gantt chart from solution file.")
    parser.add_argument("file", type=str, help="Path to the solution file.")

    # Parse arguments
    args = parser.parse_args()
    file_path = args.file

    # Generate the output file path
    # Replace extension with .png
    output_file = os.path.splitext(file_path)[0] + ".png"

    try:
        # Parse the file to extract data
        instance_name, makespan, schedule = parse_file(file_path)

        # Plot the Gantt chart and save to file
        plot_gantt(instance_name, makespan, schedule, output_file)

    except Exception as e:
        print(f"Error: {e}")


# Run the program
if __name__ == "__main__":
    main()
