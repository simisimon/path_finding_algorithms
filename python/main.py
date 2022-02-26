import sys
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
        self.queued = False
        self.visited = False
        self.neighbours = []
        self.prior = None

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(GRID[self.x - 1][self.y])
        if self.x < COLUMNS - 1:
            self.neighbours.append(GRID[self.x + 1][self.y])

        if self.y > 0:
            self.neighbours.append(GRID[self.x][self.y - 1])
        if self.y < ROWS - 1:
            self.neighbours.append(GRID[self.x][self.y + 1])

    def draw(self, window, color):
        """Draw the box."""
        pygame.draw.rect(window, color, (self.x * BOX_WIDTH, self.y * BOX_HEIGHT, BOX_WIDTH - MARGIN, BOX_HEIGHT - MARGIN))


# Define grid
for i in range(COLUMNS):
    arr = []
    for j in range(ROWS):
        arr.append(Box(i, j))
    GRID.append(arr)


# Set neighbours
for i in range(COLUMNS):
    for j in range(ROWS):
        GRID[i][j].set_neighbours()


def main() -> None:
    pygame.init()

    start_dijkstra = False
    searching = True
    start_defined = False
    target_defined = False
    target_box = None
    start_box = None

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
                    start_box.visited = True
                    QUEUE.append(start_box)
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
                if event.key == pygame.K_d:
                    start_dijkstra = True
                    print("Start Searching!")

                # TODO: Add other path finding algorithms

        # Run dijkstra path finding algorithm:
        if start_dijkstra:
            if len(QUEUE) > 0 and searching:
                current_box = QUEUE.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = True
                    while current_box.prior != start_box:
                        PATH.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.prior = current_box
                            neighbour.queued = True
                            QUEUE.append(neighbour)

            else:
                if searching:
                    print("There is no solution found.")
                    searching = False

        window.fill((0, 0, 0))

        for i in range(COLUMNS):
            for j in range(ROWS):
                box = GRID[i][j]
                box.draw(window, BACKGROUND_COLOR)

                if box.queued:
                    box.draw(window, QUEUED_COLOR)
                if box.visited:
                    box.draw(window, VISITED_COLOR)
                if box in PATH:
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
