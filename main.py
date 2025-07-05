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

#Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    money_text = font.render(f"${machine.money:03d}", True, "green")
    money_text_rect = money_text.get_rect()
    money_text_rect.center = (100, screen.get_height() - 40)

    power_draw_text = font.render(f"Power Draw: {machine.power_draw} watt/sec  |  Current Power: {int(machine.current_power)}", True, "Red")
    power_draw_text_rect = money_text.get_rect()
    power_draw_text_rect.center = (400, screen.get_height() - 40)

    mouse_click = pygame.mouse.get_pressed()
    if mouse_click[0] == 1:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] / game_grid.cell_size <= game_grid.columns and mouse_pos[1] / game_grid.cell_size <= game_grid.rows and game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] != 2:
            if machine.money >= machine.battery_cost and machine.power_draw >= machine.battery_production:
                machine.money -= machine.battery_cost
                machine.power_draw -= machine.battery_production
                game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] = 2


    screen.fill("black")
    game_grid.draw_grid()
    machine.draw_machine()
    machine.update_machine(dt, )
    screen.blit(money_text, money_text_rect)
    screen.blit(power_draw_text, power_draw_text_rect)
    pygame.display.update()
    dt = clock.tick(60) / 1000

pygame.quit()