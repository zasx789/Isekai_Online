# ===============================================================
# Isekai Online - UI (Heads-Up Display)
# ===============================================================
# Responsible for drawing all on-screen UI elements like
# health bars, XP bars, and text indicators.

import pygame
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg

# Config constants
SCREEN_W = cfg.SCREEN_W
SCREEN_H = cfg.SCREEN_H


class GameUI:
    """Draws the player's HUD (HP, XP, etc.)."""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_hud(self, player_data):
        """Render HP and XP bars at top-left corner."""
        if not player_data:
            return

        hp = player_data.get("hp", 100)
        max_hp = player_data.get("max_hp", 100)
        xp = player_data.get("xp", 0)
        lvl = player_data.get("lvl", 1)
        cls = player_data.get("class", "Unknown").title()

        # HUD box background
        hud_rect = pygame.Rect(10, 10, 220, 65)
        pygame.draw.rect(self.screen, (40, 40, 40), hud_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), hud_rect, 2)

        # HP Bar (red)
        hp_ratio = hp / max_hp if max_hp > 0 else 0
        pygame.draw.rect(self.screen, (100, 0, 0), (20, 25, 180, 15))
        pygame.draw.rect(self.screen, (255, 0, 0), (20, 25, 180 * hp_ratio, 15))

        # XP Bar (gold)
        xp_ratio = xp / 100
        pygame.draw.rect(self.screen, (50, 50, 0), (20, 45, 180, 10))
        pygame.draw.rect(self.screen, (255, 255, 0), (20, 45, 180 * xp_ratio, 10))

        # Text elements
        txt1 = self.font.render(f"HP: {hp}/{max_hp}", True, (255, 255, 255))
        txt2 = self.font.render(f"Lvl {lvl} {cls}", True, (255, 255, 255))
        self.screen.blit(txt1, (25, 25))
        self.screen.blit(txt2, (25, 10))