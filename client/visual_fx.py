# ===============================================================
# Isekai Online - Client Visual Effects
# ===============================================================
import random
import pygame
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg

SCREEN_W = cfg.SCREEN_W
SCREEN_H = cfg.SCREEN_H


class DamageNumber:
    def __init__(self, x, y, text, color=(255, 255, 255)):
        self.x = x + random.randint(-10, 10)
        self.y = y
        self.text = text
        self.timer = 60
        self.color = color
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.vel_y = -1

    def update(self):
        self.y += self.vel_y
        self.timer -= 1
        if self.timer < 30:
            self.vel_y = 0
        return self.timer > 0

    def draw(self, surface, cam_x, cam_y):
        screen_x = self.x - cam_x
        screen_y = self.y - cam_y
        alpha = min(255, self.timer * 4)
        surf = self.font.render(self.text, True, self.color)
        surface.blit(surf, (screen_x, screen_y))


class VFXManager:
    def __init__(self):
        self.damage_numbers = []
        self.hit_flares = []  # (x, y, timer, color, radius)
        self.shake_timer = 0
        self.shake_intensity = 0

    # Add damage/heal numbers (client receives from server)
    def add_damage(self, x, y, dmg, is_crit=False):
        color = (255, 200, 50) if is_crit else (255, 80, 80)
        self.damage_numbers.append(DamageNumber(x, y - 20, str(dmg), color))

    def add_heal(self, x, y, amount):
        self.damage_numbers.append(DamageNumber(x, y - 20, f"+{amount}", (80, 255, 80)))

    # Combat visual flash from skill use
    def add_skill_flash(self, x, y, skill_name):
        if skill_name == "Fireball":
            self.hit_flares.append([x, y, 20, (255, 100, 0), 45])
        elif skill_name == "PowerStrike":
            self.hit_flares.append([x, y, 15, (255, 255, 100), 25])
        elif skill_name == "ShadowStep":
            self.hit_flares.append([x, y, 25, (180, 180, 255), 30])
        elif skill_name == "WindSlash":
            self.hit_flares.append([x, y, 10, (200, 255, 255), 40])

    # Screen shake on powerful attacks
    def add_shake(self, intensity=4):
        self.shake_timer = 15
        self.shake_intensity = intensity

    def update(self):
        # Update damage numbers
        self.damage_numbers = [d for d in self.damage_numbers if d.update()]
        # Update hit flares
        new_flares = []
        for x, y, t, col, rad in self.hit_flares:
            if t > 0:
                new_flares.append([x, y, t - 1, col, rad + 1])
        self.hit_flares = new_flares
        # Update shake
        if self.shake_timer > 0:
            self.shake_timer -= 1

    def apply_shake(self, surface):
        if self.shake_timer > 0:
            off_x = random.randint(-self.shake_intensity, self.shake_intensity)
            off_y = random.randint(-self.shake_intensity, self.shake_intensity)
            pygame.display.get_surface().blit(surface, (off_x, off_y))
            return True
        return False

    def draw(self, surface, cam_x, cam_y):
        # Draw flares
        for x, y, t, col, rad in self.hit_flares:
            screen_x = int(x - cam_x)
            screen_y = int(y - cam_y)
            alpha = min(200, t * 10)
            pygame.draw.circle(surface, (*col, alpha), (screen_x, screen_y), rad, 2)
        # Draw damage numbers
        for dmg in self.damage_numbers:
            dmg.draw(surface, cam_x, cam_y)