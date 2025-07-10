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

        self.game_over_text = self.font.render("Game Over", True, "White", "Black")
        self.game_over_text_rect = self.game_over_text.get_rect()
        self.game_over_text_rect.center = self.screen.get_width() / 2, 200

    def draw_menu(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.play_button_rect.collidepoint(mouse_pos):
            button_color = (0, 150, 0)
        else:
            button_color = (0, 255, 0)

        pygame.draw.rect(self.screen, button_color, self.play_button_rect, 0, 5)
        self.screen.blit(self.play_text, self.play_text_rect)
        self.screen.blit(self.title, self.title_rect)

    def draw_game_over(self, game_time):
        self.screen.blit(self.game_over_text, self.game_over_text_rect)

        minutes = int(game_time) // 60
        secs = int(game_time) % 60

        self.game_time_text = self.font.render(f"You survived for: {minutes:02}:{secs:02}", True, "White", "Black")
        self.game_time_text_rect = self.game_time_text.get_rect()
        self.game_time_text_rect.center = self.screen.get_width() / 2, self.screen.get_height() / 2
        self.screen.blit(self.game_time_text, self.game_time_text_rect)

