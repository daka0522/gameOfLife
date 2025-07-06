import pygame
import random
import sys

# 설정
CELL_SIZE = 10
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

def create_random_grid():
    return [[random.choice([0, 1]) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(screen, grid):
    screen.fill(BLACK)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 1:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect)

def count_neighbors(grid, x, y):
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    count = 0
    for dx, dy in directions:
        nx, ny = (x + dx) % GRID_WIDTH, (y + dy) % GRID_HEIGHT
        count += grid[ny][nx]
    return count

def update_grid(grid):
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(grid, x, y)

            # Conway's Game of Life 규칙 적용
            # 1. 생명체가 2개 또는 3개 이웃이 있으면 생존
            if grid[y][x] == 1 and neighbors in [2, 3]:
                new_grid[y][x] = 1
            # 2. 생명체가 1개 이하 또는 4개 이상 이웃이 있으면 죽음
            elif grid[y][x] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[y][x] = 0
            # 3. 죽은 세포가 정확히 3개 이웃이 있으면 생명 탄생

            elif grid[y][x] == 0 and neighbors == 3:
                new_grid[y][x] = 1
    return new_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life (Auto Simulation)")
    clock = pygame.time.Clock()



    grid = create_random_grid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        grid = update_grid(grid)
        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(10)  # FPS

if __name__ == "__main__":
    main()
