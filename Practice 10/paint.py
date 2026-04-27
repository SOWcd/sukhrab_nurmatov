import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (90, 90, 90)
PURPLE = (160, 60, 255)

# Fonts
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 16)

# Canvas settings
TOOLBAR_HEIGHT = 90
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Drawing state
current_color = BLACK
brush_size = 5
tool = "brush"
drawing = False
start_pos = None
last_pos = None

# Color buttons
color_buttons = [
    (BLACK, pygame.Rect(20, 20, 30, 30)),
    (RED, pygame.Rect(60, 20, 30, 30)),
    (GREEN, pygame.Rect(100, 20, 30, 30)),
    (BLUE, pygame.Rect(140, 20, 30, 30)),
    (YELLOW, pygame.Rect(180, 20, 30, 30)),
    (PURPLE, pygame.Rect(220, 20, 30, 30)),
]

# Tool buttons
tool_buttons = {
    "brush": pygame.Rect(320, 20, 100, 30),
    "rectangle": pygame.Rect(430, 20, 100, 30),
    "circle": pygame.Rect(540, 20, 100, 30),
    "eraser": pygame.Rect(650, 20, 100, 30),
    "clear": pygame.Rect(760, 20, 100, 30),
}


def draw_toolbar():
    """Draw the top toolbar with color and tool buttons."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    title = font.render("Paint", True, BLACK)
    screen.blit(title, (20, 60))

    # Draw color buttons
    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # Draw tool buttons
    for name, rect in tool_buttons.items():
        fill = DARK_GRAY if tool == name else WHITE
        pygame.draw.rect(screen, fill, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
        label = small_font.render(name.capitalize(), True, BLACK if fill == WHITE else WHITE)
        screen.blit(label, (rect.x + 10, rect.y + 7))

    # Draw current tool and instructions
    info = font.render(
        "Keys: 1-Brush 2-Rectangle 3-Circle 4-Eraser | +/- size",
        True,
        BLACK
    )
    screen.blit(info, (320, 60))

    state = font.render(f"Tool: {tool}   Size: {brush_size}", True, BLACK)
    screen.blit(state, (700, 60))


def draw_preview(mouse_pos):
    """Draw preview for rectangle or circle while dragging."""
    if not drawing or start_pos is None:
        return

    if mouse_pos[1] < TOOLBAR_HEIGHT:
        return

    preview_surface = canvas.copy()
    adjusted_mouse = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

    if tool == "rectangle":
        x = min(start_pos[0], adjusted_mouse[0])
        y = min(start_pos[1], adjusted_mouse[1])
        width = abs(start_pos[0] - adjusted_mouse[0])
        height = abs(start_pos[1] - adjusted_mouse[1])
        pygame.draw.rect(preview_surface, current_color, (x, y, width, height), 2)

    elif tool == "circle":
        radius = int(math.hypot(adjusted_mouse[0] - start_pos[0], adjusted_mouse[1] - start_pos[1]))
        pygame.draw.circle(preview_surface, current_color, start_pos, radius, 2)

    screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))


def handle_toolbar_click(pos):
    """Handle button clicks in the toolbar."""
    global current_color, tool

    # Check color buttons
    for color, rect in color_buttons:
        if rect.collidepoint(pos):
            current_color = color
            return

    # Check tool buttons
    for name, rect in tool_buttons.items():
        if rect.collidepoint(pos):
            if name == "clear":
                canvas.fill(WHITE)
            else:
                tool = name
            return


running = True
while running:
    screen.fill(WHITE)
    draw_toolbar()

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                tool = "brush"
            elif event.key == pygame.K_2:
                tool = "rectangle"
            elif event.key == pygame.K_3:
                tool = "circle"
            elif event.key == pygame.K_4:
                tool = "eraser"
            elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                brush_size += 1
            elif event.key == pygame.K_MINUS and brush_size > 1:
                brush_size -= 1

            # Quick color keys
            elif event.key == pygame.K_r:
                current_color = RED
            elif event.key == pygame.K_g:
                current_color = GREEN
            elif event.key == pygame.K_b:
                current_color = BLUE
            elif event.key == pygame.K_k:
                current_color = BLACK
            elif event.key == pygame.K_y:
                current_color = YELLOW

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] <= TOOLBAR_HEIGHT:
                    handle_toolbar_click(event.pos)
                else:
                    drawing = True
                    start_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)
                    last_pos = start_pos

                    # Draw immediately for brush/eraser
                    if tool == "brush":
                        pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, WHITE, start_pos, brush_size * 2)

        elif event.type == pygame.MOUSEMOTION:
            if drawing and event.pos[1] > TOOLBAR_HEIGHT:
                current_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

                # Free drawing with brush
                if tool == "brush":
                    pygame.draw.line(canvas, current_color, last_pos, current_pos, brush_size * 2)
                    pygame.draw.circle(canvas, current_color, current_pos, brush_size)

                # Eraser works like a white brush
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, current_pos, brush_size * 4)
                    pygame.draw.circle(canvas, WHITE, current_pos, brush_size * 2)

                last_pos = current_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False

                if event.pos[1] > TOOLBAR_HEIGHT:
                    end_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

                    if tool == "rectangle":
                        x = min(start_pos[0], end_pos[0])
                        y = min(start_pos[1], end_pos[1])
                        width = abs(start_pos[0] - end_pos[0])
                        height = abs(start_pos[1] - end_pos[1])
                        pygame.draw.rect(canvas, current_color, (x, y, width, height), 2)

                    elif tool == "circle":
                        radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                        pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

    # Draw the canvas
    if tool in ("rectangle", "circle") and drawing:
        draw_preview(mouse_pos)
    else:
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    pygame.display.flip()

pygame.quit()
sys.exit()