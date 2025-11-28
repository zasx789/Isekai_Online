# ===============================================================
# Isekai Online - Auto Skill System (class-based + level scaling)
# ===============================================================

import random
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg

# Config constants
XP_FROM_SLIME = cfg.XP_FROM_SLIME
WARRIOR_SKILL_RANGE = cfg.WARRIOR_SKILL_RANGE
MAGE_SKILL_RANGE = cfg.MAGE_SKILL_RANGE
ROGUE_SKILL_RANGE = cfg.ROGUE_SKILL_RANGE
NINJA_SKILL_RANGE = cfg.NINJA_SKILL_RANGE


class SkillManager:
    """Handles class‑specific skills that scale with level."""

    def __init__(self, players, mobs):
        self.players = players
        self.mobs = mobs

    # -----------------------------------------------------------
    def use_skill(self, caster_id, skill_name=None):
        """Cast the proper skill for the class.  If skill_name is None,
        uses the default for that player's class automatically."""
        caster = self.players.players.get(caster_id)
        if not caster:
            return {"events": [], "error": "no caster"}

        # auto‑select based on class
        if skill_name is None:
            cname = caster.class_name.lower()
            if cname == "warrior":
                skill_name = "PowerStrike"
            elif cname == "mage":
                skill_name = "Fireball"
            elif cname == "paladin":
                skill_name = "HealLight"
            elif cname == "rogue":
                skill_name = "ShadowStep"
            elif cname == "ninja":
                skill_name = "WindSlash"
            else:
                skill_name = "PowerStrike"

        px, py = caster.x, caster.y
        lvl = caster.level
        events = []

        # -----------------------------------------------------------
        # WARRIOR - PowerStrike: heavy dmg single target
        # -----------------------------------------------------------
        if skill_name == "PowerStrike":
            dmg = random.randint(30, 50) + lvl * 5
            for mid, mob in list(self.mobs.mobs.items()):
                dist = ((mob["x"] - px) ** 2 + (mob["y"] - py) ** 2) ** 0.5
                if dist < WARRIOR_SKILL_RANGE:
                    mob["hp"] -= dmg
                    events.append({"type": "hit", "mob": mid, "damage": dmg})
                    if mob["hp"] <= 0:
                        caster.add_xp(XP_FROM_SLIME)
                        self.mobs.remove_mob(mid)
                        self.mobs.respawn_mob()
                    break
            if not events:
                events.append({"type": "miss"})

        # -----------------------------------------------------------
        # MAGE - Fireball: area attack around player
        # -----------------------------------------------------------
        elif skill_name == "Fireball":
            radius = MAGE_SKILL_RANGE + lvl * 5
            base = random.randint(25, 35) + lvl * 3
            hits = 0
            for mid, mob in list(self.mobs.mobs.items()):
                dist = ((mob["x"] - px)**2 + (mob["y"] - py)**2)**0.5
                if dist < radius:
                    hits += 1
                    mob["hp"] -= base
                    events.append({"type": "aoe_hit", "mob": mid, "damage": base})
                    if mob["hp"] <= 0:
                        caster.add_xp(XP_FROM_SLIME)
                        self.mobs.remove_mob(mid)
                        self.mobs.respawn_mob()
            if hits == 0:
                events.append({"type": "miss"})

        # -----------------------------------------------------------
        # PALADIN - HealLight: heal increases with level
        # -----------------------------------------------------------
        elif skill_name == "HealLight":
            heal = random.randint(40, 60) + lvl * 8
            caster.stats["hp"] = min(
                caster.stats["max_hp"], caster.stats["hp"] + heal)
            events.append({"type": "heal", "target": caster_id, "amount": heal})

        # -----------------------------------------------------------
        # ROGUE - ShadowStep: blink behind nearest target + dmg
        # -----------------------------------------------------------
        elif skill_name == "ShadowStep":
            dmg = 20 + lvl * 4
            for mid, mob in list(self.mobs.mobs.items()):
                dist = ((mob["x"] - px)**2 + (mob["y"] - py)**2)**0.5
                if dist < ROGUE_SKILL_RANGE:
                    mob["hp"] -= dmg
                    caster.x, caster.y = mob["x"] - 20, mob["y"] + 5
                    events.append({"type": "step_hit", "mob": mid, "damage": dmg})
                    if mob["hp"] <= 0:
                        caster.add_xp(XP_FROM_SLIME)
                        self.mobs.remove_mob(mid)
                        self.mobs.respawn_mob()
                    break
            if not events:
                events.append({"type": "miss"})

        # -----------------------------------------------------------
        # NINJA - WindSlash: line attack, hits several in row
        # -----------------------------------------------------------
        elif skill_name == "WindSlash":
            dmg = 15 + lvl * 3
            range_x = NINJA_SKILL_RANGE
            count = 0
            for mid, mob in list(self.mobs.mobs.items()):
                if abs(mob["y"] - py) < 40 and 0 < mob["x"] - px < range_x:
                    mob["hp"] -= dmg
                    count += 1
                    events.append({"type": "slash_hit", "mob": mid, "damage": dmg})
                    if mob["hp"] <= 0:
                        caster.add_xp(XP_FROM_SLIME)
                        self.mobs.remove_mob(mid)
                        self.mobs.respawn_mob()
            if count == 0:
                events.append({"type": "miss"})

        # future classes can be appended here

        return {"skill": skill_name, "events": events}