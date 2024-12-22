import os

# Move to the 'Day19' directory
os.chdir('Day22')

# Read the contents of the 'instance.txt' file
with open('instance.txt', 'r') as file:
    data = file.readlines()

# Initialize variables
instances = {}  # Dictionary to store instance data
current_instance_name = None
current_instance_lines = []
is_collecting = False

# Process lines in the file
for line in data:
    line = line.strip()

    # Check for the start of a new instance
    if line.startswith("instance"):
        # Save the current instance if one exists
        if current_instance_name and current_instance_lines:
            instances[current_instance_name] = current_instance_lines

        # Extract the name of the new instance
        current_instance_name = line.split(
            "instance")[1].strip()  # Extract task name
        current_instance_lines = []
        is_collecting = False  # Reset the flag for reading numerical data

    # Detect if numerical data has started (a line with two numbers)
    elif line and len(line.split()) == 2 and line.split()[0].isdigit() and line.split()[1].isdigit():
        is_collecting = True
        current_instance_lines.append(line)

    # Collect lines with numerical data
    elif is_collecting:
        # Check line validity
        if line and all(part.isdigit() or part == " " for part in line.replace(" ", "")):
            current_instance_lines.append(line)

    # Finish collecting data for the current instance
    elif line.startswith("+++++++++++++++++++++++++++++++") and current_instance_lines:
        if current_instance_name:
            instances[current_instance_name] = current_instance_lines
        current_instance_lines = []
        is_collecting = False

# Process the last instance
if current_instance_name and current_instance_lines:
    instances[current_instance_name] = current_instance_lines

# Write each instance to its corresponding file
for instance_name, content in instances.items():
    filename = f"instance_{instance_name}.txt"
    with open(filename, 'w') as output_file:
        output_file.write("\n".join(content))

print("Processing complete! Data has been written to separate files.")
