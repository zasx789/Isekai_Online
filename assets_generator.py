# ===============================================================
# Isekai Online - Asset Generator
# ===============================================================
# Responsible for creating all base pixel assets if they don't exist yet.
# Called once on client startup to ensure all required files are present.

import os
import random
import pygame
import sys
# Add project root to path (should already be in root directory)
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg

# Config constant
TILE_SIZE = cfg.TILE_SIZE


def generate_assets():
    """Generate simple procedural graphics used in the game."""
    if not os.path.exists("assets"):
        print("[System] Creating assets folder...")
        os.makedirs("assets")

    # --- Terrain Tiles ---
    if not os.path.exists("assets/grass.png"):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        s.fill((34, 139, 34))
        for _ in range(120):
            pygame.draw.rect(s, (40, 160, 40), (random.randint(0, 63), random.randint(0, 63), 2, 2))
        pygame.image.save(s, "assets/grass.png")

    if not os.path.exists("assets/water.png"):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        s.fill((0, 105, 148))
        pygame.image.save(s, "assets/water.png")

    if not os.path.exists("assets/sand.png"):
        s = pygame.Surface((TILE_SIZE, TILE_SIZE))
        s.fill((238, 214, 175))
        pygame.image.save(s, "assets/sand.png")

    if not os.path.exists("assets/tree.png"):
        s = pygame.Surface((128, 128), pygame.SRCALPHA)
        pygame.draw.rect(s, (101, 67, 33), (56, 80, 16, 40))
        pygame.draw.circle(s, (34, 139, 34), (64, 60), 35)
        pygame.image.save(s, "assets/tree.png")

    # --- Player Classes ---
    if not os.path.exists("assets/warrior.png"):
        s = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.rect(s, (180, 40, 40), (20, 25, 24, 30))
        pygame.draw.circle(s, (255, 220, 180), (32, 16), 10)
        pygame.draw.rect(s, (160, 160, 160), (20, 26, 24, 20))
        pygame.draw.rect(s, (220, 220, 220), (50, 10, 4, 20))
        pygame.image.save(s, "assets/warrior.png")

    if not os.path.exists("assets/mage.png"):
        s = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.rect(s, (75, 0, 130), (20, 20, 24, 40))
        pygame.draw.circle(s, (255, 220, 180), (32, 16), 10)
        pygame.draw.polygon(s, (75, 0, 130), [(22, 6), (42, 6), (32, -5)])
        pygame.draw.line(s, (139, 69, 19), (50, 20), (50, 60), 3)
        pygame.draw.circle(s, (0, 255, 255), (50, 18), 5)
        pygame.image.save(s, "assets/mage.png")

    if not os.path.exists("assets/rogue.png"):
        s = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.rect(s, (50, 50, 50), (22, 25, 20, 25))
        pygame.draw.circle(s, (255, 220, 180), (32, 16), 10)
        pygame.draw.rect(s, (30, 30, 30), (22, 8, 20, 8))
        pygame.draw.polygon(s, (200, 200, 200), [(50, 30), (55, 40), (45, 40)])
        pygame.image.save(s, "assets/rogue.png")

    # --- Enemy: Slime ---
    if not os.path.exists("assets/slime.png"):
        s = pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (0, 200, 50), (16, 32, 32, 24))
        pygame.draw.circle(s, (0, 0, 0), (24, 40), 2)
        pygame.draw.circle(s, (0, 0, 0), (40, 40), 2)
        pygame.image.save(s, "assets/slime.png")

    print("[System] Asset generation complete.")
