import os


def read_instance(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        num_cities = int(lines[0].strip())
        # Flatten the matrix data into a single list of integers
        matrix_data = list(
            map(int, [token for token in ' '.join(lines[1:]).split() if token.isdigit()]))
        # Create a square matrix based on the number of cities
        distance_matrix = [
            matrix_data[i * num_cities:(i + 1) * num_cities]
            for i in range(num_cities)
        ]
    return num_cities, distance_matrix


def read_solution2(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        num_cities = int(lines[0].split(':')[1].strip())
        total_distance = int(lines[1].split(':')[1].strip())
        # print(lines[2].split(', '))
        route = list(
            map(lambda x: int(x), lines[2].split(', ')))
    return num_cities, total_distance, route


def read_solution(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        num_cities = int(lines[0].split(':')[1].strip())
        total_distance = int(lines[1].split(':')[1].strip())
        route = list(map(int, lines[2].split(':')[1].strip().split('->')))
    return num_cities, total_distance, route


def calculate_route_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
        print(f"{route[i]}->{route[i + 1]}: {distance_matrix[route[i]]
              [route[i + 1]]}, total: {total_distance}")
    # Добавляем расстояние возвращения в начальный город
    total_distance += distance_matrix[route[-1]][route[0]]
    print(f"{route[-1]}->{route[0]}: {distance_matrix[route[-1]]
          [route[0]]}, total: {total_distance}")
    return total_distance


def main():
    instance_file = 'instance_clean.txt'
    solution_file = 'solution_tf.txt'

    # Read data
    num_cities, distance_matrix = read_instance(instance_file)
    sol_num_cities, sol_total_distance, route = read_solution2(solution_file)

    # for i in range(len(distance_matrix)):
    #     print(i+1, len(distance_matrix[i]))

    # Checking number of cities
    if num_cities != sol_num_cities:
        print("Error: the number of cities in solution differs from the instance")
        return

    calculated_distance = calculate_route_distance(route, distance_matrix)

    # Output
    print(f"Calculated distance: {calculated_distance}")
    print(f"Distance from the solution: {sol_total_distance}")

    if calculated_distance == sol_total_distance:
        print("Solution is valid.")
    else:
        print("Solution is invalid.")


if __name__ == "__main__":
    #    os.chdir("Day12")
    main()
