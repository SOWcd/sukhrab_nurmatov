import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 42)

# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
BLUE = (0, 100, 255)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)

# начальные данные змейки
snake = [(100, 100), (80, 100), (60, 100)]
dx = CELL
dy = 0

score = 0
game_over = False

food_pos = (200, 200)
food_weight = 1
food_timer = 0
food_lifetime = 300  # примерно 5 секунд при 60 fps


def new_food():
    global food_pos, food_weight, food_timer

    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake:
            food_pos = (x, y)
            break

    # еда бывает разного веса
    food_weight = random.choice([1, 2, 3])

    # таймер снова ставим с начала
    food_timer = food_lifetime


def draw_grid():
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))


def draw_snake():
    i = 0
    for part in snake:
        rect = pygame.Rect(part[0], part[1], CELL, CELL)

        if i == 0:
            pygame.draw.rect(screen, BLUE, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)

        i += 1


def draw_food():
    # разный цвет еды в зависимости от веса
    if food_weight == 1:
        color = RED
    elif food_weight == 2:
        color = ORANGE
    else:
        color = YELLOW

    rect = pygame.Rect(food_pos[0], food_pos[1], CELL, CELL)
    pygame.draw.rect(screen, color, rect)


def draw_text():
    score_text = font.render("Score: " + str(score), True, WHITE)
    weight_text = font.render("Food weight: " + str(food_weight), True, WHITE)
    timer_text = font.render("Timer: " + str(food_timer // 60), True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(weight_text, (10, 40))
    screen.blit(timer_text, (10, 70))


def draw_game_over():
    text1 = big_font.render("GAME OVER", True, WHITE)
    text2 = font.render("Press R to restart", True, WHITE)

    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 20))


def restart_game():
    global snake, dx, dy, score, game_over
    snake = [(100, 100), (80, 100), (60, 100)]
    dx = CELL
    dy = 0
    score = 0
    game_over = False
    new_food()


new_food()

running = True
while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
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
                    restart_game()

    if not game_over:
        head_x = snake[0][0]
        head_y = snake[0][1]

        new_head = (head_x + dx, head_y + dy)

        # проверка на выход за границу
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            game_over = True

        # проверка на столкновение с собой
        elif new_head in snake:
            game_over = True

        else:
            snake.insert(0, new_head)

            # если змейка съела еду
            if new_head == food_pos:
                score += food_weight

                # добавляем длину в зависимости от веса еды
                for i in range(food_weight - 1):
                    snake.append(snake[-1])

                new_food()
            else:
                snake.pop()

        # еда исчезает через некоторое время
        food_timer -= 1
        if food_timer <= 0:
            new_food()

    screen.fill(BLACK)
    draw_grid()
    draw_snake()
    draw_food()
    draw_text()

    if game_over:
        draw_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()