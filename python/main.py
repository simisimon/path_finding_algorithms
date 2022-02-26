import sys

import pygame

# COLORS
DARK_GREY = (96, 96, 96)
GREY = (169, 169, 169)
LIGHT_GREEN = (144, 238, 144)
RED = (255, 0, 0)
GREEN = (51, 255, 51)
LIGHT_BLUE = (173, 216, 230)
YELLOW = (255, 255, 0)

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
COLUMNS = 25
ROWS = 25
MARGIN = 2

BOX_WIDTH = WINDOW_WIDTH // COLUMNS
BOX_HEIGHT = WINDOW_HEIGHT // ROWS

GRID = []
QUEUE = []
PATH = []


class Box:
    def __init__(self, i: int, j: int):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False

    def draw(self, window, color):
        """Draw the box."""
        pygame.draw.rect(window, color, (self.x * BOX_WIDTH, self.y * BOX_HEIGHT, BOX_WIDTH - MARGIN, BOX_HEIGHT - MARGIN))


for i in range(COLUMNS):
    arr = []
    for j in range(ROWS):
        arr.append(Box(i, j))
    GRID.append(arr)


def main() -> None:
    pygame.init()

    start_searching = False
    start_defined = False
    target_defined = False

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
                    i = x // BOX_WIDTH
                    j = y // BOX_HEIGHT
                    start_box = GRID[i][j]
                    start_box.start = True
                    start_defined = True
                    print("Start defined.")

                # Define target box
                if event.button == 3 and start_defined and not target_defined:
                    i = x // BOX_WIDTH
                    j = y // BOX_HEIGHT
                    target_box = GRID[i][j]
                    target_box.target = True
                    target_defined = True
                    print("Target defined.")

            # Mouse Motion
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                # Define walls
                if event.buttons[2] and start_defined and target_defined:
                    i = x // BOX_WIDTH
                    j = y // BOX_HEIGHT
                    if not GRID[i][j].start and not GRID[i][j].target:
                        GRID[i][j].wall = True

            # Start Searching
            if event.type == pygame.KEYDOWN and start_defined and target_defined:
                start_searching = True

        window.fill((0, 0, 0))

        for i in range(COLUMNS):
            for j in range(ROWS):
                box = GRID[i][j]
                box.draw(window, GREY)
                if box.start:
                    box.draw(window, YELLOW)
                if box.target:
                    box.draw(window, GREEN)
                if box.wall:
                    box.draw(window, DARK_GREY)

        pygame.display.flip()


if __name__ == "__main__":
    main()
