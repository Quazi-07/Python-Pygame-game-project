import pygame
import random
import time

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Screen setup for fullscreen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Pearland Soccer Craze")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREY = (100, 100, 100)

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 36)

# Load sounds
goal_sound = pygame.mixer.Sound("goal.wav")
save_sound = pygame.mixer.Sound("save.wav")

# Clock
clock = pygame.time.Clock()

# Game Constants
max_rounds = 5
directions = ["LEFT", "CENTER", "RIGHT"]

# Game State
players = []
player_name = ""
score = 0
rounds = 0
kicking = False
ball_x, ball_y = WIDTH // 2, HEIGHT - 100
target_x, target_y = ball_x, 100
player_dir = None
goalie_dir = None
goalie_pose = "CENTER"
result_text = ""
game_mode = "MENU"

def display_text(text, size, y, color=WHITE):
    font_obj = pygame.font.SysFont("Cambria", size)
    text_surface = font_obj.render(text, True, color)
    screen.blit(text_surface, text_surface.get_rect(center=(WIDTH // 2, y)))

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, GREY, (x, y, w, h))
    label = font.render(text, True, WHITE)
    screen.blit(label, (x + 10, y + 10))
    return pygame.Rect(x, y, w, h)

def draw_field():
    screen.fill(GREEN)
    goal_width = WIDTH * 0.5
    goal_left = (WIDTH - goal_width) // 2
    pygame.draw.rect(screen, WHITE, (goal_left, 50, goal_width, 100), 5)
    pygame.draw.line(screen, WHITE, (goal_left + goal_width / 3, 50), (goal_left + goal_width / 3, 150), 5)
    pygame.draw.line(screen, WHITE, (goal_left + 2 * goal_width / 3, 50), (goal_left + 2 * goal_width / 3, 150), 5)
    pygame.draw.circle(screen, BLACK, (int(ball_x), int(ball_y)), 15)

def draw_goalkeeper(direction):
    base_x = WIDTH // 2
    y = 140
    offset = 0
    if direction == "LEFT": offset = -WIDTH * 0.15
    elif direction == "RIGHT": offset = WIDTH * 0.15
    x = int(base_x + offset)
    pygame.draw.circle(screen, BLUE, (x, y), 10)
    pygame.draw.line(screen, BLUE, (x, y + 10), (x, y + 40), 3)
    pygame.draw.line(screen, BLUE, (x, y + 20), (x - 15, y + 30), 2)
    pygame.draw.line(screen, BLUE, (x, y + 20), (x + 15, y + 30), 2)
    pygame.draw.line(screen, BLUE, (x, y + 40), (x - 10, y + 60), 2)
    pygame.draw.line(screen, BLUE, (x, y + 40), (x + 10, y + 60), 2)

def get_player_name():
    name = ""
    active = True
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 30, 300, 50)
    while active:
        screen.fill(BLACK)
        display_text("Enter Player Name", 50, HEIGHT // 2 - 100)
        pygame.draw.rect(screen, WHITE, input_box, 2)
        txt_surface = font.render(name, True, WHITE)
        screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip() != "":
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 20:
                    name += event.unicode
        pygame.display.flip()
        clock.tick(30)

def display_footer():
    developer_text = "Developed by: Md. Saifur Rahman (Saif)"
    display_text(developer_text, 30, HEIGHT - 40, color=WHITE)

# Main Loop
running = True
while running:
    screen.fill(GREEN)

    if game_mode == "MENU":
        display_text("Pearland Soccer Craze", 60, 150)
        start_btn = draw_button("Start Game", WIDTH // 2 - 100, 250, 200, 60)
        exit_btn = draw_button("Exit", WIDTH // 2 - 100, 350, 200, 60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    player_name = get_player_name()
                    score = 0
                    rounds = 0
                    ball_x, ball_y = WIDTH // 2, HEIGHT - 100
                    goalie_pose = "CENTER"
                    game_mode = "GAME"
                elif exit_btn.collidepoint(event.pos):
                    running = False

        display_footer()  # Add this line to display the footer

    elif game_mode == "GAME":
        draw_field()
        draw_goalkeeper(goalie_pose)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not kicking and event.type == pygame.KEYDOWN and rounds < max_rounds:
                if event.key in [pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT]:
                    if event.key == pygame.K_LEFT:
                        player_dir = "LEFT"
                        target_x = WIDTH // 2 - WIDTH * 0.15
                    elif event.key == pygame.K_DOWN:
                        player_dir = "CENTER"
                        target_x = WIDTH // 2
                    elif event.key == pygame.K_RIGHT:
                        player_dir = "RIGHT"
                        target_x = WIDTH // 2 + WIDTH * 0.15
                    target_y = 100
                    goalie_dir = random.choice(directions)
                    goalie_pose = goalie_dir
                    kicking = True

        if kicking:
            dx, dy = target_x - ball_x, target_y - ball_y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            speed = 15
            if dist > speed:
                ball_x += speed * dx / dist
                ball_y += speed * dy / dist
            else:
                kicking = False
                if player_dir != goalie_dir:
                    score += 1
                    result_text = f"Goal! Goalie jumped {goalie_dir}"
                    goal_sound.play()
                else:
                    result_text = f"Saved! Goalie blocked {goalie_dir}"
                    save_sound.play()
                rounds += 1
                ball_x, ball_y = WIDTH // 2, HEIGHT - 100
                goalie_pose = "CENTER"
                time.sleep(0.5)
                if rounds == max_rounds:
                    players.append({"name": player_name, "score": score})
                    game_mode = "RESULTS"

        display_text(f"{player_name}'s Score: {score}", 40, 250)
        display_text(f"Round: {rounds}/{max_rounds}", 40, 300)
        display_text(" ", 40, 400)
        display_text("Press ← (left), ↓ (center), → (right) to Kick", 30, HEIGHT - 100)
        if result_text:
            display_text(result_text, 36, 350)

        display_footer()  # Add this line to display the footer

    elif game_mode == "RESULTS":
        screen.fill(BLACK)
        display_text("Game Over! Scores are:", 50, 80)
        y_offset = 150
        for p in players:
            display_text(f"{p['name']}: {p['score']}", 40, y_offset)
            y_offset += 50
        play_again_btn = draw_button("New Player", WIDTH // 2 - 100, y_offset + 30, 200, 50)
        exit_btn = draw_button("Exit", WIDTH // 2 - 100, y_offset + 100, 200, 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_btn.collidepoint(event.pos):
                    player_name = get_player_name()
                    score = 0
                    rounds = 0
                    ball_x, ball_y = WIDTH // 2, HEIGHT - 100
                    goalie_pose = "CENTER"
                    result_text = ""
                    game_mode = "GAME"
                elif exit_btn.collidepoint(event.pos):
                    running = False

        display_footer()  # Add this line to display the footer

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
