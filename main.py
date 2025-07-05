import pygame, grid, machine

#Basic Pygame Initialization (Screen Size, Clock, Loop, Delta Time)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

game_grid = grid.GRID(screen)
machine = machine.MACHINE(screen, game_grid)

font = pygame.font.Font('main_font.ttf', 20)
money_text = font.render("$ 000.00", True, "green")
money_text_rect = money_text.get_rect()
money_text_rect.center = (100, screen.get_height() - 40)

#Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    power_draw_text = font.render(f"Power Draw: {machine.power_draw} watt/sec  |  Current Power: {int(machine.current_power)}", True, "Red")
    power_draw_text_rect = money_text.get_rect()
    power_draw_text_rect.center = (400, screen.get_height() - 40)


    screen.fill("black")
    game_grid.draw_grid()
    machine.draw_machine()
    machine.update_machine(dt, )
    screen.blit(money_text, money_text_rect)
    screen.blit(power_draw_text, power_draw_text_rect)
    pygame.display.update()
    dt = clock.tick(60) / 1000

pygame.quit()