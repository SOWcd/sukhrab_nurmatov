import pygame
from ball import Ball

pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
ball = Ball(W//2, H//2, 25, 20, (W, H))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: ball.move(0, -1)
            elif event.key == pygame.K_DOWN: ball.move(0, 1)
            elif event.key == pygame.K_LEFT: ball.move(-1, 0)
            elif event.key == pygame.K_RIGHT: ball.move(1, 0)

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.r)
    pygame.display.flip()

pygame.quit()