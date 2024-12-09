import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Settings
os.chdir('Day8/minizinc')
dzn_folder = "data"  # Folder containing .dzn files
model_file = "binpack.mzn"  # Name of the MiniZinc model
results_file = "solution.txt"  # File to save results
time_limit_ms = 180000  # Time limit for each task (in milliseconds)
max_processes = 8  # Number of parallel processes

# Create/clear the results file
with open(results_file, "w") as f:
    f.write("Instance ID | Number of Bins | Best Known Bins\n")
    f.write("-" * 50 + "\n")

# Function to solve a single MiniZinc instance


def solve_instance(dzn_path):
    dzn_file = os.path.basename(dzn_path)
    command = [
        "minizinc",
        "--time-limit", str(time_limit_ms),
        model_file,
        dzn_path
    ]
    try:
        # Run MiniZinc and capture output
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )

        # Parse results
        output_lines = result.stdout.strip().split("\n")
        instance_id = "Unknown"
        num_bins = "N/A"
        best_known_bins = "N/A"

        for line in output_lines:
            if "Instance ID:" in line:
                instance_id = line.split(":")[1].strip()
            elif "Number of bins required:" in line:
                num_bins = line.split(":")[1].strip()
            elif "Smallest known number of bins:" in line:
                best_known_bins = line.split(":")[1].strip()

        # Save results to the file
        with open(results_file, "a") as f:
            f.write(f"{instance_id} | {num_bins} | {best_known_bins}\n")

    except subprocess.CalledProcessError as e:
        # Handle errors during MiniZinc execution
        with open(results_file, "a") as f:
            f.write(f"Error processing {dzn_file}: {e.stderr}\n")
        print(f"Error solving {dzn_file}: {e.stderr}")


# List all .dzn files
dzn_files = [os.path.join(dzn_folder, file)
             for file in os.listdir(dzn_folder) if file.endswith(".dzn")]

# Run tasks in parallel
with ThreadPoolExecutor(max_workers=max_processes) as executor:
    executor.map(solve_instance, dzn_files)

print(f"All tasks processed. Results saved to '{results_file}'.")
