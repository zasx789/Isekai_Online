# ===============================================================
# Isekai Online - Shared Biome Module
# ===============================================================
# Provides biome generation functionality without requiring client
# to import from server code.

import math
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg

# Config constant
TILE_SIZE = cfg.TILE_SIZE


def get_biome(x: float, y: float) -> str:
    """Return a biome type based on sine-wave height pattern."""
    sx, sy = x * 0.005, y * 0.005
    h = math.sin(sx) + math.cos(sy) + 0.5 * math.sin(sx * 3)
    if h < -0.5:
        return "water"
    elif h < -0.2:
        return "sand"
    return "grass"


def is_safe_spawn(x: float, y: float) -> bool:
    """Is the tile valid for spawning mobs / players?"""
    if get_biome(x, y) == "water":
        return False
    col, row = int(x // TILE_SIZE), int(y // TILE_SIZE)
    seed = (col * 73856093) ^ (row * 19349663)
    # 15% chance to have trees (block spawn there)
    if (seed % 100) < 15 and get_biome(col * TILE_SIZE, row * TILE_SIZE) == "grass":
        return False
    return True