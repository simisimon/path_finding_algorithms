import sys
from typing import List

import pygame

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
margin = 2

box_width = width // columns
box_height = height // rows

grid = []
queue = []
path = []


class Box:
    def __init__(self, i: int, j: int):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])

        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

    def draw(self, window, color):
        """Draw the box."""
        pygame.draw.rect(window, color, (self.x * box_width, self.y * box_height, box_width - margin, box_height - margin))


# Define grid
for i in range(columns):
    arr = []
    for j in range(rows):
        arr.append(Box(i, j))
    grid.append(arr)


# Set neighbours
for i in range(columns):
    for j in range(rows):
        grid[i][j].set_neighbours()


def main() -> None:
    pygame.init()

    start_searching = False
    searching = True
    start_defined = False
    target_defined = False
    target_box = None
    start_box = None

    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Path Algorithm")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Mouse Pressed
            elif event.type == pygame.MOUSEBUTTONDOWN:
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
                if event.key == pygame.K_SPACE:
                    start_searching = True
                    print("Start Searching!")

                # TODO: Add other path finding algorithms

        # Run dijkstra path finding algorithm:
        if start_searching:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = True
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.prior = current_box
                            neighbour.queued = True
                            queue.append(neighbour)

            else:
                if searching:
                    print("There is no solution found.")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(columns):
            for j in range(rows):
                box = grid[i][j]
                box.draw(window, BACKGROUND_COLOR)

                if box.queued:
                    box.draw(window, QUEUED_COLOR)
                if box.visited:
                    box.draw(window, VISITED_COLOR)
                if box in path:
                    box.draw(window, PATH_COLOR)
                if box.start:
                    box.draw(window, START_COLOR)
                if box.target:
                    box.draw(window, TARGET_COLOR)
                if box.wall:
                    box.draw(window, WALL_COLOR)

        pygame.display.flip()


if __name__ == "__main__":
    main()
