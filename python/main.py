import sys
import pygame
from typing import List
from box import Box
from path_finding_algorithms import dijkstra


# COLORS
WALL_COLOR = (96, 96, 96)
START_COLOR = (255, 255, 51)
TARGET_COLOR = (0, 0, 0)
PATH_COLOR = (51, 153, 255)
QUEUED_COLOR = (0, 153, 0)
VISITED_COLOR = (153, 255, 153)
BACKGROUND_COLOR = (169, 169, 169)

# Constants
width = 1000
height = 1000
columns = 25
rows = 25
box_width = width // columns
box_height = height // rows


def make_grid(columns: int, rows: int) -> List:
    """Create grid."""
    grid = []
    for i in range(columns):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)
    return grid


def set_neighbours(grid: List, columns: int, rows: int) -> None:
    """Set neighbours."""
    for i in range(columns):
        for j in range(rows):
            grid[i][j].set_neighbours(grid, columns, rows)


def reset_grid(grid: List, columns: int, rows: int) -> None:
    """Reset boxes in grid."""
    for i in range(columns):
        for j in range(rows):
            box = grid[i][j]
            box.start = False
            box.wall = False
            box.target = False
            box.queued = False
            box.visited = False
            box.neighbours = []
            box.prior = None


def draw_grid(window, grid, columns, rows, path) -> None:
    """Draw the grid."""
    for i in range(columns):
        for j in range(rows):
            box = grid[i][j]
            box.draw(window, BACKGROUND_COLOR, box_width, box_height)

            if box.queued:
                box.draw(window, QUEUED_COLOR, box_width, box_height)
            if box.visited:
                box.draw(window, VISITED_COLOR, box_width, box_height)
            if box in path:
                box.draw(window, PATH_COLOR, box_width, box_height)
            if box.start:
                box.draw(window, START_COLOR, box_width, box_height)
            if box.target:
                box.draw(window, TARGET_COLOR, box_width, box_height)
            if box.wall:
                box.draw(window, WALL_COLOR, box_width, box_height)


def main() -> None:
    pygame.init()

    start_searching = False
    start_dijkstra = False
    start_a_star = False
    start_defined = False
    target_defined = False
    target_box = None
    start_box = None

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Path Algorithm")

    grid = make_grid(columns=columns, rows=rows)
    set_neighbours(grid=grid, columns=columns, rows=rows)
    queue = []
    path = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Mouse Pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not start_searching:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                    # Define start box
                    if event.button == 1 and not start_defined:
                        i = x // box_width
                        j = y // box_height
                        start_box = grid[i][j]
                        start_box.start = True
                        start_defined = True
                        start_box.visited = True
                        queue.append(start_box)
                        print("Start defined.")

                    # Define target box
                    if event.button == 3 and start_defined and not target_defined:
                        i = x // box_width
                        j = y // box_height
                        target_box = grid[i][j]
                        target_box.target = True
                        target_defined = True
                        print("Target defined.")

            # Mouse Motion
            elif event.type == pygame.MOUSEMOTION:
                if not start_searching:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                    # Define walls
                    if event.buttons[2] and start_defined and target_defined:
                        i = x // box_width
                        j = y // box_height
                        if not grid[i][j].start and not grid[i][j].target:
                            grid[i][j].wall = True

            # Start Searching
            if event.type == pygame.KEYDOWN and start_defined and target_defined:
                start_searching = True
                if event.key == pygame.K_d:
                    start_dijkstra = True

                    print("Start Searching!")

                # TODO: Add other path finding algorithms

            # Reset
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start_searching = False
                    start_dijkstra = False
                    start_defined = False
                    target_defined = False
                    target_box = None
                    start_box = None
                    queue = []
                    path = []
                    reset_grid(grid, columns, rows)
                    set_neighbours(grid, columns, rows)

        # Run dijkstra path finding algorithm:
        if start_searching:
            if start_dijkstra:
                dijkstra(queue=queue, path=path, start_box=start_box, target_box=target_box)
            if start_a_star:
                # TODO: implement a star algorithm
                pass

        window.fill((0, 0, 0))

        draw_grid(window, grid, columns, rows, path)

        pygame.display.flip()


if __name__ == "__main__":
    main()
