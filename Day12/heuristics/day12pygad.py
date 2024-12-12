import pygad
import numpy as np
import random
import os


def load_tsp_instance(filename):
    dimension = None
    matrix = []
    reading_matrix = False

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.upper().startswith("DIMENSION"):
                _, val = line.split(':')
                dimension = int(val.strip())
            elif line.upper().startswith("EDGE_WEIGHT_TYPE"):
                pass
            elif line.upper().startswith("EDGE_WEIGHT_FORMAT"):
                pass
            elif line.upper().startswith("EDGE_WEIGHT_SECTION"):
                reading_matrix = True
            elif reading_matrix:
                values = line.split()
                matrix.extend(values)
                if dimension is not None and len(matrix) == dimension * dimension:
                    reading_matrix = False

    if dimension is None or len(matrix) != dimension * dimension:
        print("I don't know")
        return None, None

    dist_matrix = []
    for i in range(dimension):
        row = matrix[i*dimension:(i+1)*dimension]
        dist_matrix.append(list(map(int, row)))
    return dimension, dist_matrix


def compute_route_length(route, dist_matrix):
    length = 0
    for i in range(len(route)):
        length += dist_matrix[route[i]][route[(i+1) % len(route)]]
    return length


def fitness_func(ga_instance, solution, solution_idx):
    route_length = compute_route_length(solution, dist_matrix)
    # Минимизируем длину -> максимизируем 1/(длина+1)
    return 1.0 / (route_length + 1)


def nearest_neighbor_route(dist_matrix, start=0):
    dimension = len(dist_matrix)
    unvisited = set(range(dimension))
    route = [start]
    unvisited.remove(start)
    current_city = start
    while unvisited:
        next_city = min(
            unvisited, key=lambda city: dist_matrix[current_city][city])
        route.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city
    return np.array(route, dtype=int)


def ox_crossover(parent1, parent2, ga_instance):
    # OX-кроссовер:
    # 1) Выбираем два разреза
    size = len(parent1)
    c1, c2 = sorted(random.sample(range(size), 2))

    # Создаем потомка 1
    child1 = [-1]*size
    child1[c1:c2] = parent1[c1:c2]

    # Заполняем оставшиеся гены из parent2 в порядке, пропуская уже взятые города
    used = set(parent1[c1:c2])
    pos = c2
    for gene in parent2:
        if gene not in used:
            if pos >= size:
                pos = 0
            child1[pos] = gene
            pos += 1

    # Потомок 2 аналогично:
    child2 = [-1]*size
    child2[c1:c2] = parent2[c1:c2]
    used = set(parent2[c1:c2])
    pos = c2
    for gene in parent1:
        if gene not in used:
            if pos >= size:
                pos = 0
            child2[pos] = gene
            pos += 1

    return np.array(child1), np.array(child2)


def swap_mutation(offspring, ga_instance):
    # Swap mutation: обмен двух случайных генов
    for idx in range(offspring.shape[0]):
        # В зависимости от процента мутации pygad вызывает эту функцию,
        # мы просто делаем swap один раз
        size = offspring.shape[1]
        i1, i2 = random.sample(range(size), 2)
        # Меняем местами
        temp = offspring[idx, i1]
        offspring[idx, i1] = offspring[idx, i2]
        offspring[idx, i2] = temp
    return offspring


if __name__ == "__main__":
    filename = "instance.txt"
    os.chdir('Day12')
    dimension, dist_matrix = load_tsp_instance(filename)
    if dimension is None or dist_matrix is None:
        exit()

    population_size = 30
    # Формируем начальную популяцию:
    # Часть - по эвристике ближайшего соседа
    # Часть - случайные перестановки для разнообразия
    initial_population = []
    for _ in range(population_size // 2):
        start_city = random.randint(0, dimension-1)
        route = nearest_neighbor_route(dist_matrix, start=start_city)
        initial_population.append(route)
    for _ in range(population_size - len(initial_population)):
        route = np.random.permutation(dimension)
        initial_population.append(route)

    initial_population = np.array(initial_population)

    ga_instance = pygad.GA(
        num_generations=100,
        num_parents_mating=10,
        fitness_func=fitness_func,
        sol_per_pop=population_size,
        num_genes=dimension,
        initial_population=initial_population,
        gene_type=int,
        mutation_percent_genes=10,
        # Используем кастомный кроссовер
        crossover_type="custom",
        crossover_func=ox_crossover,  # вместо crossover_function
        # Используем кастомную мутацию
        mutation_type="custom",
        mutation_func=swap_mutation,  # вместо mutation_function
        on_generation=lambda ga: print(f"Поколение {ga.generations_completed}: лучшая приспособленность = {
                                       ga.best_solution()[1]}, длина = {compute_route_length(ga.best_solution()[0], dist_matrix)}")
    )

    ga_instance.run()

    best_solution, best_fitness, _ = ga_instance.best_solution()
    best_length = compute_route_length(best_solution, dist_matrix)

    print("Лучший найденный маршрут:", best_solution)
    print("Длина лучшего маршрута:", best_length)
