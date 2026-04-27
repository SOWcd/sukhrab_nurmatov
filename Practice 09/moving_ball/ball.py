class Ball:
    def __init__(self, x, y, r, step, bounds):
        self.x = x
        self.y = y
        self.r = r
        self.step = step
        self.w, self.h = bounds

    def move(self, dx, dy):
        new_x = self.x + dx * self.step
        new_y = self.y + dy * self.step
        if self.r <= new_x <= self.w - self.r:
            self.x = new_x
        if self.r <= new_y <= self.h - self.r:
            self.y = new_y