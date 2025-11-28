# ===============================================================
# Isekai Online - Enhanced Combat System (All Enemy Types)
# ===============================================================
import random
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg
from server.player import PlayerManager

# Config constants
ATTACK_RANGE = cfg.ATTACK_RANGE
BASE_ATTACK_MIN = cfg.BASE_ATTACK_MIN
BASE_ATTACK_MAX = cfg.BASE_ATTACK_MAX
LEVEL_DAMAGE_BONUS = cfg.LEVEL_DAMAGE_BONUS


class EnhancedCombatSystem:
    """Enhanced combat system that works with the new enemy manager"""

    def __init__(self, player_mgr: PlayerManager, enemy_mgr):
        self.players = player_mgr
        self.enemies = enemy_mgr

    def player_attack(self, attacker_id: str):
        """Perform an attack from a player toward nearby enemies"""
        if attacker_id not in self.players.players:
            return {"result": "fail", "reason": "Invalid player."}

        attacker = self.players.players[attacker_id]
        px, py = attacker.x, attacker.y
        attacked_enemy = None
        combat_result = {}

        # Check all enemies for attack range
        for enemy_id, enemy in list(self.enemies.enemies.items()):
            dist = ((enemy["x"] - px) ** 2 + (enemy["y"] - py) ** 2) ** 0.5
            if dist < ATTACK_RANGE:  # attack range from config
                attacked_enemy = enemy_id
                
                # Calculate damage based on player's stats (can be enhanced)
                dmg = random.randint(BASE_ATTACK_MIN, BASE_ATTACK_MAX) + (attacker.level * LEVEL_DAMAGE_BONUS)
                
                # Apply damage
                enemy["hp"] -= dmg
                
                combat_result = {
                    "result": "hit",
                    "attacker": attacker_id,
                    "enemy_id": enemy_id,
                    "damage": dmg,
                    "enemy_hp": enemy["hp"],
                    "enemy_max_hp": enemy["max_hp"],
                    "enemy_type": enemy["type"],
                    "xp": enemy["xp"],
                }
                
                # Handle different enemy types for quest progress
                if enemy["type"] == "slime":
                    combat_result["notify_type"] = "SLIME_KILL"  # for quest progress
                elif enemy["type"] == "goblin":
                    combat_result["notify_type"] = "GOBLIN_KILL"
                elif enemy["type"] == "ogre":
                    combat_result["notify_type"] = "OGRE_KILL"

                # Enemy dies
                if enemy["hp"] <= 0:
                    self.enemies.remove_enemy(enemy_id)
                    self.enemies.respawn_enemy()  # Spawn a new enemy
                        
                    # Give XP to player
                    attacker.add_xp(enemy["xp"])
                    
                    combat_result["result"] = "kill"
                    combat_result["xp_gained"] = enemy["xp"]
                    combat_result["enemy_type"] = enemy["type"]
                    combat_result["new_level"] = attacker.level

                break

        if not attacked_enemy:
            combat_result = {"result": "miss", "reason": "No enemy nearby."}

        return combat_result


if __name__ == "__main__":
    # --- Standalone Test ---
    from server.player import PlayerManager
    from server.enemies import EnemyManager

    pm = PlayerManager()
    em = EnemyManager()
    em.spawn_initial_enemies(25)  # Test with fewer enemies
    
    p = pm.create_player("warrior")

    combat = EnhancedCombatSystem(pm, em)
    print(f"[Test] Player {p.id} attacking...")
    
    result = combat.player_attack(p.id)
    print("[Combat Result]:", result)
    print("[Player State]:", pm.get_state()[p.id])