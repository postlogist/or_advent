import os


def load_tsp_instance(filename):
    dimension = None
    matrix = []
    reading_matrix = False

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                # Пропускаем пустые строки или комментарии
                continue
            if line.upper().startswith("DIMENSION"):
                # Формат строки: DIMENSION: <число>
                _, val = line.split(':')
                dimension = int(val.strip())
            elif line.upper().startswith("EDGE_WEIGHT_TYPE"):
                # Можно проверить, что EDGE_WEIGHT_TYPE: EXPLICIT
                pass
            elif line.upper().startswith("EDGE_WEIGHT_FORMAT"):
                # Ожидаем FULL_MATRIX
                pass
            elif line.upper().startswith("EDGE_WEIGHT_SECTION"):
                reading_matrix = True
            elif reading_matrix:
                # Читаем строки матрицы расстояний
                values = line.split()
                matrix.extend(values)
                # Остановимся, когда соберём dimension^2 элементов.
                if dimension is not None and len(matrix) == dimension * dimension:
                    reading_matrix = False

    if dimension is None or len(matrix) != dimension * dimension:
        print("I don't know")  # Не удалось корректно прочитать данные
        return None, None

    # Преобразуем в двумерный массив
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


def two_opt_swap(route, i, k):
    # Выполняет 2-opt перестановку на подмаршруте route[i:k+1]
    new_route = route[0:i]
    new_route.extend(reversed(route[i:k+1]))
    new_route.extend(route[k+1:])
    return new_route


def two_opt(dist_matrix, initial_route):
    # Реализация 2-opt эвристики для улучшения маршрута
    best = initial_route
    best_distance = compute_route_length(best, dist_matrix)

    improved = True
    while improved:
        improved = False
        for i in range(1, len(best)-2):
            for k in range(i+1, len(best)):
                new_route = two_opt_swap(best, i, k)
                new_distance = compute_route_length(new_route, dist_matrix)
                if new_distance < best_distance:
                    best = new_route
                    best_distance = new_distance
                    print("Улучшение найдено! Новая длина маршрута:", best_distance)
                    improved = True
                    break
            if improved:
                break
    return best, best_distance


def nearest_neighbor_route(dist_matrix, start=0):
    # Создаём маршрут, используя эвристику ближайшего соседа
    dimension = len(dist_matrix)
    unvisited = set(range(dimension))
    route = [start]
    unvisited.remove(start)

    current_city = start
    while unvisited:
        # Найдём ближайший город из не посещённых
        next_city = min(
            unvisited, key=lambda city: dist_matrix[current_city][city])
        route.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city

    return route


def main():
    filename = "instance.txt"
    dimension, dist_matrix = load_tsp_instance(filename)
    if dimension is None or dist_matrix is None:
        return

    # Начальный маршрут с помощью метода ближайшего города
    initial_route = nearest_neighbor_route(dist_matrix, start=0)

    # Применяем 2-opt эвристику для улучшения решения
    best_route, best_length = two_opt(dist_matrix, initial_route)

    print("Лучший найденный маршрут:", best_route)
    print("Длина маршрута:", best_length)


if __name__ == "__main__":
    os.chdir('Day12')
    main()
