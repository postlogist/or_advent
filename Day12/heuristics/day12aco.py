import os
import math
import random


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


def ant_colony_optimization(dist_matrix, num_ants=10, num_iterations=100, alpha=1.0, beta=5.0, rho=0.5, Q=100):
    # dist_matrix: матрица расстояний
    # num_ants: количество муравьёв
    # num_iterations: количество итераций алгоритма
    # alpha: влияние феромонов
    # beta: влияние эвристической информации (1/расстояние)
    # rho: коэффициент испарения феромона
    # Q: параметр для обновления феромонов

    dimension = len(dist_matrix)

    # Инициализация феромонов (равномерно)
    pheromones = [[1.0 for _ in range(dimension)] for _ in range(dimension)]

    # Эвристическая информация tau_ij = 1/d_ij (если d_ij != 0)
    # Если расстояние равно 0 (город в себя), то ставим небольшое число, чтобы не делить на ноль
    heuristic = [[1.0/(dist_matrix[i][j] if dist_matrix[i][j] > 0 else 0.0001)
                  for j in range(dimension)] for i in range(dimension)]

    best_route = None
    best_length = math.inf

    for iteration in range(num_iterations):
        all_routes = []
        all_lengths = []

        # Каждая муравьиная особь строит свой маршрут
        for ant in range(num_ants):
            route = [random.randint(0, dimension - 1)]
            visited = set(route)
            for _ in range(dimension - 1):
                current_city = route[-1]
                # Вычисляем вероятность перехода
                # p_ij = (pheromone[current_city][j]^alpha * heuristic[current_city][j]^beta) / sum(...)
                probabilities = []
                denominator = 0.0
                for city in range(dimension):
                    if city not in visited:
                        val = (pheromones[current_city][city]**alpha) * \
                            (heuristic[current_city][city]**beta)
                        denominator += val
                        probabilities.append((city, val))

                if denominator == 0:
                    # Все феромоны очень маленькие, выбираем случайно
                    city = random.choice([c for c, v in probabilities])
                    route.append(city)
                    visited.add(city)
                else:
                    # Рулетка
                    rand_val = random.random()
                    cum_prob = 0.0
                    chosen_city = None
                    for city, val in probabilities:
                        cum_prob += val / denominator
                        if rand_val <= cum_prob:
                            chosen_city = city
                            break
                    route.append(chosen_city)
                    visited.add(chosen_city)

            # Вычисляем длину построенного маршрута
            route_length = compute_route_length(route, dist_matrix)
            all_routes.append(route)
            all_lengths.append(route_length)

        # Находим лучший маршрут среди текущих муравьёв
        min_length = min(all_lengths)
        min_route = all_routes[all_lengths.index(min_length)]

        # Обновляем глобальный лучший результат
        if min_length < best_length:
            best_length = min_length
            best_route = min_route[:]
            print(f"Итерация {iteration}: новое лучшее решение длиной {
                  best_length}")

        # Испаряем феромоны
        for i in range(dimension):
            for j in range(dimension):
                pheromones[i][j] *= (1 - rho)
                if pheromones[i][j] < 0.0000001:
                    pheromones[i][j] = 0.0000001

        # Обновление феромонов по лучшему маршруту (можно использовать global-best или iteration-best)
        # Здесь используем iteration-best для разнообразия
        for i in range(dimension):
            current_city = min_route[i]
            next_city = min_route[(i + 1) % dimension]
            pheromones[current_city][next_city] += Q / min_length
            pheromones[next_city][current_city] += Q / min_length

    return best_route, best_length


def main():
    filename = "instance.txt"
    dimension, dist_matrix = load_tsp_instance(filename)
    if dimension is None or dist_matrix is None:
        return

    best_route, best_length = ant_colony_optimization(
        dist_matrix, num_ants=20, num_iterations=50, alpha=1.0, beta=5.0, rho=0.5, Q=100)

    print("Лучший найденный маршрут:", best_route)
    print("Длина лучшего маршрута:", best_length)


if __name__ == "__main__":
    os.chdir("Day12")
    main()
