import os


def preprocess_instance_file(input_file):
    # Read the file content
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Number of test problems
    num_problems = int(lines[0].strip())

    # Directory to store the .dzn files
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    idx = 1  # Start reading after the number of problems
    for _ in range(num_problems):
        # Instance identifier
        instance_id = lines[idx].strip()
        idx += 1

        # Bin capacity, number of items, and best known solution
        bin_capacity, num_items, best_known_bins = map(
            int, lines[idx].strip().split())
        idx += 1

        # Item sizes
        item_sizes = []
        for _ in range(num_items):
            item_sizes.append(int(lines[idx].strip()))
            idx += 1

        # Create .dzn file content
        dzn_content = f"""
        n = {num_items};
        bin_capacity = {bin_capacity};
        item_sizes = {item_sizes};
        instance_id = "{instance_id}";
        best_known_bins = {best_known_bins};
        """

        # Write to .dzn file
        output_file = os.path.join(output_dir, f"{instance_id}.dzn")
        with open(output_file, 'w') as dzn_file:
            dzn_file.write(dzn_content.strip())

    print(f"Preprocessing complete. {
          num_problems} .dzn files created in '{output_dir}'.")


# Specify the input file
input_file = "instance_clean.txt"
preprocess_instance_file(input_file)
