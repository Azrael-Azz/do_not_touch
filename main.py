import pygame   # Game framework for graphics, input, and events
import random   # For randomizing positions of fruit and enemies
import os       # For saving and loading high score

pygame.init()

# Screen and frame setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60  # Frames per second
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Don't Let it Touch U")
clock = pygame.time.Clock()

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("monospace", 35, bold=True)
small_font = pygame.font.SysFont("monospace", 25)

# Game variables
player_size = 30
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

fruit_size = 20
fruit_pos = [random.randint(0, SCREEN_WIDTH - fruit_size),
             random.randint(0, SCREEN_HEIGHT - fruit_size)]

enemy_size = 30
enemies = []
base_enemy_speed = 2
max_enemies = 5

score = 0
high_score = 0
game_over = False

# File for saving high score (relative path)
HIGH_SCORE_FILE = "highscore.txt"


def create_enemy():
    # Create a new enemy at random position with speed scaling with score
    enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size),
                 random.randint(0, SCREEN_HEIGHT - enemy_size)]

    current_speed = base_enemy_speed + (score // 5) * 0.5
    enemy_speed = [random.choice([-current_speed, current_speed]),
                   random.choice([-current_speed, current_speed])]

    return {"pos": enemy_pos, "speed": enemy_speed}


def detect_collision(player_pos, player_size, object_pos, object_size):
    # Check if two rectangular objects collide
    p_x, p_y = player_pos
    o_x, o_y = object_pos

    return (p_x < o_x + object_size and
            p_x + player_size > o_x and
            p_y < o_y + object_size and
            p_y + player_size > o_y)


def update_enemy_count():
    # Increase number of enemies based on score, capped at max_enemies
    target_enemies = min(1 + score // 3, max_enemies)
    while len(enemies) < target_enemies:
        enemies.append(create_enemy())


def update_enemy_speeds():
    # Update enemy speed based on score while preserving direction
    current_speed = base_enemy_speed + (score // 5) * 0.5
    for enemy in enemies:
        enemy["speed"][0] = current_speed if enemy["speed"][0] > 0 else -current_speed
        enemy["speed"][1] = current_speed if enemy["speed"][1] > 0 else -current_speed


def reset_game():
    # Reset game state after Game Over
    global player_pos, fruit_pos, score, game_over, enemies
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    fruit_pos = [random.randint(0, SCREEN_WIDTH - fruit_size),
                 random.randint(0, SCREEN_HEIGHT - fruit_size)]
    score = 0
    game_over = False
    enemies.clear()
    enemies.append(create_enemy())


def handle_player_movement():
    # Move player based on keyboard input (WASD)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_UP] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - player_size:
        player_pos[1] += player_speed


def handle_enemy_movement():
    # Move enemies and bounce them off screen edges
    for enemy in enemies:
        enemy["pos"][0] += enemy["speed"][0]
        enemy["pos"][1] += enemy["speed"][1]

        if enemy["pos"][0] <= 0 or enemy["pos"][0] >= SCREEN_WIDTH - enemy_size:
            enemy["speed"][0] = -enemy["speed"][0]
        if enemy["pos"][1] <= 0 or enemy["pos"][1] >= SCREEN_HEIGHT - enemy_size:
            enemy["speed"][1] = -enemy["speed"][1]


def handle_fruit_collection():
    # Check if player collects fruit, then increase score and difficulty
    global fruit_pos, score
    if detect_collision(player_pos, player_size, fruit_pos, fruit_size):
        score += 1
        fruit_pos = [random.randint(0, SCREEN_WIDTH - fruit_size),
                     random.randint(0, SCREEN_HEIGHT - fruit_size)]
        update_enemy_count()
        update_enemy_speeds()


def check_enemy_collision():
    # End game if player collides with enemy, update high score
    global game_over, high_score
    for enemy in enemies:
        if detect_collision(player_pos, player_size, enemy["pos"], enemy_size):
            game_over = True
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            break


def load_high_score():
    # Load high score from file, fallback to 0 if missing/corrupted
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0


def save_high_score(score):
    # Save high score to file
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


high_score = load_high_score()


def draw_game():
    # Render all game elements and UI
    screen.fill(BLACK)

    if not game_over:
        pygame.draw.rect(screen, BLUE, (*player_pos,
                         player_size, player_size))  # Player
        pygame.draw.circle(screen, YELLOW,  # Fruit
                           (fruit_pos[0] + fruit_size // 2,
                            fruit_pos[1] + fruit_size // 2),
                           fruit_size // 2)
        for enemy in enemies:  # Enemies
            pygame.draw.rect(
                screen, RED, (*enemy["pos"], enemy_size, enemy_size))
    else:
        game_over_text = font.render("GAME OVER!", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                     SCREEN_HEIGHT // 2 - 80))

        current_score_text = small_font.render(f"Score: {score}", True, WHITE)
        screen.blit(current_score_text, (SCREEN_WIDTH // 2 - current_score_text.get_width() // 2,
                                         SCREEN_HEIGHT // 2 - 40))

        high_score_text = small_font.render(
            f"High Score: {high_score}", True, YELLOW)
        screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2,
                                      SCREEN_HEIGHT // 2 - 10))

        restart_text = small_font.render("Press Ctrl to restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2 + 30))

    # Always show score at top-left
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()


# Main game loop
enemies.append(create_enemy())  # Start with one enemy
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LCTRL, pygame.K_RCTRL) and game_over:
                reset_game()

    if not game_over:
        handle_player_movement()
        handle_enemy_movement()
        handle_fruit_collection()
        check_enemy_collision()

    draw_game()
    clock.tick(FPS)

pygame.quit()
