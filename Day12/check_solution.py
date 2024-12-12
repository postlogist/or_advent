import os


def read_instance(filename):
    dimension = None
    matrix = []
    start_reading_matrix = False

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            # Читаем размерность
            if line.startswith('DIMENSION'):
                parts = line.split(':')
                if len(parts) > 1:
                    dimension = int(parts[1].strip())

            # Как только находим EDGE_WEIGHT_SECTION, начинаем читать матрицу
            elif line.startswith('EDGE_WEIGHT_SECTION'):
                start_reading_matrix = True
                continue

            elif start_reading_matrix:
                # Игнорируем пустые и комментные строки
                if not line or line.startswith('#'):
                    continue

                # Преобразуем строку в список чисел
                row = list(map(int, line.split()))

                # Проверяем, что в строке ровно DIMENSION чисел
                if dimension is not None and len(row) != dimension:
                    raise ValueError(
                        f"Ожидается {dimension} значений в строке матрицы, получено: {
                            len(row)}"
                    )

                matrix.append(row)

                # Если считали все DIMENSION строк
                if dimension is not None and len(matrix) == dimension:
                    break

    # Проверка корректности размера матрицы
    if dimension is None or len(matrix) != dimension:
        raise ValueError(
            "Некорректный формат матрицы или не совпадает количество строк с DIMENSION.")

    return matrix


def read_solution(filename):
    route = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('Route:'):
                # Формат: Route: 1 -> 198 -> 35 -> ...
                # Нужно извлечь числа
                parts = line.split(':', 1)
                if len(parts) > 1:
                    route_part = parts[1].strip()
                    # Разделим по '->'
                    route_str = route_part.split('->')
                    # Очистим пробелы и превратим в числа
                    route = [int(r.strip())-1 for r in route_str]
                break
    if not route:
        raise ValueError("Не удалось прочитать маршрут из файла solution.txt")
    return route


def calculate_route_distance(matrix, route):
    # Предполагается, что индекс города в route начинается с 1, а в матрице с 0.
    # matrix[i][j] - расстояние от города i+1 к j+1.
    total_distance = 0
    for i in range(len(route)-1):
        from_city = route[i] - 1
        to_city = route[i+1] - 1
        total_distance += matrix[from_city][to_city]

    # Добавляем переход от последнего города к первому
    last_city = route[-1] - 1
    first_city = route[0] - 1
    total_distance += matrix[last_city][first_city]

    return total_distance


if __name__ == "__main__":
    # Замените 'instance.txt' и 'solution.txt' на нужные вам пути к файлам
    os.chdir("Day12")
    instance_file = 'instance.txt'
    solution_file = 'solution.txt'

    # Читаем данные
    matrix = read_instance(instance_file)
    route = read_solution(solution_file)
    for i in range(len(matrix)):
        print(i, len(matrix[i]))
    # Вычисляем длину
    dist = calculate_route_distance(matrix, route)
    print(f"Computed total distance: {dist}")
