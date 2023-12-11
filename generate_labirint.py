import random

def generate_labyrinth(size):
    """
    Генерирует лабиринт заданного размера.

    Args:
    size (int): Размер лабиринта (количество ячеек в ширину/высоту).

    Returns:
    list: Двумерный массив, представляющий лабиринт.
    """
    labyrinth = [[1 for _ in range(size)] for _ in range(size)]
    carve_passages(1, 1, labyrinth, size)
    return labyrinth

def carve_passages(x, y, labyrinth, size):
    """
    Рекурсивно прорезает проходы в лабиринте.

    Args:
    x, y (int): Текущие координаты в лабиринте.
    labyrinth (list): Двумерный массив лабиринта.
    size (int): Размер лабиринта.
    """
    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
    random.shuffle(directions)

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < size and 0 <= new_y < size and labyrinth[new_y][new_x] == 1:
            labyrinth[new_y][new_x] = 0
            labyrinth[new_y - dy//2][new_x - dx//2] = 0
            carve_passages(new_x, new_y, labyrinth, size)

def print_labyrinth(labyrinth):
    """
    Выводит лабиринт в консоль.

    Args:
    labyrinth (list): Двумерный массив лабиринта.
    """
    for row in labyrinth:
        print(" ".join(' ' if cell == 0 else 'H' for cell in row))

# Пример использования:
labyrinth = generate_labyrinth(31)
print_labyrinth(labyrinth)
