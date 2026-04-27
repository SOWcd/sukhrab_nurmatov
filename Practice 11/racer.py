import pygame
import random
import sys

pygame.init()

# размеры окна
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Racer")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 40)

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)

# дорога
ROAD_LEFT = 50
ROAD_RIGHT = 350

# переменные игры
coins = 0
road_y = 0
enemy_speed = 5
speed_changed = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)

        # рисуем простую машинку
        pygame.draw.rect(self.image, BLUE, (0, 10, 40, 50), border_radius=8)
        pygame.draw.rect(self.image, BLACK, (5, 0, 30, 20), border_radius=5)
        pygame.draw.circle(self.image, BLACK, (8, 15), 5)
        pygame.draw.circle(self.image, BLACK, (32, 15), 5)
        pygame.draw.circle(self.image, BLACK, (8, 60), 5)
        pygame.draw.circle(self.image, BLACK, (32, 60), 5)

        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 80)
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # чтобы машина не уезжала за пределы дороги
        if self.rect.left < ROAD_LEFT + 5:
            self.rect.left = ROAD_LEFT + 5
        if self.rect.right > ROAD_RIGHT - 5:
            self.rect.right = ROAD_RIGHT - 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)

        # рисуем вражескую машинку
        pygame.draw.rect(self.image, RED, (0, 10, 40, 50), border_radius=8)
        pygame.draw.rect(self.image, BLACK, (5, 0, 30, 20), border_radius=5)
        pygame.draw.circle(self.image, BLACK, (8, 15), 5)
        pygame.draw.circle(self.image, BLACK, (32, 15), 5)
        pygame.draw.circle(self.image, BLACK, (8, 60), 5)
        pygame.draw.circle(self.image, BLACK, (32, 60), 5)

        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 50)
        self.rect.y = random.randint(-300, -80)

    def update(self):
        self.rect.y += enemy_speed

        # если машина ушла вниз экрана, переносим наверх
        if self.rect.top > HEIGHT:
            self.reset()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # случайный вес монеты
        self.weight = random.choice([1, 2, 3])

        # размер и цвет зависит от веса
        if self.weight == 1:
            size = 18
            color = YELLOW
        elif self.weight == 2:
            size = 24
            color = ORANGE
        else:
            size = 30
            color = WHITE

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, BLACK, (size // 2, size // 2), size // 2, 2)

        self.rect = self.image.get_rect()
        self.speed = 4
        self.reset()

    def reset(self):
        # при каждом новом появлении снова меняем вес
        self.weight = random.choice([1, 2, 3])

        if self.weight == 1:
            size = 18
            color = YELLOW
        elif self.weight == 2:
            size = 24
            color = ORANGE
        else:
            size = 30
            color = WHITE

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, BLACK, (size // 2, size // 2), size // 2, 2)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 40)
        self.rect.y = random.randint(-500, -50)

    def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.reset()


def draw_road():
    global road_y

    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

    # боковые линии дороги
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

    # пунктир по центру
    for y in range(-40, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 3, y + road_y, 6, 40))

    road_y += 6
    if road_y >= 80:
        road_y = 0


def show_text():
    coins_text = font.render("Coins: " + str(coins), True, WHITE)
    speed_text = font.render("Enemy speed: " + str(enemy_speed), True, WHITE)

    screen.blit(coins_text, (20, 20))
    screen.blit(speed_text, (20, 50))


def game_over_text():
    text1 = big_font.render("GAME OVER", True, WHITE)
    text2 = font.render("Press R to restart", True, WHITE)

    screen.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 + 20))


def restart_game():
    global coins, enemy_speed, speed_changed, game_over
    coins = 0
    enemy_speed = 5
    speed_changed = False
    game_over = False

    player.rect.center = (WIDTH // 2, HEIGHT - 80)
    enemy.reset()

    for c in coin_group:
        c.reset()


player = Player()
enemy = Enemy()

all_sprites = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

all_sprites.add(player)
all_sprites.add(enemy)
enemy_group.add(enemy)

# создаём несколько монет
for i in range(3):
    c = Coin()
    all_sprites.add(c)
    coin_group.add(c)

game_over = False
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()

    if not game_over:
        player.update()
        enemy.update()
        coin_group.update()

        # если игрок столкнулся с врагом, игра закончится
        if pygame.sprite.spritecollide(player, enemy_group, False):
            game_over = True

        # собираем монеты
        hits = pygame.sprite.spritecollide(player, coin_group, False)
        for coin in hits:
            coins += coin.weight
            coin.reset()

        # увеличиваем скорость врага, если игрок собрал N монет
        # пусть N = 10
        if coins >= 10 and speed_changed == False:
            enemy_speed += 3
            speed_changed = True

    draw_road()
    all_sprites.draw(screen)
    show_text()

    if game_over:
        game_over_text()

    pygame.display.flip()

pygame.quit()
sys.exit()