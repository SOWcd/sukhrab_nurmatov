import pygame
import math
import sys

pygame.init()

WIDTH = 1000
HEIGHT = 700
TOOLBAR_HEIGHT = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Practice 11 - Paint")

font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 16)

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 215, 0)
GRAY = (210, 210, 210)
DARK_GRAY = (90, 90, 90)

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

current_color = BLACK
tool = "square"
drawing = False
start_pos = None

# кнопки цветов
color_buttons = [
    (BLACK, pygame.Rect(20, 20, 30, 30)),
    (RED, pygame.Rect(60, 20, 30, 30)),
    (GREEN, pygame.Rect(100, 20, 30, 30)),
    (BLUE, pygame.Rect(140, 20, 30, 30)),
    (YELLOW, pygame.Rect(180, 20, 30, 30)),
]

# кнопки инструментов
tool_buttons = {
    "square": pygame.Rect(260, 20, 100, 30),
    "right_triangle": pygame.Rect(370, 20, 130, 30),
    "eq_triangle": pygame.Rect(510, 20, 130, 30),
    "rhombus": pygame.Rect(650, 20, 100, 30),
    "clear": pygame.Rect(760, 20, 100, 30)
}


def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

    # рисуем кнопки цветов
    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

    # рисуем кнопки инструментов
    for name, rect in tool_buttons.items():
        if tool == name:
            fill = DARK_GRAY
            text_color = WHITE
        else:
            fill = WHITE
            text_color = BLACK

        pygame.draw.rect(screen, fill, rect, border_radius=8)
        pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)

        if name == "square":
            text = "Square"
        elif name == "right_triangle":
            text = "Right triangle"
        elif name == "eq_triangle":
            text = "Eq triangle"
        elif name == "rhombus":
            text = "Rhombus"
        else:
            text = "Clear"

        label = small_font.render(text, True, text_color)
        screen.blit(label, (rect.x + 8, rect.y + 8))

    info = font.render("Фигуры: square, right triangle, equilateral triangle, rhombus", True, BLACK)
    screen.blit(info, (20, 65))


def handle_toolbar_click(pos):
    global current_color, tool

    for color, rect in color_buttons:
        if rect.collidepoint(pos):
            current_color = color
            return

    for name, rect in tool_buttons.items():
        if rect.collidepoint(pos):
            if name == "clear":
                canvas.fill(WHITE)
            else:
                tool = name
            return


def draw_square(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end

    side = min(abs(x2 - x1), abs(y2 - y1))

    if x2 >= x1:
        x = x1
    else:
        x = x1 - side

    if y2 >= y1:
        y = y1
    else:
        y = y1 - side

    pygame.draw.rect(surface, color, (x, y, side, side), 2)


def draw_right_triangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end

    # прямоугольный треугольник
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, 2)


def draw_equilateral_triangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end

    # строим примерно равносторонний треугольник
    side = abs(x2 - x1)
    if side < 1:
        side = 1

    height = int((math.sqrt(3) / 2) * side)

    if y2 < y1:
        height = -height

    points = [
        (x1, y1),
        (x1 + side, y1),
        (x1 + side // 2, y1 - height)
    ]

    pygame.draw.polygon(surface, color, points, 2)


def draw_rhombus(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    points = [
        (center_x, y1),
        (x2, center_y),
        (center_x, y2),
        (x1, center_y)
    ]

    pygame.draw.polygon(surface, color, points, 2)


def draw_preview(mouse_pos):
    if not drawing or start_pos is None:
        return

    if mouse_pos[1] < TOOLBAR_HEIGHT:
        return

    preview = canvas.copy()
    end_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

    if tool == "square":
        draw_square(preview, current_color, start_pos, end_pos)
    elif tool == "right_triangle":
        draw_right_triangle(preview, current_color, start_pos, end_pos)
    elif tool == "eq_triangle":
        draw_equilateral_triangle(preview, current_color, start_pos, end_pos)
    elif tool == "rhombus":
        draw_rhombus(preview, current_color, start_pos, end_pos)

    screen.blit(preview, (0, TOOLBAR_HEIGHT))


running = True
while running:
    screen.fill(WHITE)
    draw_toolbar()

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[1] <= TOOLBAR_HEIGHT:
                    handle_toolbar_click(event.pos)
                else:
                    drawing = True
                    start_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                drawing = False

                if event.pos[1] > TOOLBAR_HEIGHT:
                    end_pos = (event.pos[0], event.pos[1] - TOOLBAR_HEIGHT)

                    if tool == "square":
                        draw_square(canvas, current_color, start_pos, end_pos)
                    elif tool == "right_triangle":
                        draw_right_triangle(canvas, current_color, start_pos, end_pos)
                    elif tool == "eq_triangle":
                        draw_equilateral_triangle(canvas, current_color, start_pos, end_pos)
                    elif tool == "rhombus":
                        draw_rhombus(canvas, current_color, start_pos, end_pos)

    if drawing:
        draw_preview(mouse_pos)
    else:
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    pygame.display.flip()

pygame.quit()
sys.exit()