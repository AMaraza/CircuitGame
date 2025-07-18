import pygame
import random
from tiletypes import EMPTY, BATTERY, UPGRADED_BATTERY, MACHINE

class MachineCore:
    def __init__(self, screen, grid, connected_sound, disconnected_sound):
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

        self.connection_sound = connected_sound
        self.disconnection_sound = disconnected_sound
        self.previous_connections = {}  # {(row, col): True/False}

        self.machine_positions = []
        r, c = self.grid.rows // 2 - 1, self.grid.columns // 2 - 1
        self.machine_positions += [(r, c), (r+1, c), (r, c+1), (r+1, c+1)]

        # Power management
        self.max_power = 100
        self.current_power = self.max_power
        self.base_power_draw = 2
        self.power_draw = self.base_power_draw

        # Economy
        self.money = 45
        self.battery_cost = 15
        self.battery_production = 1
        self.battery_production_upgrade = 2.5
        self.battery_upgrade = 45
        self.trace_cost = 5

        self.time_since_power_increase = 0.0
        self.time_since_last_income = 0.0
        self.time_since_machine_spawn = 0.0

        self.machine_spawn_power_bonus = 30
        self.machine_spawn_power_draw_penalty = 3
        self.machines = 0
        self.spawn_time = 30

    from tiletypes import TRACE  # if not already imported

    def recalculate_power_draw(self):
        self.power_draw = self.base_power_draw

        current_connections = {}

        for row in range(self.grid.rows):
            for col in range(self.grid.columns):
                tile = self.grid.grid[row][col]
                pos = (row, col)
                if tile in (BATTERY, UPGRADED_BATTERY):
                    connected = self.grid.is_connected_to_machine(row, col, self.machine_positions)
                    current_connections[pos] = connected

                    # Compare with previous state
                    was_connected = self.previous_connections.get(pos, False)

                    if connected and not was_connected:
                        self.connection_sound.play()  # connection sound
                    elif not connected and was_connected:
                        self.disconnection_sound.play()  # disconnection sound

                    # Subtract power only if connected
                    if connected:
                        if tile == BATTERY:
                            self.power_draw -= self.battery_production
                        else:
                            self.power_draw -= (self.battery_production + self.battery_production_upgrade)

        self.previous_connections = current_connections
        self.power_draw = max(0, self.power_draw)

    def draw_machine(self):
        for row, col in self.machine_tiles:
            self.grid.grid[row][col] = MACHINE

    def total_battery_output(self):
        output = 0
        visited = set()

        for row in range(self.grid.rows):
            for col in range(self.grid.columns):
                tile = self.grid.grid[row][col]
                if tile in (BATTERY, UPGRADED_BATTERY) and (row, col) not in visited:
                    if self.grid.is_connected_to_machine(row, col, self.machine_positions):
                        visited.add((row, col))
                        if tile == BATTERY:
                            output += self.battery_production
                        elif tile == UPGRADED_BATTERY:
                            output += self.battery_production_upgrade

        return output

    def find_spawn_position(self):
        max_row = self.grid.rows - 1
        max_column = self.grid.columns - 1

        spawn_row = random.randint(0, max_row)
        spawn_col = random.randint(0, max_column)

        while self.grid.grid[spawn_row][spawn_col] != EMPTY:
            spawn_row = random.randint(0, max_row)
            spawn_col = random.randint(0, max_column)

        return spawn_row, spawn_col

    def update_machine(self, dt, spawn_sound):
        if self.current_power > 0:
            self.current_power -= self.power_draw * dt
        else:
            self.current_power = 0

        self.time_since_power_increase += dt
        self.time_since_last_income += dt
        self.time_since_machine_spawn += dt

        if self.time_since_power_increase >= 25:
            self.time_since_power_increase = 0.0
            self.base_power_draw += 1
            self.recalculate_power_draw()

        if self.time_since_last_income >= 1.0:
            self.time_since_last_income = 0.0

            if self.power_draw > 0:
                income = 0
                upgraded_tiles = 0

                for row in range(self.grid.rows):
                    for col in range(self.grid.columns):
                        tile = self.grid.grid[row][col]
                        if self.grid.is_connected_to_machine(row, col, self.machine_positions):
                            if tile == BATTERY:
                                income += 1

                self.money += income

        if self.time_since_machine_spawn >= self.spawn_time:
            self.time_since_machine_spawn = 0
            self.machines += 1

            if self.machines > 5:
                self.machine_spawn_power_bonus = 20
                self.machine_spawn_power_draw_penalty = 4
            elif self.machines > 8:
                self.machine_spawn_power_bonus = 15
                self.machine_spawn_power_draw_penalty = 5
                self.spawn_time = 25
            spawn_sound.play()

            spawn_row, spawn_col = self.find_spawn_position()
            self.grid.grid[spawn_row][spawn_col] = MACHINE
            self.machine_positions.append((spawn_row, spawn_col))

            self.current_power += self.machine_spawn_power_bonus
            self.base_power_draw += self.machine_spawn_power_draw_penalty
            self.recalculate_power_draw()

    def reset(self):
        self.machine_positions = []
        self.top_left_grid_row = (self.grid.rows // 2) - 1
        self.top_left_grid_col = (self.grid.columns // 2) - 1
        self.machine_tiles = [
            (self.top_left_grid_row, self.top_left_grid_col),
            (self.top_left_grid_row, self.top_left_grid_col + 1),
            (self.top_left_grid_row + 1, self.top_left_grid_col),
            (self.top_left_grid_row + 1, self.top_left_grid_col + 1)
        ]
        self.machine_positions += list(self.machine_tiles)

        self.money = 45
        self.base_power_draw = 2
        self.power_draw = self.base_power_draw
        self.max_power = 100
        self.current_power = self.max_power
        self.previous_connections.clear()

        self.time_since_power_increase = 0.0
        self.time_since_last_income = 0.0
        self.time_since_machine_spawn = 0.0

        for row, col in self.machine_positions:
            self.grid.grid[row][col] = MACHINE

        self.recalculate_power_draw()
