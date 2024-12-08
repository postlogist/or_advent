def best_fit_first(problem_data):
    results = []
    num_problems = int(problem_data[0])
    index = 1  # Start after the number of problems

    for _ in range(num_problems):
        # Read problem identifier
        problem_id = problem_data[index].strip()
        index += 1

        # Read problem details (bin capacity, number of items, best-known solution)
        bin_capacity, num_items, best_known_solution = map(
            int, problem_data[index].strip().split())
        index += 1

        # Read item sizes
        items = []
        for _ in range(num_items):
            items.append(int(problem_data[index].strip()))
            index += 1

        # Solve using Best Fit heuristic
        bins = []  # List to store current bins and their remaining capacity

        for item in items:
            # Find the best bin for the current item
            best_bin_index = -1
            min_space_left = bin_capacity + 1  # Initialize with an impossible value

            for i, space_left in enumerate(bins):
                if space_left >= item and space_left - item < min_space_left:
                    best_bin_index = i
                    min_space_left = space_left - item

            if best_bin_index == -1:  # No bin can accommodate the item; open a new bin
                bins.append(bin_capacity - item)
            else:  # Place the item in the best bin
                bins[best_bin_index] -= item

        # Store the result
        results.append((problem_id, len(bins), best_known_solution))

    return results


# Input data

# Read input data from 'instance.txt'
with open('Day8/instance_clean.txt', 'r') as file:
    problem_data = file.readlines()

# Solve the problems
results = best_fit_first(problem_data)

# Output the results
for result in results:
    print(f"{result[0]}, {result[1]}, {result[2]}")
