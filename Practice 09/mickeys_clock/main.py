import pygame
from clock import MickeyClock


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Mickey's Clock")

    clock = pygame.time.Clock()
    app = MickeyClock(screen, WINDOW_WIDTH, WINDOW_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        app.update()
        app.draw()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()