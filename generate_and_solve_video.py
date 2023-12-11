import pygame
import random
import os
import cv2
import time
from queue import Queue

# Параметры окна и сетки
CELL_SIZE = 20
LABIRINT_SIZE = 25  # Размер лабиринта

# Автоматический расчет размеров окна
WIDTH = LABIRINT_SIZE * CELL_SIZE
HEIGHT = LABIRINT_SIZE * CELL_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Инициализация Pygame
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лабиринт")

def draw_labirint(labirint, frame_counter, path=None, start=None, finish=None):
    win.fill(WHITE)
    for y in range(len(labirint)):
        for x in range(len(labirint[y])):
            color = BLACK if labirint[y][x] == 1 else WHITE
            if path and (y, x) in path:
                color = GREEN
            pygame.draw.rect(win, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if start:
        pygame.draw.rect(win, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if finish:
        pygame.draw.rect(win, RED, (finish[1] * CELL_SIZE, finish[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.update()
    pygame.image.save(win, f"images/frame_{frame_counter:04d}.png")

def generate_labirint(labirint_size):
    labirint = [[1 for _ in range(labirint_size)] for _ in range(labirint_size)]
    frame_counter = 0

    def recurse(x, y):
        nonlocal frame_counter
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < labirint_size and 0 <= new_y < labirint_size and labirint[new_y][new_x] == 1:
                labirint[new_y][new_x] = 0
                labirint[new_y - dy // 2][new_x - dx // 2] = 0
                draw_labirint(labirint, frame_counter)
                frame_counter += 1
                recurse(new_x, new_y)

    labirint[1][1] = 0
    draw_labirint(labirint, frame_counter)
    frame_counter += 1
    recurse(1, 1)
    return labirint, frame_counter

def bfs_find_path(labirint, start, finish, frame_counter):
    queue = Queue()
    queue.put((start, [start]))
    visited = set()

    while not queue.empty():
        current, path = queue.get()
        if current == finish:
            draw_labirint(labirint, frame_counter, path=path, start=start, finish=finish)
            return path, frame_counter

        if current not in visited:
            visited.add(current)
            y, x = current
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_y, new_x = y + dy, x + dx
                if 0 <= new_y < LABIRINT_SIZE and 0 <= new_x < LABIRINT_SIZE and labirint[new_y][new_x] == 0:
                    queue.put(((new_y, new_x), path + [(new_y, new_x)]))
            draw_labirint(labirint, frame_counter, path=path, start=start, finish=finish)
            frame_counter += 1

    return [], frame_counter

def create_video(image_folder, video_name, fps):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    last_frame = cv2.imread(os.path.join(image_folder, images[-1]))
    for _ in range(fps*2):
        video.write(last_frame)

    cv2.destroyAllWindows()
    video.release()

def main():
    if not os.path.exists("images"):
        os.makedirs("images")

    labirint, frame_counter = generate_labirint(LABIRINT_SIZE)
    start_point, finish_point = (1, 1), (LABIRINT_SIZE - 2, LABIRINT_SIZE - 2)
    path, frame_counter = bfs_find_path(labirint, start_point, finish_point, frame_counter)

    create_video("images", "labirint.mp4", 30)
    pygame.quit()

if __name__ == "__main__":
    main()
