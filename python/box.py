import pygame


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

    def set_neighbours(self, grid, columns, rows):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y])
        if self.x < columns - 1:
            self.neighbours.append(grid[self.x + 1][self.y])

        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

    def draw(self, window, color, box_width, box_height):
        """Draw the box."""
        pygame.draw.rect(window, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))