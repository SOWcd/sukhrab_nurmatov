import os
import sys
import pygame
from player import MusicPlayer


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
FPS = 30


def draw_text(screen, text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def format_time(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    minutes = total_seconds // 60
    secs = total_seconds % 60
    return f"{minutes:02}:{secs:02}"


def load_playlist(folder="music"):
    supported_formats = (".mp3", ".wav")

    if not os.path.exists(folder):
        raise FileNotFoundError(f"Folder '{folder}' not found.")

    files = []
    for file_name in os.listdir(folder):
        if file_name.lower().endswith(supported_formats):
            files.append(os.path.join(folder, file_name))

    files.sort()

    if not files:
        raise Exception("No music files found in 'music/' folder.")

    return files


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("arial", 36, bold=True)
    info_font = pygame.font.SysFont("arial", 26)
    small_font = pygame.font.SysFont("arial", 20)

    playlist = load_playlist("music")
    player = MusicPlayer(playlist)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()

        player.update(dt)

        screen.fill((245, 245, 245))

        draw_text(screen, "Music Player", title_font, (20, 20, 20), 30, 20)
        draw_text(
            screen,
            f"Current track: {player.get_current_track_name()}",
            info_font,
            (40, 40, 40),
            30,
            90,
        )
        draw_text(
            screen,
            f"Status: {player.get_status()}",
            info_font,
            (40, 40, 40),
            30,
            135,
        )

        current_time = format_time(player.get_current_position())
        total_time = format_time(player.get_current_track_length())

        draw_text(
            screen,
            f"Progress: {current_time} / {total_time}",
            info_font,
            (40, 40, 40),
            30,
            180,
        )

        bar_x = 30
        bar_y = 230
        bar_width = 740
        bar_height = 25

        pygame.draw.rect(
            screen,
            (200, 200, 200),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=8,
        )

        progress_ratio = 0
        track_length = player.get_current_track_length()
        if track_length > 0:
            progress_ratio = min(player.get_current_position() / track_length, 1)

        progress_width = int(bar_width * progress_ratio)
        pygame.draw.rect(
            screen,
            (80, 170, 255),
            (bar_x, bar_y, progress_width, bar_height),
            border_radius=8,
        )

        controls = [
            "P = Play",
            "S = Stop",
            "N = Next track",
            "B = Previous track",
            "Q = Quit",
        ]

        y = 290
        for control in controls:
            draw_text(screen, control, small_font, (70, 70, 70), 30, y)
            y += 28

        pygame.display.flip()

    player.cleanup()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()