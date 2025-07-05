import pygame

class GRID:
    def __init__(self, screen):
        #Define Grid Traits
        self.cell_size = 40
        self.columns = int(screen.get_width() / self.cell_size)
        self.rows = int((screen.get_height() - (self.cell_size * 2)) / self.cell_size)
        self.grid = []
        self.screen = screen

        #Populate Grid List
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                row.append(0)
            self.grid.append(row)

    def draw_grid(self):
        #Draw grid with borderlines
        for i in range(self.rows):
            for j in range(self.columns):
                x = j * self.cell_size
                y = i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, "gray", rect, 1)

                if self.grid[i][j] == 1:
                    rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                    pygame.draw.rect(self.screen, "red", rect)
