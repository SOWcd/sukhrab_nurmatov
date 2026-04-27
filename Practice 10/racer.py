import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
YELLOW = (255, 215, 0)
BLUE = (0, 100, 255)

# Game settings
FPS = 60
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
big_font = pygame.font.SysFont("Arial", 42)

# Road settings
ROAD_LEFT = 50
ROAD_RIGHT = 350
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LINE_WIDTH = 6

# Game variables
scroll_speed = 6
coins_collected = 0
score = 0


class Player(pygame.sprite.Sprite):
    """Player car controlled by the user."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLUE, (0, 10, 40, 50), border_radius=8)
        pygame.draw.rect(self.image, BLACK, (6, 0, 28, 18), border_radius=6)
        pygame.draw.circle(self.image, BLACK, (8, 15), 6)
        pygame.draw.circle(self.image, BLACK, (32, 15), 6)
        pygame.draw.circle(self.image, BLACK, (8, 60), 6)
        pygame.draw.circle(self.image, BLACK, (32, 60), 6)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 90))
        self.speed = 6

    def update(self):
        """Move player left/right inside the road."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep the player inside the road boundaries
        if self.rect.left < ROAD_LEFT + 5:
            self.rect.left = ROAD_LEFT + 5
        if self.rect.right > ROAD_RIGHT - 5:
            self.rect.right = ROAD_RIGHT - 5


class Enemy(pygame.sprite.Sprite):
    """Enemy car moving downward."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 70), pygame.SRCALPHA)
        pygame.draw.rect(self.image, RED, (0, 10, 40, 50), border_radius=8)
        pygame.draw.rect(self.image, BLACK, (6, 0, 28, 18), border_radius=6)
        pygame.draw.circle(self.image, BLACK, (8, 15), 6)
        pygame.draw.circle(self.image, BLACK, (32, 15), 6)
        pygame.draw.circle(self.image, BLACK, (8, 60), 6)
        pygame.draw.circle(self.image, BLACK, (32, 60), 6)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        """Place enemy at a random position above the screen."""
        lane_x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 50)
        self.rect.x = lane_x
        self.rect.y = random.randint(-300, -80)
        self.speed = random.randint(5, 9)

    def update(self):
        """Move enemy down. Reset when it leaves the screen."""
        global score
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            score += 1
            self.reset()


class Coin(pygame.sprite.Sprite):
    """Coin that appears randomly on the road."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((26, 26), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (13, 13), 13)
        pygame.draw.circle(self.image, BLACK, (13, 13), 13, 2)
        pygame.draw.circle(self.image, WHITE, (13, 13), 6, 2)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        """Place coin at a random road position above the screen."""
        self.rect.x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 36)
        self.rect.y = random.randint(-500, -50)
        self.speed = random.randint(4, 7)

    def update(self):
        """Move coin down and respawn when it leaves the screen."""
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.reset()


def draw_road(offset):
    """Draw road background and moving lane lines."""
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

    # Road borders
    pygame.draw.line(screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
    pygame.draw.line(screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

    # Dashed center lines
    for y in range(-40, HEIGHT, 80):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - LINE_WIDTH // 2, y + offset, LINE_WIDTH, 40))


def show_text():
    """Display score and collected coins."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    coins_text = font.render(f"Coins: {coins_collected}", True, WHITE)

    screen.blit(score_text, (15, 15))
    screen.blit(coins_text, (WIDTH - 130, 15))


def game_over_screen():
    """Display game over text."""
    over = big_font.render("GAME OVER", True, WHITE)
    info = font.render("Press R to restart or Q to quit", True, WHITE)
    screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(info, (WIDTH // 2 - info.get_width() // 2, HEIGHT // 2 + 10))


def reset_game():
    """Reset game state."""
    global coins_collected, score, road_offset
    coins_collected = 0
    score = 0
    road_offset = 0
    player.rect.center = (WIDTH // 2, HEIGHT - 90)

    for enemy in enemies:
        enemy.reset()

    for coin in coins:
        coin.reset()


player = Player()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(player)

# Create enemy cars
for _ in range(3):
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)

# Create coins
for _ in range(2):
    coin = Coin()
    coins.add(coin)
    all_sprites.add(coin)

road_offset = 0
running = True
game_over = False

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
                game_over = False
            elif event.key == pygame.K_q:
                running = False

    if not game_over:
        # Update moving road line offset
        road_offset += scroll_speed
        if road_offset >= 80:
            road_offset = 0

        # Update all objects
        player.update()
        enemies.update()
        coins.update()

        # Check collision between player and enemy
        if pygame.sprite.spritecollide(player, enemies, False):
            game_over = True

        # Check collision between player and coins
        hit_coins = pygame.sprite.spritecollide(player, coins, False)
        for coin in hit_coins:
            coins_collected += 1
            coin.reset()

    draw_road(road_offset)
    all_sprites.draw(screen)
    show_text()

    if game_over:
        game_over_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()