# ===============================================================
# Isekai Online - Rendering & World Engine
# ===============================================================
# Handles drawing the terrain, mobs, players, and camera tracking.

import math
import pygame
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg
from shared.biome import get_biome

# Config constants
SCREEN_W = cfg.SCREEN_W
SCREEN_H = cfg.SCREEN_H
TILE_SIZE = cfg.TILE_SIZE


class RenderEngine:
    """Draws the game world onto the Pygame surface."""

    def __init__(self, screen, imgs, font):
        self.screen = screen
        self.imgs = imgs
        self.font = font
        self.cam_x = 0
        self.cam_y = 0

    # -----------------------------------------------------------
    # Helper Methods
    # -----------------------------------------------------------
    def is_blocked(self, x, y):
        """Check if a tile should block movement (water, trees)."""
        if get_biome(x, y) == "water":
            return True

        c, r = int(x // TILE_SIZE), int(y // TILE_SIZE)
        seed = (c * 73856093) ^ (r * 19349663)
        if (seed % 100) < 15 and get_biome(c * 64, r * 64) == "grass":
            return True
        return False

    # -----------------------------------------------------------
    # Drawing Functions
    # -----------------------------------------------------------
    def draw_world(self, me, players, mobs, npcs=None):
        """Main world drawing order."""
        self.screen.fill((0, 0, 0))
        if npcs is None:
            npcs = {}

        # --- Camera Tracking ---
        if me:
            self.cam_x += (me["x"] - SCREEN_W // 2 - self.cam_x) * 0.1
            self.cam_y += (me["y"] - SCREEN_H // 2 - self.cam_y) * 0.1
        cam_x, cam_y = self.cam_x, self.cam_y

        # --- Ground Tiles ---
        sc = int(cam_x // TILE_SIZE)
        sr = int(cam_y // TILE_SIZE)
        for c in range(sc, sc + SCREEN_W // TILE_SIZE + 2):
            for r in range(sr, sr + SCREEN_H // TILE_SIZE + 2):
                wx, wy = c * TILE_SIZE, r * TILE_SIZE
                self.screen.blit(self.imgs[get_biome(wx, wy)], (wx - cam_x, wy - cam_y))

        # --- Trees ---
        for c in range(sc, sc + SCREEN_W // TILE_SIZE + 2):
            for r in range(sr, sr + SCREEN_H // TILE_SIZE + 2):
                seed = (c * 73856093) ^ (r * 19349663)
                if (seed % 100) < 15:
                    wx, wy = c * TILE_SIZE, r * TILE_SIZE
                    if get_biome(wx, wy) == "grass":
                        self.screen.blit(self.imgs["tree"], (wx - cam_x - 30, wy - cam_y - 60))

        # --- NPCs (Guild Master placeholder) ---
        for nid, npc in npcs.items():
            sx, sy = npc["x"] - cam_x, npc["y"] - cam_y
            # Use warrior sprite as stand-in for NPC
            self.screen.blit(self.imgs.get("warrior"), (sx - 32, sy - 32))
            # Draw name above
            name_surf = self.font.render(npc["name"], True, (180, 150, 80))
            self.screen.blit(name_surf, (sx - name_surf.get_width()//2, sy - 50))

        # --- Mobs ---
        for mid, mob in mobs.items():
            sx, sy = mob["x"] - cam_x, mob["y"] - cam_y
            self.screen.blit(self.imgs["slime"], (sx - 32, sy - 32))
            self.draw_bar(sx, sy - 40, 40, mob["hp"], mob["max_hp"], (255, 0, 0), (0, 255, 0))

        # --- Players ---
        for pid, p in sorted(players.items(), key=lambda i: i[1]["y"]):
            sx, sy = p["x"] - cam_x, p["y"] - cam_y
            p_cls = p.get("class", "warrior")
            self.screen.blit(self.imgs[p_cls], (sx - 32, sy - 32))
            tag = f"Lv.{p['lvl']} {p_cls.title()}"
            col = (0, 255, 0) if pid == me else (255, 100, 100)
            label = self.font.render(tag, True, col)
            self.screen.blit(label, (sx - label.get_width() / 2, sy - 50))

    def draw_bar(self, x, y, width, hp, max_hp, bg_col, fg_col):
        pygame.draw.rect(self.screen, bg_col, (x - width // 2, y, width, 5))
        ratio = hp / max_hp if max_hp > 0 else 0
        pygame.draw.rect(self.screen, fg_col, (x - width // 2, y, width * ratio, 5))