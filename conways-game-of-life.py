import pygame
from pygame.locals import *

WIDTH, HEIGHT = 800, 600
FPS = 60

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
pygame.init()

clock = pygame.time.Clock()
running = True

MAP_SIZE = (100,100)

grid = [[0 for _ in range(MAP_SIZE[0])] for _ in range(MAP_SIZE[1])]

top_left = (0, 0)
cell_size = 5

mouse_down = False

paused = True

def next(grid):
    new_grid = [[0 for _ in range(MAP_SIZE[0])] for _ in range(MAP_SIZE[1])]

    for i, row in enumerate(grid):
        for j, x in enumerate(row):
            alive_neighbors = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    if 0 <= i+dy < MAP_SIZE[1] and 0 <= j+dx < MAP_SIZE[0]:
                        alive_neighbors += grid[i+dy][j+dx]

            if x == 1 and (alive_neighbors == 2 or alive_neighbors == 3):
                new_grid[i][j] = 1
            elif x == 0 and alive_neighbors == 3:
                new_grid[i][j] = 1
            else:
                new_grid[i][j] = 0

    return new_grid

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
               paused = not paused
            elif event.key == K_r:
                grid = [[0 for _ in range(MAP_SIZE[0])] for _ in range(MAP_SIZE[1])]
            elif event.key == K_c:
                grid = next(grid)
        if event.type == MOUSEBUTTONDOWN:
            mouse_down = True
            cells_painted = []
        if event.type == MOUSEBUTTONUP:
            mouse_down = False
    if mouse_down:
        mx, my = event.pos
        grid_y = (my - top_left[1]) // cell_size
        grid_x = (mx - top_left[0]) // cell_size
        if 0 <= grid_x < MAP_SIZE[0] and 0 <= grid_y < MAP_SIZE[1]:
            if (grid_x, grid_y) in cells_painted:
                continue
            else:
                cells_painted.append((grid_x, grid_y))
                grid[grid_y][grid_x] = 1 - grid[grid_y][grid_x]
    keys = pygame.key.get_pressed()
    if keys[K_DOWN]:
        top_left = (top_left[0], top_left[1] - 5)
    elif keys[K_UP]:
        top_left = (top_left[0], top_left[1] + 5)
    elif keys[K_RIGHT]:
        top_left = (top_left[0] - 5, top_left[1])
    elif keys[K_LEFT]:
        top_left = (top_left[0] + 5, top_left[1])
    elif keys[K_EQUALS] or keys[K_PLUS]:
        cell_size += 1
    elif keys[K_MINUS]:
        cell_size = max(1, cell_size - 1)

    if not paused:
        grid = next(grid)

    win.fill((100, 100, 100))

    
    for y in range(MAP_SIZE[1]):
        for x in range(MAP_SIZE[0]):
                pygame.draw.rect(win, (255, 255, 255) if grid[y][x]==1 else (0,0,0), (top_left[0] + x * cell_size, top_left[1] + y * cell_size, cell_size*0.9, cell_size*0.9))

    win.blit(pygame.font.SysFont("Arial", 18).render("Space: Pause/Unpause | R: Reset | C: Step | Arrows: Move | +/-: Zoom", True, (255,255,255)), (10,10))


    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()