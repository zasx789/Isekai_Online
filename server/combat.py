# ===============================================================
# Isekai Online - Combat System
# ===============================================================
# Handles fighting logic between players and mobs.

import random
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg
from server.mobs import MobManager
from server.player import PlayerManager

# Config constants
XP_FROM_SLIME = cfg.XP_FROM_SLIME
ATTACK_RANGE = cfg.ATTACK_RANGE
BASE_ATTACK_MIN = cfg.BASE_ATTACK_MIN
BASE_ATTACK_MAX = cfg.BASE_ATTACK_MAX
LEVEL_DAMAGE_BONUS = cfg.LEVEL_DAMAGE_BONUS


class CombatSystem:
    """Manages combat actions and results."""

    def __init__(self, player_mgr: PlayerManager, mob_mgr: MobManager):
        self.players = player_mgr
        self.mobs = mob_mgr

    def player_attack(self, attacker_id: str):
        """Perform an attack from a player toward nearby mobs."""

        if attacker_id not in self.players.players:
            return {"result": "fail", "reason": "Invalid player."}

        attacker = self.players.players[attacker_id]
        px, py = attacker.x, attacker.y

        hit_mob_id = None
        combat_result = {}

        for mid, mob in list(self.mobs.mobs.items()):
            dist = ((mob["x"] - px) ** 2 + (mob["y"] - py) ** 2) ** 0.5
            if dist < ATTACK_RANGE:  # attack range from config
                hit_mob_id = mid
                dmg = random.randint(BASE_ATTACK_MIN, BASE_ATTACK_MAX) + (attacker.level * LEVEL_DAMAGE_BONUS)
                mob["hp"] -= dmg

                combat_result = {
                    "result": "hit",
                    "attacker": attacker_id,
                    "mob_id": mid,
                    "damage": dmg,
                    "mob_hp": mob["hp"],
                }

                # Mob dies
                if mob["hp"] <= 0:
                    self.mobs.remove_mob(mid)
                    self.mobs.respawn_mob()
                    attacker.add_xp(XP_FROM_SLIME)
                    combat_result["result"] = "kill"
                    combat_result["xp_gained"] = XP_FROM_SLIME
                    combat_result["notify_type"] = "SLIME_KILL"  # for quest progress
                    combat_result["new_level"] = attacker.level

                    break

        if not hit_mob_id:
            combat_result = {"result": "miss", "reason": "No mob nearby."}

        return combat_result


if __name__ == "__main__":
    # --- Standalone Test ---
    from Isekai_Online.server.player import PlayerManager
    from Isekai_Online.server.mobs import MobManager

    pm = PlayerManager()
    mm = MobManager()
    mm.spawn_initial_mobs()
    p = pm.create_player("warrior")

    combat = CombatSystem(pm, mm)
    print(f"[Test] Player {p.id} attacking...")

    result = combat.player_attack(p.id)
    print("[Combat Result]:", result)
    print("[Player State]:", pm.get_state()[p.id])