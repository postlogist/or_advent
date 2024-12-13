import os
import numpy as np
import pygad
import random


def load_instance(file_path):

    with open(file_path, 'r') as f:
        size = int(f.readline().strip())  # Первая строка содержит размерность
        data = f.read().replace('\n', '')
        matrix = np.fromstring(data, dtype=int, sep=' ').reshape((size, size))
        return size, matrix


def compute_route_length(route, dist_matrix):
    length = 0
    for i in range(len(route)):
        length += dist_matrix[route[i]][route[(i+1) % len(route)]]
    return length


def fitness_func(ga_instance, solution, solution_idx):
    route_length = compute_route_length(solution, dist_matrix)
    # Минимизируем длину -> максимизируем 1/(длина+1)
    # return 1.0 / (route_length + 1)
    return -route_length


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


def ox_crossover(parents, offspring_size, ga_instance):
    """
    Implementation of the Order Crossover (OX) operator for multiple parents to produce the required number of offspring.
    :param parents: A numpy array containing multiple parents (shape: [num_parents, num_genes]).
    :param offspring_size: Tuple representing the size of the offspring array (num_offspring, num_genes).
    :param ga_instance: The GA instance (not used here).
    :return: A numpy array of offspring created from the parents.
    """
    num_offspring, num_genes = offspring_size
    offspring = []

    for _ in range(num_offspring):
        # Randomly select two parents for crossover
        parent1, parent2 = parents[np.random.choice(
            parents.shape[0], 2, replace=False)]
        size = len(parent1)

        # Randomly select crossover points
        c1, c2 = sorted(random.sample(range(size), 2))

        # Create child
        child = [-1] * size
        child[c1:c2] = parent1[c1:c2]

        used = set(parent1[c1:c2])
        pos = c2
        for gene in parent2:
            if gene not in used:
                if pos >= size:
                    pos = 0
                child[pos] = gene
                pos += 1

        offspring.append(child)

    # Return offspring as a numpy array
    return np.array(offspring)

    # offspring = []
    # idx = 0
    # while len(offspring) != offspring_size[0]:
    #     parent1 = parents[idx % parents.shape[0], :].copy()
    #     parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

    #     random_split_point = np.random.choice(range(offspring_size[1]))

    #     parent1[random_split_point:] = parent2[random_split_point:]

    #     offspring.append(parent1)

    #     idx += 1

    # return np.array(offspring)


def swap_mutation(offspring, ga_instance):
    for idx in range(offspring.shape[0]):
        size = offspring.shape[1]
        i1, i2 = random.sample(range(size), 2)
        offspring[idx, i1], offspring[idx,
                                      i2] = offspring[idx, i2], offspring[idx, i1]
    return offspring


# Загрузка файла данных
os.chdir('Day12/heuristics')
dimension, dist_matrix = load_instance("instance_clean.txt")


def two_opt(route, dist_matrix):
    best = route[:]
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 1):
            for j in range(i + 1, len(route)):
                new_route = np.concatenate(
                    [route[:i], route[i:j][::-1], route[j:]])
                if compute_route_length(new_route, dist_matrix) < compute_route_length(best, dist_matrix):
                    best = new_route
                    improved = True
    return np.array(best)


population_size = 30
initial_population = []

initial_population.append(nearest_neighbor_route(dist_matrix))

for i in range(population_size-1):
    initial_population.append(two_opt(initial_population[-1], dist_matrix))


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
    # crossover_type="custom",
    crossover_type=ox_crossover,
    # mutation_type="custom",
    mutation_type=swap_mutation,
    on_generation=lambda ga: print(
        f"Поколение {ga.generations_completed}: лучшая приспособленность = {
            ga.best_solution()[1]}, длина = {compute_route_length(ga.best_solution()[0], dist_matrix)}"
    ),
)

ga_instance.run()

best_solution, best_fitness, _ = ga_instance.best_solution()
best_length = compute_route_length(best_solution, dist_matrix)

print("Лучший найденный маршрут:", best_solution)
print("Длина лучшего маршрута:", best_length)
