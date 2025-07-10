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

    def is_connected_to_machine(self, row, col, machine_positions):
        visited = set()
        stack = [(row, col)]

        while stack:
            r, c = stack.pop()
            if (r, c) in visited:
                continue
            visited.add((r, c))

            if (r, c) in machine_positions:
                return True

            for nr, nc in self.get_adjacent_cells(r, c):
                if self.grid[nr][nc] in [BATTERY, TRACE, UPGRADED_BATTERY, MACHINE] and (nr, nc) not in visited:
                    stack.append((nr, nc))
        return False

    def get_adjacent_cells(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [
            (row + dr, col + dc)
            for dr, dc in directions
            if 0 <= row + dr < self.rows and 0 <= col + dc < self.columns
        ]

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
                    UPGRADED_BATTERY: "orange",
                }.get(tile, "white")


                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, "gray", rect, 1)  # grid border
