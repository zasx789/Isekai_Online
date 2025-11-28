# ===============================================================
# Isekai Online - Player Management (castle spawn + DB)
# ===============================================================

import uuid
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg
from server.world import city_spawn_point
from server.database import Database

# Config constants
DEFAULT_STATS = cfg.DEFAULT_STATS
XP_PER_LEVEL = cfg.XP_PER_LEVEL

# shared db connection
db = Database()


class Player:
    """Represents a single player entity."""

    def __init__(self, class_name="warrior", player_id=None):
        self.id = player_id or str(uuid.uuid4())[:4]
        self.class_name = class_name
        self.x, self.y = self.spawn()  # spawn in castle
        base = DEFAULT_STATS.get(class_name, DEFAULT_STATS["warrior"]).copy()
        base.setdefault("max_hp", base.get("hp", 100))
        self.stats = base
        self.level = 1
        self.xp = 0

        # attempt to load saved data
        saved = db.load_player(self.id)
        if saved:
            self.class_name = saved.get("class", self.class_name)
            self.level = saved.get("lvl", self.level)
            self.xp = saved.get("xp", self.xp)
            self.stats["hp"] = saved.get("hp", self.stats["hp"])
            self.stats["max_hp"] = saved.get("max_hp", self.stats["max_hp"])

    def spawn(self):
        """Spawn/respawn inside the castle city (safe zone)."""
        return city_spawn_point()

    def respawn(self):
        """Fully heal and return to city after death."""
        self.x, self.y = city_spawn_point()
        self.stats["hp"] = self.stats["max_hp"]

    def add_xp(self, amount: int):
        """Adds XP and performs auto‑level logic."""
        self.xp += amount
        leveled_up = False
        while self.xp >= XP_PER_LEVEL:
            self.xp -= XP_PER_LEVEL
            self.level += 1
            leveled_up = True
            self.stats["max_hp"] = self.stats.get("max_hp", 100) + 20
            self.stats["hp"] = self.stats["max_hp"]
        db.save_player(self.id, self.serialize())
        return leveled_up

    def serialize(self):
        """Export player data."""
        return {
            "x": self.x,
            "y": self.y,
            "class": self.class_name,
            "hp": self.stats.get("hp", 100),
            "max_hp": self.stats.get("max_hp", 100),
            "lvl": self.level,
            "xp": self.xp,
        }


# -----------------------------------------------------------
# Player Manager
# -----------------------------------------------------------
class PlayerManager:
    """Handles all connected players."""

    def __init__(self):
        self.players: dict[str, Player] = {}

    def create_player(self, class_name="warrior", existing_id=None) -> Player:
        player = Player(class_name, existing_id)
        self.players[player.id] = player
        return player

    def remove_player(self, pid: str):
        """Remove player from memory and persist to DB."""
        if pid in self.players:
            db.save_player(pid, self.players[pid].serialize())
            del self.players[pid]

    def get_player(self, pid: str):
        """Fetch a player object."""
        return self.players.get(pid)

    def get_state(self) -> dict:
        """Return serialized dict of all active players."""
        return {pid: p.serialize() for pid, p in self.players.items()}

    def save_all(self):
        """Save all loaded players to DB."""
        for p in self.players.values():
            db.save_player(p.id, p.serialize())


if __name__ == "__main__":
    # quick self‑test
    m = PlayerManager()
    p1 = m.create_player("warrior")
    p2 = m.create_player("mage")
    print(f"[TEST] Created {len(m.players)} test players inside city.")
    for pid, p in m.players.items():
        print(f" - {pid}: {p.class_name} L{p.level} @({p.x},{p.y})")

    p1.add_xp(250)
    m.save_all()
    print(f"[TEST] {p1.class_name} new lvl={p1.level}, HP={p1.stats['hp']}")