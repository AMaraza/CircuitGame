import asyncio
import pygame
import grid, machine
from tiletypes import EMPTY, MACHINE, BATTERY, TRACE, UPGRADED_BATTERY

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

place_battery_sound = pygame.mixer.Sound("sounds/placebattery.wav")
place_trace_sound = pygame.mixer.Sound("sounds/placetrace.wav")
upgrade_sound = pygame.mixer.Sound("sounds/upgrade.wav")
delete_sound = pygame.mixer.Sound("sounds/delete.wav")
delete_sound.set_volume(1.5)
connect_sound = pygame.mixer.Sound("sounds/connected.wav")
disconnect_sound = pygame.mixer.Sound("sounds/disconnect.wav")

game_grid = grid.GRID(screen)
machine = machine.MachineCore(screen, game_grid, connect_sound, disconnect_sound)
font = pygame.font.Font('main_font.ttf', 20)
smaller_font = pygame.font.Font('main_font.ttf', 13)





def get_mouse_tile():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col = int(mouse_x / game_grid.cell_size)
    row = int(mouse_y / game_grid.cell_size)
    return row, col

def is_near_machine(row, col, machine_positions, radius = 2):
    for mr, mc in machine_positions:
        if abs(row - mr) <= radius and abs(col - mc) <= radius:
            return True

    return False

async def main():
    mode = 0  # MODE_BATTERY
    running = True
    dt = 0

    def place_battery(row, col):
        if game_grid.grid[row][col] != EMPTY:
            return
        if machine.money < machine.battery_cost:
            return
        if is_near_machine(row, col, machine.machine_positions):
            return
        machine.money -= machine.battery_cost
        game_grid.grid[row][col] = BATTERY
        place_battery_sound.play()
        machine.recalculate_power_draw()

    def place_trace(row, col):
        if game_grid.grid[row][col] != EMPTY:
            return
        if machine.money < machine.trace_cost:
            return
        machine.money -= machine.trace_cost
        game_grid.grid[row][col] = TRACE
        place_trace_sound.play()
        machine.recalculate_power_draw()

    def upgrade_battery(row, col):
        if game_grid.grid[row][col] != BATTERY:
            return
        if machine.money < machine.battery_upgrade:
            return
        machine.money -= machine.battery_upgrade
        game_grid.grid[row][col] = UPGRADED_BATTERY
        upgrade_sound.play()
        machine.recalculate_power_draw()

    def delete_tile(row, col):
        tile = game_grid.grid[row][col]
        if tile == EMPTY or tile == MACHINE:
            return

        if tile == BATTERY:
            machine.money += machine.battery_cost // 2
        elif tile == TRACE:
            machine.money += machine.trace_cost // 2
        elif tile == UPGRADED_BATTERY:
            machine.money += machine.battery_upgrade // 2

        game_grid.grid[row][col] = EMPTY
        delete_sound.play()
        machine.recalculate_power_draw()

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYUP and event.key == pygame.K_TAB:
                mode = (mode + 1) % 4

        if pygame.mouse.get_pressed()[0]:
            row, col = get_mouse_tile()
            if 0 <= row < game_grid.rows and 0 <= col < game_grid.columns:
                if mode == 0:
                    place_battery(row, col)
                elif mode == 1:
                    place_trace(row, col)
                elif mode == 2:
                    upgrade_battery(row, col)
                elif mode == 3:
                    delete_tile(row, col)

        screen.fill("black")
        game_grid.draw_grid()
        machine.draw_machine()
        machine.update_machine(dt)

        hover_row, hover_col = get_mouse_tile()
        if (
                0 <= hover_row < game_grid.rows and
                0 <= hover_col < game_grid.columns and
                game_grid.grid[hover_row][hover_col] == EMPTY
        ):
            near_machine = is_near_machine(hover_row, hover_col, machine.machine_positions)
            color = "red" if mode == 0 and near_machine else "white"

            hover_rect = pygame.Rect(
                hover_col * game_grid.cell_size,
                hover_row * game_grid.cell_size,
                game_grid.cell_size,
                game_grid.cell_size
            )
            pygame.draw.rect(screen, color, hover_rect, 2)

        money_text = font.render(f"${machine.money:03d}", True, "green")
        money_rect = money_text.get_rect(center=(100, screen.get_height() - 40))
        screen.blit(money_text, money_rect)

        power_text = font.render(f"Power Loss: {machine.power_draw} Watts  |  Current Power: {int(machine.current_power)}", True, "red")
        power_rect = power_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 40))
        screen.blit(power_text, power_rect)

        switch_text = smaller_font.render(f"[TAB] to Switch Modes", True, "green")
        switch_rect = switch_text.get_rect(center=(screen.get_width() - 150, screen.get_height() - 42))
        screen.blit(switch_text, switch_rect)

        # Mode text UI
        if mode == 0:
            mode_text = smaller_font.render(f"Mode: Battery", True, "green", "black")
            mode_rect = mode_text.get_rect(center=(mouse_x, mouse_y + 40))
            money_text = smaller_font.render(f"-${machine.battery_cost}", True, "red", "black")
            money_rect = mode_text.get_rect(center=(mouse_x + money_text.get_width(), mouse_y + 60))
            screen.blit(mode_text, mode_rect)
            screen.blit(money_text, money_rect)
        elif mode == 1:
            mode_text = smaller_font.render(f"Mode: Trace", True, "green", "black")
            mode_rect = mode_text.get_rect(center=(mouse_x, mouse_y + 40))
            money_text = smaller_font.render(f"-${machine.trace_cost}", True, "red", "black")
            money_rect = mode_text.get_rect(center=(mouse_x + money_text.get_width(), mouse_y + 60))
            screen.blit(mode_text, mode_rect)
            screen.blit(money_text, money_rect)
        elif mode == 2:
            mode_text = smaller_font.render(f"Mode: Upgrade", True, "green", "black")
            mode_rect = mode_text.get_rect(center=(mouse_x, mouse_y + 40))
            money_text = smaller_font.render(f"-${machine.battery_upgrade}", True, "red", "black")
            money_rect = mode_text.get_rect(center=(mouse_x + money_text.get_width(), mouse_y + 60))
            screen.blit(mode_text, mode_rect)
            screen.blit(money_text, money_rect)
        elif mode == 3:
            mode_text = smaller_font.render(f"Mode: Delete", True, "green", "black")
            mode_rect = mode_text.get_rect(center=(mouse_x, mouse_y + 40))
            screen.blit(mode_text, mode_rect)

        pygame.display.update()

        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)  # Yield control for async compatibility

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
