import pygame  # to create the game frame, define game logic, player movements
import random  # to make the maps, enemies and fruit position random
import os  # to save high score in file

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Don't Let it Touch U")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont('monospace', 35)
small_font = pygame.font.SysFont('monospace', 25)


# Variables Description
player_size = 30
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player_speed = 5

fruit_size = 20
fruit_pos = [random.randint(0, SCREEN_WIDTH - fruit_size),
             random.randint(0, SCREEN_HEIGHT - fruit_size)]

enemy_size = 30
enemies = []  # List of enemies
base_enemy_speed = 2
max_enemies = 5

score = 0
high_score = 0
game_over = False
HIGH_SCORE_FILE = "C:/Users/acer/Desktop/My Coding Projects/Don'tLetItTouchYou_Game_Python/highscore.txt"


# Functions
# To Create Enemy at random Location other than where player is located
def create_enemy():
    # Create a new enemy at a random position with speed scaling with score
    enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size),
                 random.randint(0, SCREEN_HEIGHT - enemy_size)]

    # Enemy speed increases slightly as score increases
    current_speed = base_enemy_speed + (score // 5) * 0.5
    enemy_speed = [random.choice([-current_speed, current_speed]),
                   random.choice([-current_speed, current_speed])]

    return {'pos': enemy_pos, 'speed': enemy_speed}


# To Detect Collision with other Objects
def detect_collision(player_pos, player_size, object_pos, object_size):
    p_x, p_y = player_pos
    o_x, o_y = object_pos

    return (p_x < o_x + object_size and
            p_x + player_size > o_x and
            p_y < o_y + object_size and
            p_y + player_size > o_y)


# To Increase Enemy Count
def update_enemy_count():
    # Increase number of enemies as score grows max at 5
    target_enemies = min(
        1 + score // 3, max_enemies)  # Add 1 enemy every 3 points
    while len(enemies) < target_enemies:
        enemies.append(create_enemy())


# To Increase Enemy Speed
def update_enemy_speeds():
    # Adjust enemy speeds based on current score, keeping their direction
    current_speed = base_enemy_speed + (score // 5) * 0.5
    for enemy in enemies:
        enemy['speed'][0] = current_speed if enemy['speed'][0] > 0 else -current_speed
        enemy['speed'][1] = current_speed if enemy['speed'][1] > 0 else -current_speed


# To Reset Game
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


# Logic Functions
def handle_player_movement():
    # Move player based on key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < SCREEN_WIDTH - player_size:
        player_pos[0] += player_speed
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] < SCREEN_HEIGHT - player_size:
        player_pos[1] += player_speed


# For Enemy Movement
def handle_enemy_movement():
    # Move enemies and bounce them off walls
    for enemy in enemies:
        enemy['pos'][0] += enemy['speed'][0]
        enemy['pos'][1] += enemy['speed'][1]

        # Bounce off walls
        if enemy['pos'][0] <= 0 or enemy['pos'][0] >= SCREEN_WIDTH - enemy_size:
            enemy['speed'][0] = -enemy['speed'][0]
        if enemy['pos'][1] <= 0 or enemy['pos'][1] >= SCREEN_HEIGHT - enemy_size:
            enemy['speed'][1] = -enemy['speed'][1]


# To Collect Fruit
def handle_fruit_collection():
    # Check if player collects fruit and update score and increase enemy count and speed
    global fruit_pos, score
    if detect_collision(player_pos, player_size, fruit_pos, fruit_size):
        score += 1
        fruit_pos = [random.randint(0, SCREEN_WIDTH - fruit_size),
                     random.randint(0, SCREEN_HEIGHT - fruit_size)]
        update_enemy_count()
        update_enemy_speeds()


# To Detect Collision with Enemy
def check_enemy_collision():
    # Check if player collides with any enemy
    global game_over, high_score
    for enemy in enemies:
        if detect_collision(player_pos, player_size, enemy['pos'], enemy_size):
            game_over = True
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            break


# Load the lastest high score for game launch
def load_high_score():
    # Load high score from file, or return 0 if file doesn't exist
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0  # fallback if file is empty/corrupted
    return 0


# Save the latest high score for next session in highscore.txt file
def save_high_score(score):
    # Save high score to file
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


high_score = load_high_score()


# To Draw UI
def draw_game():
    # Draw all game elements (player, fruit, enemies, score).
    screen.fill(BLACK)

    if not game_over:
        # Player
        pygame.draw.rect(screen, BLUE, (*player_pos, player_size, player_size))
        # fruit
        pygame.draw.circle(screen, YELLOW,
                           (fruit_pos[0] + fruit_size // 2,
                            fruit_pos[1] + fruit_size // 2),
                           fruit_size // 2)
        # Enemies
        for enemy in enemies:
            pygame.draw.rect(
                screen, RED, (*enemy['pos'], enemy_size, enemy_size))
    else:
        # Game Over screen
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

        restart_text = small_font.render(
            "Press LCtrl or RCtrl to restart", True, WHITE)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2 + 30))

    # Always show score at top-left
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()


# Main Game Loop
enemies.append(create_enemy())  # Start with one enemy
running = True

while running:
    # Handle events
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
    clock.tick(60)  # Maintain 60 FPS

pygame.quit()
