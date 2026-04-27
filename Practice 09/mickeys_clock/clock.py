import math
import datetime
import pygame


class MickeyClock:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height

        self.center_x = width // 2
        self.center_y = height // 2 + 40

        self.background_color = (255, 255, 255)
        self.clock_color = (240, 220, 130)
        self.outline_color = (0, 0, 0)
        self.hand_color = (0, 0, 0)
        self.text_color = (20, 20, 20)

        self.clock_radius = 180
        self.ear_radius = 65
        self.hand_width = 18
        self.hand_length = 130

        self.font = pygame.font.SysFont("arial", 36, bold=True)

    def get_time(self):
        now = datetime.datetime.now()
        return now.minute, now.second

    def get_hand_endpoint(self, angle_degrees, length):
        # 0 градусов = вверх
        angle_radians = math.radians(angle_degrees - 90)
        x = self.center_x + length * math.cos(angle_radians)
        y = self.center_y + length * math.sin(angle_radians)
        return int(x), int(y)

    def draw_background(self):
        self.screen.fill(self.background_color)

    def draw_mickey_face(self):
        # Голова
        pygame.draw.circle(
            self.screen,
            self.clock_color,
            (self.center_x, self.center_y),
            self.clock_radius
        )
        pygame.draw.circle(
            self.screen,
            self.outline_color,
            (self.center_x, self.center_y),
            self.clock_radius,
            4
        )

        # Уши
        left_ear_center = (self.center_x - 120, self.center_y - 140)
        right_ear_center = (self.center_x + 120, self.center_y - 140)

        pygame.draw.circle(self.screen, self.clock_color, left_ear_center, self.ear_radius)
        pygame.draw.circle(self.screen, self.outline_color, left_ear_center, self.ear_radius, 4)

        pygame.draw.circle(self.screen, self.clock_color, right_ear_center, self.ear_radius)
        pygame.draw.circle(self.screen, self.outline_color, right_ear_center, self.ear_radius, 4)

    def draw_marks(self):
        for i in range(60):
            angle = i * 6
            outer_x, outer_y = self.get_hand_endpoint(angle, self.clock_radius - 10)

            if i % 5 == 0:
                inner_x, inner_y = self.get_hand_endpoint(angle, self.clock_radius - 35)
                width = 4
            else:
                inner_x, inner_y = self.get_hand_endpoint(angle, self.clock_radius - 20)
                width = 2

            pygame.draw.line(
                self.screen,
                self.outline_color,
                (inner_x, inner_y),
                (outer_x, outer_y),
                width
            )

    def draw_hand(self, angle, length, width, color):
        end_x, end_y = self.get_hand_endpoint(angle, length)
        pygame.draw.line(
            self.screen,
            color,
            (self.center_x, self.center_y),
            (end_x, end_y),
            width
        )
        pygame.draw.circle(self.screen, color, (self.center_x, self.center_y), 10)

    def draw_time_text(self, minute, second):
        time_text = f"{minute:02}:{second:02}"
        text_surface = self.font.render(time_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.center_x, self.center_y + 230))
        self.screen.blit(text_surface, text_rect)

    def update(self):
        self.minute, self.second = self.get_time()
        self.minute_angle = self.minute * 6
        self.second_angle = self.second * 6

    def draw(self):
        self.draw_background()
        self.draw_mickey_face()
        self.draw_marks()

        # По заданию:
        # Right hand = minutes hand
        # Left hand = seconds hand
        #
        # В упрощённой реализации:
        # толстая рука = минуты
        # тонкая рука = секунды
        self.draw_hand(self.minute_angle, self.hand_length, 12, (30, 30, 30))
        self.draw_hand(self.second_angle, self.hand_length + 20, 6, (200, 50, 50))

        self.draw_time_text(self.minute, self.second)