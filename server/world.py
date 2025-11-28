# ===============================================================
# Isekai Online - World & Biome Logic (with City / Castle helpers)
# ===============================================================
# - City (castle) safe‑zone helpers for player spawn and mob exclusion
# - Utility for minimap and visuals
# - biome functions are imported from shared module

import random
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg
from shared.biome import get_biome, is_safe_spawn

# Config constants
TILE_SIZE = cfg.TILE_SIZE
CITY = cfg.CITY
CITY_SPAWN = cfg.CITY_SPAWN

# ===============================================================
# NOTE: Biome functions are now imported from shared/biome.py
# ===============================================================


def random_spawn_area(xmin=200, xmax=2800, ymin=200, ymax=2800):
    """Generate a random valid world coordinate (used for mobs)."""
    for _ in range(80):
        x, y = random.randint(xmin, xmax), random.randint(ymin, ymax)
        if is_safe_spawn(x, y):
            return x, y
    # fallback if nothing valid after tries
    return random.randint(xmin, xmax), random.randint(ymin, ymax)


# -----------------------------------------------------------
# City / Castle helpers
# -----------------------------------------------------------
def in_city(x: float, y: float) -> bool:
    """True if (x,y) is inside the castle city safe‑zone."""
    return (CITY["x"] <= x <= CITY["x"] + CITY["w"]) and (
        CITY["y"] <= y <= CITY["y"] + CITY["h"]
    )


def city_spawn_point():
    """Center coordinate of city for player spawn / respawn."""
    return CITY_SPAWN


def get_city_rect():
    """Return (x,y,w,h) for client rendering or minimap overlay."""
    return CITY["x"], CITY["y"], CITY["w"], CITY["h"]


# -----------------------------------------------------------
# Quick self‑test
# -----------------------------------------------------------
if __name__ == "__main__":
    print("Biome test:")
    for i in range(5):
        x, y = random_spawn_area()
        print(f"({x},{y}) -> {get_biome(x,y)}, in_city={in_city(x,y)}")

    cx, cy, cw, ch = get_city_rect()
    print(f"City rect = ({cx}, {cy}, {cw}, {ch})")
    print(f"City spawn = {city_spawn_point()}")