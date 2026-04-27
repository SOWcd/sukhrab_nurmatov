import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
GRAY = (80, 80, 80)
BLUE = (0, 120, 255)
YELLOW = (255, 220, 0)

# Font and clock
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 42)
clock = pygame.time.Clock()

# Game state
snake = [(100, 100), (80, 100), (60, 100)]
dx = CELL
dy = 0
score = 0
level = 1
speed = 8
game_over = False


def generate_walls(level_number):
    """Generate wall positions depending on the level."""
    walls = []

    # Level 2: horizontal wall in the center
    if level_number >= 2:
        for x in range(180, 420, CELL):
            walls.append((x, 300))

    # Level 3: vertical walls
    if level_number >= 3:
        for y in range(120, 260, CELL):
            walls.append((200, y))
            walls.append((380, y))

    # Level 4: lower walls
    if level_number >= 4:
        for y in range(360, 500, CELL):
            walls.append((200, y))
            walls.append((380, y))

    return walls


def generate_food(snake_body, wall_positions):
    """Generate food not on snake and not on walls."""
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        if (x, y) not in snake_body and (x, y) not in wall_positions:
            return (x, y)


def draw_grid():
    """Optional visible grid lines."""
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (35, 35, 35), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (35, 35, 35), (0, y), (WIDTH, y))


def draw_snake():
    """Draw snake body."""
    for i, segment in enumerate(snake):
        rect = pygame.Rect(segment[0], segment[1], CELL, CELL)
        color = BLUE if i == 0 else GREEN
        pygame.draw.rect(screen, color, rect, border_radius=4)


def draw_food(food_pos):
    """Draw food."""
    rect = pygame.Rect(food_pos[0], food_pos[1], CELL, CELL)
    pygame.draw.rect(screen, RED, rect, border_radius=10)


def draw_walls(wall_positions):
    """Draw walls."""
    for wall in wall_positions:
        rect = pygame.Rect(wall[0], wall[1], CELL, CELL)
        pygame.draw.rect(screen, GRAY, rect)


def draw_info():
    """Draw score and level."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, YELLOW)
    speed_text = font.render(f"Speed: {speed}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))
    screen.blit(speed_text, (10, 70))


def show_game_over():
    """Draw game over screen."""
    text1 = big_font.render("GAME OVER", True, WHITE)
    text2 = font.render("Press R to restart or Q to quit", True, WHITE)

    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 20))


def reset_game():
    """Reset all game values."""
    global snake, dx, dy, score, level, speed, walls, food, game_over
    snake = [(100, 100), (80, 100), (60, 100)]
    dx = CELL
    dy = 0
    score = 0
    level = 1
    speed = 8
    walls = generate_walls(level)
    food = generate_food(snake, walls)
    game_over = False


walls = generate_walls(level)
food = generate_food(snake, walls)

running = True
while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                # Prevent snake from moving directly backwards
                if event.key == pygame.K_UP and dy == 0:
                    dx = 0
                    dy = -CELL
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx = 0
                    dy = CELL
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx = -CELL
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = CELL
                    dy = 0
            else:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False

    if not game_over:
        # Compute new head position
        head_x, head_y = snake[0]
        new_head = (head_x + dx, head_y + dy)

        # Check border collision
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_over = True
        # Check self collision
        elif new_head in snake:
            game_over = True
        # Check wall collision
        elif new_head in walls:
            game_over = True
        else:
            snake.insert(0, new_head)

            # If snake eats food, increase score
            if new_head == food:
                score += 1

                # Increase level every 4 points
                new_level = score // 4 + 1
                if new_level > level:
                    level = new_level
                    speed += 2
                    walls = generate_walls(level)

                food = generate_food(snake, walls)
            else:
                snake.pop()

    screen.fill(BLACK)
    draw_grid()
    draw_walls(walls)
    draw_food(food)
    draw_snake()
    draw_info()

    if game_over:
        show_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()