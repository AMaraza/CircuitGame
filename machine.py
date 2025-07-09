import pygame
from tiletypes import BATTERY, UPGRADED_BATTERY

class MACHINE:
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid

        # Machine is 2x2 square at center
        self.top_left_grid_row = (grid.rows // 2) - 1
        self.top_left_grid_col = (grid.columns // 2) - 1
        self.machine_tiles = [
            (self.top_left_grid_row, self.top_left_grid_col),
            (self.top_left_grid_row, self.top_left_grid_col + 1),
            (self.top_left_grid_row + 1, self.top_left_grid_col),
            (self.top_left_grid_row + 1, self.top_left_grid_col + 1)
        ]

        # Power management
        self.max_power = 20
        self.current_power = self.max_power
        self.base_power_draw = 2
        self.power_draw = self.base_power_draw  # starts at full draw

        # Economy
        self.money = 500
        self.battery_cost = 20
        self.battery_production = 1
        self.battery_production_upgrade = 5
        self.battery_upgrade = 50
        self.trace_cost = 5

    def draw_machine(self):
        for row, col in self.machine_tiles:
            self.grid.grid[row][col] = 1

    def update_machine(self, dt):
        if self.current_power > 0:
            self.current_power -= self.power_draw * dt
        else:
            self.current_power = 0

    def recalculate_power_draw(self):
        total_output = 0
        visited = set()

        for row in range(self.grid.rows):
            for col in range(self.grid.columns):
                tile = self.grid.grid[row][col]
                if tile in (BATTERY, UPGRADED_BATTERY) and (row, col) not in visited:
                    if self.grid.is_connected_to_machine(row, col):
                        visited.add((row, col))
                        if tile == BATTERY:
                            total_output += self.battery_production
                        elif tile == UPGRADED_BATTERY:
                            total_output += self.battery_production + self.battery_production_upgrade

        # New logic: base draw minus total output
        self.power_draw = max(0, self.base_power_draw - total_output)
