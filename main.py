import pygame, grid, machine

#Basic Pygame Initialization (Screen Size, Clock, Loop, Delta Time)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

#0 = battery, 1 = trace, 2 = upgrade, 3 = delete
mode = 0

game_grid = grid.GRID(screen)
machine = machine.MACHINE(screen, game_grid)

font = pygame.font.Font('main_font.ttf', 20)

#Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB:
                if mode != 3:
                    mode += 1
                else:
                    mode = 0


    money_text = font.render(f"${machine.money:03d}", True, "green")
    money_text_rect = money_text.get_rect()
    money_text_rect.center = (100, screen.get_height() - 40)

    power_draw_text = font.render(f"Power Draw: {machine.power_draw} watt/sec  |  Current Power: {int(machine.current_power)}", True, "Red")
    power_draw_text_rect = money_text.get_rect()
    power_draw_text_rect.center = (400, screen.get_height() - 40)

    mouse_click = pygame.mouse.get_pressed()
    if mouse_click[0] == 1:
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] / game_grid.cell_size <= game_grid.columns and mouse_pos[1] / game_grid.cell_size <= game_grid.rows:
            if machine.money >= machine.battery_cost and machine.power_draw >= machine.battery_production and mode == 0 and game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] != 2:
                machine.money -= machine.battery_cost
                machine.power_draw -= machine.battery_production
                game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] = 2
            if mode == 1 and game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] != 3 and game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] != 2:
                if machine.money - machine.trace_cost >= 0:
                    machine.money -= machine.trace_cost
                    game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] = 3
            if mode == 2 and game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] == 2 and game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] != 4:
                machine.money -= machine.battery_upgrade
                machine.power_draw -= machine.battery_production_upgrade
                game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] = 4
            if mode == 3 and game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] != 0 and game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] != 1:
                if game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] == 2:
                    machine.money += int(machine.battery_cost / 2)
                elif game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] == 3:
                    machine.money += int(machine.trace_cost / 2)
                elif game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][
                    int(mouse_pos[0] / game_grid.cell_size)] == 4:
                    machine.money += int(machine.battery_upgrade / 2)
                game_grid.grid[int(mouse_pos[1] / game_grid.cell_size)][int(mouse_pos[0] / game_grid.cell_size)] = 0

    screen.fill("black")
    game_grid.draw_grid()
    machine.draw_machine()
    machine.update_machine(dt, )
    screen.blit(money_text, money_text_rect)
    screen.blit(power_draw_text, power_draw_text_rect)
    pygame.display.update()
    dt = clock.tick(60) / 1000

pygame.quit()