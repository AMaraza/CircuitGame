import pygame, os

class MACHINE:
    def __init__(self, screen, grid):
        #Position Initializing
        self.screen = screen
        self.grid = grid
        self.top_left_grid_row = (grid.rows // 2) - 1
        self.top_left_grid_col = (grid.columns // 2) - 1

        #Functional Variables
        self.max_power = 20
        self.current_power = self.max_power
        self.power_draw = 2
        self.power_tick = 0

        self.money = 100
        self.battery_cost = 20
        self.battery_production = 1
        self.battery_production_upgrade = 5
        self.battery_upgrade = 50

        self.trace_cost = 5

    def draw_machine(self):
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                if i == self.top_left_grid_row and j == self.top_left_grid_col:
                    self.grid.grid[i][j] = 1
                    self.grid.grid[i][j + 1] = 1
                    self.grid.grid[i+1][j] = 1
                    self.grid.grid[i + 1][j + 1] = 1

    def update_machine(self, dt):
        if self.current_power > 0:
            self.current_power -= self.power_draw * dt
