# ===============================================================
# Isekai Online - Enemy System with Multiple Types
# ===============================================================
import uuid
import random
from typing import Dict, List

from config import TILE_SIZE, CITY, CITY_SPAWN
from shared.biome import is_safe_spawn
from server.world import in_city


class EnemyTypes:
    """Registry for all enemy types with stats by level"""
    
    @staticmethod
    def get_stats(enemy_type: str, level: int):
        """Get stats for an enemy type based on level scaling"""
        base_stats = {
            "slime": {
                "hp": 25,
                "attack": 5,
                "xp": 35,
                "speed": 2.0,
                "color": (0, 200, 50),
                "size": 32,
                "level_variance": 1.0,  # HP growth per level
            },
            "goblin": {
                "hp": 40,
                "attack": 12,
                "xp": 80,
                "speed": 2.5,
                "color": (100, 50, 30),
                "size": 40,
                "level_variance": 1.2,
            },
            "ogre": {
                "hp": 120,
                "attack": 20,
                "xp": 200,
                "speed": 1.2,
                "color": (150, 80, 40),
                "size": 64,
                "level_variance": 1.4,
            },
            "demon_slime": {
                "hp": 60,
                "attack": 18,
                "xp": 150,
                "speed": 2.8,
                "color": (180, 50, 100),
                "size": 48,
                "level_variance": 1.3,
            },
            "orc": {
                "hp": 80,
                "attack": 22,
                "xp": 180,
                "speed": 2.2,
                "color": (100, 100, 50),
                "size": 56,
                "level_variance": 1.35,
            },
        }
        
        stats = base_stats.get(enemy_type, base_stats["slime"])
        
        # Scale stats based on level
        scaled_stats = {
            "hp": int(stats["hp"] * (1 + stats["level_variance"] * (level - 1) * 0.2)),
            "attack": stats["attack"] + int(level * 2),
            "xp": stats["xp"] + level * 15,
            "speed": stats["speed"] * (1 + level * 0.05),
            "color": stats["color"],
            "size": stats["size"],
        }
        
        return scaled_stats


class SpawnZone:
    """Represents a zone where certain enemies can spawn"""
    def __init__(self, name: str, x_min: float, x_max: float, y_min: float, y_max: float, 
                 enemy_types: List[str], min_level: int, max_level: int):
        self.name = name
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.enemy_types = enemy_types
        self.min_level = min_level
        self.max_level = max_level


class EnemyManager:
    """Enhanced enemy management with zones and types"""
    
    def __init__(self):
        self.enemies: Dict[str, dict] = {}
        self.zones: List[SpawnZone] = []
        self.setup_world_zones()
        
    def setup_world_zones(self):
        """Set up the different zones with appropriate enemies"""
        self.zones = [
            # Zone 1: Safe zone (castle) - no enemies spawn
            SpawnZone(
                name="Castle",
                x_min=CITY["x"], 
                x_max=CITY["x"] + CITY["w"],
                y_min=CITY["y"], 
                y_max=CITY["y"] + CITY["h"],
                enemy_types=[],
                min_level=1,
                max_level=1
            ),
            
            # Zone 2: Grasslands around castle - slimes and weak goblins
            SpawnZone(
                name="Grasslands",
                x_min=CITY["x"] - 300,
                x_max=CITY["x"] + CITY["w"] + 300,
                y_min=CITY["y"] - 300,
                y_max=CITY["y"] + CITY["h"] + 300,
                enemy_types=["slime", "goblin"],  # Both can spawn
                min_level=1,
                max_level=5
            ),
            
            # Zone 3: Eastern plains - stronger goblins and demon slimes
            SpawnZone(
                name="Eastern Plains",
                x_min=CITY["x"] + CITY["w"] + 300,
                x_max=CITY["x"] + CITY["w"] + 900,
                y_min=CITY["y"] + 0,
                y_max=CITY["y"] + CITY["h"],
                enemy_types=["goblin", "demon_slime"],
                min_level=4,
                max_level=12
            ),
            
            # Zone 4: Southern ruins - ogres and orcs
            SpawnZone(
                name="Southern Ruins",
                x_min=CITY["x"] - 300,
                x_max=CITY["x"] + CITY["w"],
                y_min=CITY["y"] + CITY["h"] + 300,
                y_max=CITY["y"] + CITY["h"] + 900,
                enemy_types=["ogre", "orc"],
                min_level=8,
                max_level=20
            ),
        ]
    
    def find_zone(self, x: float, y: float) -> Optional[SpawnZone]:
        """Find which zone contains these coordinates"""
        for zone in self.zones:
            if zone.x_min <= x <= zone.x_max and zone.y_min <= y <= zone.y_max:
                return zone
        return None
    
    def spawn_enemy(self, zone: SpawnZone = None):
        """Spawn a single enemy, optionally in a specific zone"""
        # If no zone specified, pick one based on probability
        if zone is None:
            zone = random.choice(self.zones)
        
        # Skip if zone has no enemy types
        if not zone.enemy_types:
            return None
        
        enemy_type = random.choice(zone.enemy_types)
        level = random.randint(zone.min_level, zone.max_level)
        
        # Try many times to find a safe position
        for _ in range(120):
            x, y = random.uniform(zone.x_min, zone.x_max), random.uniform(zone.y_min, zone.y_max)
            
            # Must be safe terrain and NOT inside the castle
            if is_safe_spawn(x, y) and not in_city(x, y):
                enemy_id = str(uuid.uuid4())[:4]
                stats = EnemyTypes.get_stats(enemy_type, level)
                
                self.enemies[enemy_id] = {
                    "type": enemy_type,
                    "x": x,
                    "y": y,
                    "hp": stats["hp"],
                    "max_hp": stats["hp"],
                    "attack": stats["attack"],
                    "xp": stats["xp"],
                    "speed": stats["speed"],
                    "color": stats["color"],
                    "lvl": level,
                    "size": stats["size"],
                }
                return enemy_id
        return None
    
    def spawn_initial_enemies(self count=75):
        """Spawn multiple enemies at startup"""
        for _ in range(count):
            self.spawn_enemy()
    
    def remove_enemy(self, enemy_id: str):
        """Remove an enemy when defeated"""
        self.enemies.pop(enemy_id, None)
    
    def respawn_enemy(self):
        """Respawn one new enemy where one died"""
        self.spawn_enemy()
    
    def get_state(self) -> Dict:
        """Return full enemy dictionary for sync with clients"""
        return self.enemies
    
    def get_enemies_by_type(self, enemy_type: str) -> List:
        """Get all enemies of a specific type"""
        return [eid for eid, e in self.enemies.items() if e["type"] == enemy_type]