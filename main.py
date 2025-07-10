import asyncio
import pygame
import grid, machine, menu
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
error_sound = pygame.mixer.Sound("sounds/error.wav")
error_sound.set_volume(0.2)
low_power_sound = pygame.mixer.Sound("sounds/lowpowersound.wav")
low_power_sound.set_volume(0.2)
game_over_sound = pygame.mixer.Sound("sounds/gameoversound.wav")
game_over_sound.set_volume(0.5)
machine_place_sound = pygame.mixer.Sound("sounds/newmachine.wav")
pygame.mixer.music.load("sounds/menu.wav")
pygame.mixer.music.set_volume(0.7)

game_grid = grid.GRID(screen)
game_menu = menu.MENU(screen)
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
    game_state = 0  # 0 = menu, 1 = tutorial, 3 = gameplay, 4 = win
    prev_game_state = None
    mouse_held = False

    highlight_x = 0
    highlight_speed = 150  # pixels per second
    panel_width = game_grid.cell_size * 3
    panel_height = game_grid.cell_size * game_grid.rows

    flash_red = False
    flash_start_time = 0
    flash_duration = 1000
    low_power_triggered = False

    game_over_played = False


    game_time = 0

    def place_battery(row, col):
        if game_grid.grid[row][col] != EMPTY:
            error_sound.play()
            return
        if machine.money < machine.battery_cost:
            error_sound.play()
            return
        if is_near_machine(row, col, machine.machine_positions):
            error_sound.play()
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
            error_sound.play()
            return
        if machine.money < machine.battery_upgrade:
            error_sound.play()
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

        if game_state != prev_game_state:
            # Only run this block once per state change
            if game_state == 0:
                pygame.mixer.music.load("sounds/menu.wav")
                pygame.mixer.music.play(-1)
            elif game_state == 3:
                pygame.mixer.music.load("sounds/game.wav")
                pygame.mixer.music.play(-1)

            prev_game_state = game_state  # Update the tracker

        if game_state == 0:
            menu_grid = grid.GRID(screen)
            screen.fill("Black")
            menu_grid.draw_grid()
            highlight_x += highlight_speed * dt
            if highlight_x > screen.get_width():
                highlight_x = -panel_width

            highlight_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
            highlight_surface.fill((0, 255, 0, 80))  # White with 80 alpha
            screen.blit(highlight_surface, (highlight_x, 0))

            game_menu.draw_menu()

            author_text = font.render("Made by Ally Maraza | Made Using Pygame", True, "White")
            author_rect = author_text.get_rect(center=(screen.get_width() / 2, screen.get_height() - 40))
            screen.blit(author_text, author_rect)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    if game_menu.play_button_rect.collidepoint(event.pos):
                        game_state = 3
            pygame.display.update()


        elif game_state == 3:
            game_time += 1 * dt
            if machine.current_power == 0:
                game_state = 4
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYUP and event.key == pygame.K_TAB:
                    mode = (mode + 1) % 4

            # Check mouse press state
            if pygame.mouse.get_pressed()[0]:
                row, col = get_mouse_tile()

                # Only trigger once per press
                if not mouse_held:
                    mouse_held = True
                    if 0 <= row < game_grid.rows and 0 <= col < game_grid.columns:
                        if mode == 0:
                            place_battery(row, col)
                        elif mode == 1:
                            place_trace(row, col)
                        elif mode == 2:
                            upgrade_battery(row, col)
                        elif mode == 3:
                            delete_tile(row, col)

                # For trace (mode 1), allow dragging while held
                elif mode == 1:
                    if 0 <= row < game_grid.rows and 0 <= col < game_grid.columns:
                        place_trace(row, col)

            else:
                mouse_held = False

            screen.fill("black")
            game_grid.draw_grid()
            machine.draw_machine()
            machine.update_machine(dt, machine_place_sound)

            current_time = pygame.time.get_ticks()

            if machine.current_power <= 10:
                if not low_power_triggered:
                    flash_red = True
                    flash_start_time = current_time
                    low_power_triggered = True
                    low_power_sound.play()
            elif machine.current_power > 10:
                low_power_triggered = False
                flash_red = False  # Reset if power goes back up

            # Turn off flashing after duration
            if flash_red and current_time - flash_start_time >= flash_duration:
                flash_red = False

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

            money_text = font.render(f"${machine.money:.2f}", True, "green")
            money_rect = money_text.get_rect(center=(100, screen.get_height() - 40))
            screen.blit(money_text, money_rect)

            power_text = font.render(f"Power Loss: {machine.power_draw:.1f} Watts  |  Current Power: {int(machine.current_power)}", True, "red")
            power_rect = power_text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 40))
            screen.blit(power_text, power_rect)

            switch_text = smaller_font.render(f"[TAB] to Switch Modes", True, "green")
            switch_rect = switch_text.get_rect(center=(screen.get_width() - 150, screen.get_height() - 42))
            screen.blit(switch_text, switch_rect)

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

            if flash_red:
                overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                overlay.fill((255, 0, 0, 100))  # semi-transparent red
                screen.blit(overlay, (0, 0))

            pygame.display.update()

        elif game_state == 4:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not game_over_played:
                pygame.mixer.music.stop()
                game_over_sound.play()
                game_over_played = True

            screen.fill("Black")
            game_grid.draw_grid()
            game_menu.draw_game_over(game_time)
            pygame.display.update()

        dt = clock.tick(60) / 1000
        await asyncio.sleep(0)  # Yield control for async compatibility

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())
