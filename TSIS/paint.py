import pygame
import datetime

# Цветовые константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (230, 230, 230)
DARK_GRAY = (50, 50, 50)

# Размеры экрана и палитры
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 680
CANVAS_HEIGHT = 580
PALETTE_HEIGHT = SCREEN_HEIGHT - CANVAS_HEIGHT
PALETTE_Y = CANVAS_HEIGHT

# Цвета для палитры и кликабельные области
PALETTE_COLORS = [
    ('Black', BLACK),
    ('Red', RED),
    ('Green', GREEN),
    ('Blue', BLUE)
]

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sukhrab's Paint - TSIS 2")

    clock = pygame.time.Clock()
    canvas = pygame.Surface((SCREEN_WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)

    # Поддержание состояния рисования
    done = False
    drawing = False
    start_pos = None
    prev_pos = None

    current_tool = 'pencil'  # pencil, line, rect, circle, eraser, text
    current_color = BLACK
    thickness = 2  # Клавиши: 1, 2, 3

    font = pygame.font.SysFont("Arial", 20)

    # Подготовка кнопок палитры
    palette_buttons = []
    button_width = 120
    button_padding = 10
    x = button_padding
    button_height = 40
    for name, color in PALETTE_COLORS:
        rect = pygame.Rect(x, PALETTE_Y + 5, button_width, button_height)
        palette_buttons.append((rect, name, color))
        x += button_width + button_padding

    clear_button_rect = pygame.Rect(x, PALETTE_Y + 5, button_width, button_height)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                # Толщина кисти
                if event.key == pygame.K_1:
                    thickness = 2
                if event.key == pygame.K_2:
                    thickness = 5
                if event.key == pygame.K_3:
                    thickness = 10

                # Выбор инструментов
                if event.key == pygame.K_p:
                    current_tool = 'pencil'
                if event.key == pygame.K_l:
                    current_tool = 'line'
                if event.key == pygame.K_r:
                    # Shift+R changes color to red, plain R selects rectangle tool
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        current_color = RED
                    else:
                        current_tool = 'rect'
                if event.key == pygame.K_c:
                    current_tool = 'circle'
                if event.key == pygame.K_e:
                    current_tool = 'eraser'
                if event.key == pygame.K_t:
                    current_tool = 'text'

                # Горячие клавиши цвета
                if event.key == pygame.K_g:
                    current_color = GREEN
                if event.key == pygame.K_b:
                    current_color = BLUE
                if event.key == pygame.K_k:
                    current_color = BLACK

                # Очистить холст
                if event.key == pygame.K_x:
                    canvas.fill(WHITE)

                # Сохранение Ctrl+S
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
                    filename = f"screenshot_{timestamp}.png"
                    pygame.image.save(canvas, filename)
                    print(f"Saved as {filename}")

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Если клик по палитре, переключить цвет или очистить
                if event.pos[1] >= PALETTE_Y:
                    for rect, name, color in palette_buttons:
                        if rect.collidepoint(event.pos):
                            current_color = color
                            break
                    if clear_button_rect.collidepoint(event.pos):
                        canvas.fill(WHITE)
                    continue

                drawing = True
                start_pos = event.pos
                prev_pos = event.pos
                if current_tool == 'text':
                    text_surface = font.render("Sukhrab Nurmatov", True, current_color)
                    canvas.blit(text_surface, event.pos)

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and event.pos[1] < PALETTE_Y:
                    if current_tool == 'line':
                        pygame.draw.line(canvas, current_color, start_pos, event.pos, thickness)
                    elif current_tool == 'rect':
                        width = event.pos[0] - start_pos[0]
                        height = event.pos[1] - start_pos[1]
                        pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], width, height), thickness)
                    elif current_tool == 'circle':
                        radius = int(((event.pos[0] - start_pos[0])**2 + (event.pos[1] - start_pos[1])**2)**0.5)
                        pygame.draw.circle(canvas, current_color, start_pos, radius, thickness)
                drawing = False
                prev_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing and current_tool in ['pencil', 'eraser'] and event.pos[1] < PALETTE_Y:
                    color = WHITE if current_tool == 'eraser' else current_color
                    if prev_pos:
                        # Сглаженный штрих между предыдущей и текущей позицией мыши
                        pygame.draw.line(canvas, color, prev_pos, event.pos, thickness)
                    prev_pos = event.pos

        # Отрисовка холста
        screen.fill(GRAY)
        screen.blit(canvas, (0, 0))

        # Рисование палитры цвета и кнопки очистки
        pygame.draw.rect(screen, DARK_GRAY, (0, PALETTE_Y, SCREEN_WIDTH, PALETTE_HEIGHT))
        for rect, name, color in palette_buttons:
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            label = font.render(name, True, WHITE if color != WHITE else BLACK)
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

        pygame.draw.rect(screen, WHITE, clear_button_rect)
        pygame.draw.rect(screen, BLACK, clear_button_rect, 2)
        clear_label = font.render("Clear (X)", True, BLACK)
        clear_label_rect = clear_label.get_rect(center=clear_button_rect.center)
        screen.blit(clear_label, clear_label_rect)

        # Подсказка статуса активного цвета и инструмента
        current_color_name = next((name for name, color in PALETTE_COLORS if color == current_color), 'Custom')
        status_text = f"Tool: {current_tool.capitalize()} | Color: {current_color_name} | Thickness: {thickness}"
        status_surface = font.render(status_text, True, WHITE)
        screen.blit(status_surface, (10, PALETTE_Y + button_height + 10))

        # На экране подсказки управления
        help_text = "Tools: P=pencil, L=line, R=rect, C=circle, E=eraser, T=text | X=Clear | Ctrl+S=Save"
        help_surface = font.render(help_text, True, WHITE)
        screen.blit(help_surface, (10, PALETTE_Y + button_height + 35))

        # Превью при рисовании формы (ghost outline)
        if drawing and current_tool in ['line', 'rect', 'circle']:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < PALETTE_Y:
                if current_tool == 'line':
                    pygame.draw.line(screen, current_color, start_pos, mouse_pos, thickness)
                elif current_tool == 'rect':
                    width = mouse_pos[0] - start_pos[0]
                    height = mouse_pos[1] - start_pos[1]
                    pygame.draw.rect(screen, current_color, (start_pos[0], start_pos[1], width, height), thickness)
                elif current_tool == 'circle':
                    radius = int(((mouse_pos[0] - start_pos[0])**2 + (mouse_pos[1] - start_pos[1])**2)**0.5)
                    pygame.draw.circle(screen, current_color, start_pos, radius, thickness)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
