# ===============================================================
# Isekai Online - NPC System (Server)
# ===============================================================
from typing import Dict
from shared.story import START_DIALOGUE
from server.world import in_city


class NPCManager:
    def __init__(self):
        # Simple single NPC in city center (Guild Master)
        self.npcs: Dict[str, dict] = {
            "guild": {
                "name": "Guild Master",
                "x": 1200,
                "y": 1200,
                "dialogue": START_DIALOGUE.id,
            }
        }

    def get_state(self):
        return self.npcs

    def nearby(self, x: float, y: float, radius: float = 80):
        for nid, n in self.npcs.items():
            dx, dy = n["x"] - x, n["y"] - y
            if (dx * dx + dy * dy) ** 0.5 <= radius:
                return nid, n
        return None, None
