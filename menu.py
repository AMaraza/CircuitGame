import pygame

class MENU:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('main_font.ttf', 45)
        self.button_font = pygame.font.Font('main_font.ttf', 20)
        self.title = self.font.render("Livewire", True, "White", "Black")
        self.title_rect = self.title.get_rect()
        self.title_rect.center = (self.screen.get_width() / 2, 200)


        self.play_button_rect = pygame.Rect(0, 0, 175, 50)
        self.play_button_rect.center = (screen.get_width() / 2, screen.get_height() / 2)

        self.play_text = self.button_font.render("Play", True, "Black")
        self.play_text_rect = self.play_text.get_rect()
        self.play_text_rect.center = self.play_button_rect.center

    def draw_menu(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.play_button_rect.collidepoint(mouse_pos):
            button_color = (0, 150, 0)
        else:
            button_color = (0, 255, 0)

        pygame.draw.rect(self.screen, button_color, self.play_button_rect, 0, 5)
        self.screen.blit(self.play_text, self.play_text_rect)
        self.screen.blit(self.title, self.title_rect)
