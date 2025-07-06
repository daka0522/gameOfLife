import numpy as np
import pygame
import sys

# 설정
CELL_SIZE = 20  # 작게 설정하면 더 많은 셀을 표현 가능
GRID_WIDTH = 50
GRID_HEIGHT = 50
FPS = 60

SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# SCREEN_WIDTH = 720
# SCREEN_HEIGHT = 720

# GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
# GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE


# 색상
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def initialize_grid():
    # 초기 생존 확률 20%
    return np.random.choice([0, 1], size=(GRID_HEIGHT, GRID_WIDTH), p=[0.8, 0.2])

def count_neighbors(grid):
    return (
        np.roll(np.roll(grid, 1, 0), 1, 1) +  # ↖
        np.roll(grid, 1, 0) +                # ↑
        np.roll(np.roll(grid, 1, 0), -1, 1) +# ↗
        np.roll(grid, -1, 0) +               # ↓
        np.roll(np.roll(grid, -1, 0), 1, 1) +# ↙
        np.roll(np.roll(grid, -1, 0), -1, 1)+# ↘
        np.roll(grid, 1, 1) +                # ←
        np.roll(grid, -1, 1)                 # →
    )

def update_grid(grid):
    
    """ 
    Rules
    1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    neighbors = count_neighbors(grid)

    # rule: Live
    # rule 1. Live. if live cell with 2 or 3 live neighbors
    rule1 = (grid == 1) & ((neighbors == 2) | (neighbors == 3))
    # rule 2. Live. if dead cell with 3 live neighbors
    rule2 = (grid == 0) & (neighbors == 3)

    # rule: Die
    # rule 3. Die. underpopulation
    rule3 = (grid == 1) & (neighbors < 2) 

    # rule 4. Die. overpopulation
    rule4 = (grid == 1) & (neighbors > 3)

    return rule1 | rule2

def draw_grid(screen, grid):
    surface = pygame.surfarray.make_surface(np.stack([grid*255]*3, axis=-1).astype(np.uint8))
    surface = pygame.transform.scale(surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(surface, (0, 0))



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life (Optimized version: NumPy + Pygame)")
    clock = pygame.time.Clock()

    grid = initialize_grid()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        grid = update_grid(grid).astype(np.uint8)
        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()
