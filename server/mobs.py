# ===============================================================
# Isekai Online - Mob (Enemy) Management (castle-aware)
# ===============================================================

import uuid
import random
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg
from server.world import (
    is_safe_spawn,
    random_spawn_area,
    in_city,
)

# Config constants
INITIAL_MOB_COUNT = cfg.INITIAL_MOB_COUNT
MOB_MIN_LEVEL = cfg.MOB_MIN_LEVEL
MOB_MAX_LEVEL = cfg.MOB_MAX_LEVEL
MOB_BASE_HP = cfg.MOB_BASE_HP
MOB_HP_PER_LEVEL = cfg.MOB_HP_PER_LEVEL


class MobManager:
    """Central mob controller tracking all active enemies."""

    def __init__(self):
        self.mobs: dict[str, dict] = {}

    def spawn_mob(self, mob_type="slime"):
        """Spawn a single mob safely outside the city."""
        mid = str(uuid.uuid4())[:4]
        for _ in range(120):
            mx, my = random_spawn_area()
            # must be safe terrain and NOT inside the castle
            if is_safe_spawn(mx, my) and not in_city(mx, my):
                lvl = random.randint(MOB_MIN_LEVEL, MOB_MAX_LEVEL)
                max_hp = MOB_BASE_HP + lvl * MOB_HP_PER_LEVEL
                self.mobs[mid] = {
                    "type": mob_type,
                    "x": mx,
                    "y": my,
                    "hp": max_hp,
                    "max_hp": max_hp,
                    "lvl": lvl,
                }
                return mid
        return None

    def spawn_initial_mobs(self, count=INITIAL_MOB_COUNT):
        """Spawn multiple mobs at startup."""
        for _ in range(count):
            self.spawn_mob()

    def remove_mob(self, mob_id: str):
        """Delete a mob when defeated."""
        self.mobs.pop(mob_id, None)

    def respawn_mob(self):
        """Respawn one new mob after another dies."""
        self.spawn_mob()

    def get_state(self) -> dict:
        """Return full mob dictionary for sync with clients."""
        return self.mobs


if __name__ == "__main__":
    manager = MobManager()
    manager.spawn_initial_mobs()
    print(f"[TEST] Spawned {len(manager.mobs)} mobs:")
    for mid, mob in manager.mobs.items():
        print(f" - {mid}: Lv{mob['lvl']} {mob['type']} ({mob['x']},{mob['y']})")