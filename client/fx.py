# ===============================================================
# Isekai Online - Visual FX Engine
# ===============================================================
import pygame, random

class FxEngine:
    """Handles temporary on-screen effects."""

    def __init__(self, screen):
        self.screen = screen
        self.effects = []

    def add_hit(self, x, y):
        self.effects.append(["hit", x, y, 8])

    def add_heal(self, x, y):
        self.effects.append(["heal", x, y, 12])

    def update(self):
        for fx in list(self.effects):
            fx[3] -= 1
            if fx[3] <= 0:
                self.effects.remove(fx)
            else:
                if fx[0] == "hit":
                    pygame.draw.circle(self.screen, (255,50,50), (int(fx[1]), int(fx[2])), fx[3]*2, 2)
                elif fx[0] == "heal":
                    pygame.draw.circle(self.screen, (50,255,50), (int(fx[1]), int(fx[2])), fx[3]*2, 2)