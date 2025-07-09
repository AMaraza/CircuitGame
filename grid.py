import pygame
from collections import deque

# Constants for grid tile types
EMPTY = 0
MACHINE = 1
BATTERY = 2
TRACE = 3
UPGRADED_BATTERY = 4

class GRID:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 40
        self.columns = screen.get_width() // self.cell_size
        self.rows = (screen.get_height() - self.cell_size * 2) // self.cell_size

        # 2D grid initialized with EMPTY tiles
        self.grid = [[EMPTY for _ in range(self.columns)] for _ in range(self.rows)]

    def is_connected_to_machine(self, start_row, start_col):
        visited = set()
        queue = deque([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()
            if (row, col) in visited:
                continue
            visited.add((row, col))

            tile = self.grid[row][col]
            if tile == MACHINE:
                return True
            if tile not in (BATTERY, TRACE, UPGRADED_BATTERY):
                continue

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.columns:
                    queue.append((nr, nc))

        return False

    def get_connected_battery_type(self, start_row, start_col):
        visited = set()
        queue = deque([(start_row, start_col)])

        while queue:
            row, col = queue.popleft()
            if (row, col) in visited:
                continue
            visited.add((row, col))

            tile = self.grid[row][col]
            if tile == BATTERY:
                return "battery"
            elif tile == UPGRADED_BATTERY:
                return "upgraded"
            elif tile not in (TRACE, MACHINE):
                continue

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.columns:
                    queue.append((nr, nc))

        return "none"

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.columns):
                x = col * self.cell_size
                y = row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                tile = self.grid[row][col]
                color = {
                    EMPTY: "black",
                    MACHINE: "red",
                    BATTERY: "green",
                    TRACE: "yellow",
                    UPGRADED_BATTERY: "orange"
                }.get(tile, "white")

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, "gray", rect, 1)  # grid border
