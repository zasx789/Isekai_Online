# ===============================================================
# Isekai Online - Shared Configuration
# ===============================================================
# This file holds constants and settings shared between the
# client and server. Import it anywhere you need base settings.
# Example:
#   from Isekai_Online.config import HOST, PORT, TILE_SIZE

# --- Network ---
HOST = "127.0.0.1"
PORT = 8765

# --- Screen ---
SCREEN_W = 800
SCREEN_H = 600

# --- World ---
TILE_SIZE = 64

# --- Player Defaults ---
DEFAULT_STATS = {
    "warrior": {"hp": 100, "mp": 30, "atk": 12, "def": 6},
    "mage": {"hp": 70, "mp": 80, "atk": 18, "def": 3},
    "rogue": {"hp": 85, "mp": 40, "atk": 15, "def": 4},
}

# --- XP System ---
XP_PER_LEVEL = 100
XP_FROM_SLIME = 35

# --- Performance ---
TICK_RATE = 60  # frames per second for client

# --- Version ---
GAME_VERSION = "v0.5 (Architecture Update)"
#--- City (safe zone) ---
CITY = {
"x": 900, # top-left of city in world coords
"y": 900,
"w": 600, # width
"h": 600, # height
}
CITY_SPAWN = (CITY["x"] + CITY["w"] // 2, CITY["y"] + CITY["h"] // 2)

# --- Movement ---
PLAYER_SPEED = 5
MOVEMENT_VALIDATION_TOLERANCE = 8

# --- Combat ---
ATTACK_RANGE = 80
SKILL_RANGE = 100
BASE_ATTACK_MIN = 10
BASE_ATTACK_MAX = 20
LEVEL_DAMAGE_BONUS = 5

# --- Mobs ---
INITIAL_MOB_COUNT = 25
MOB_MIN_LEVEL = 1
MOB_MAX_LEVEL = 20
MOB_BASE_HP = 25
MOB_HP_PER_LEVEL = 10

# --- Skills ---
WARRIOR_SKILL_RANGE = 100
MAGE_SKILL_RANGE = 140
ROGUE_SKILL_RANGE = 120
NINJA_SKILL_RANGE = 220

# Game balance thresholds (prevent cheating)
MAX_MOVE_DISTANCE = 10
