# ===============================================================
# Isekai Online - Enhanced Story System with Multiple Quests
# ===============================================================

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DialogueLine:
    speaker: str
    text: str

@dataclass  
class Dialogue:
    id: str
    lines: List[DialogueLine]
    next_id: Optional[str] = None

@dataclass
class Quest:
    id: str
    name: str
    description: str
    objective: str
    progress_key: str
    required: int = 1
    reward_xp: int = 50
    next_quest_id: Optional[str] = None

# ==============================================
# QUEST LINE 1: "WAY BACK HOME - THE BEGINNING"
# ==============================================

DIALOGUE_INTRO = Dialogue(
    id="intro",
    lines=[
        DialogueLine("Mysterious Voice", "Wake up, traveler... this world is not your own."),
        DialogueLine("Mysterious Voice", "If you seek a way home, begin by proving your will."),
        DialogueLine("Guild Master", "Welcome to Haven City. I am Commander Aldus."),
        DialogueLine("Guild Master", "The slimes gather outside our walls. Deal with them first."),
    ],
)

QUEST_1 = Quest(
    id="q_slime_cull",
    name="First Steps",
    description="Defeat 3 slimes outside Haven City to earn the Guild's trust.",
    objective="Defeat slimes",
    progress_key="slimes_killed",
    required=3,
    reward_xp=100,
    next_quest_id="q_scout_goblins"
)

# ==============================================
# QUEST LINE 2: "SCOUTING THE REALM"
# ==============================================

DIALOGUE_QUEST_2 = Dialogue(
    id="quest2_start",
    lines=[
        DialogueLine("Guild Master", "Well done, traveler. The slimes no longer plague us."),
        DialogueLine("Guild Master", "But there are greater threats beyond our walls."),
        DialogueLine("Guild Master", "Scout the grasslands. We've heard of goblin activity to the east."),
        DialogueLine("Guild Master", "Defeat 5 goblins and report back. We must understand this threat."),
    ],
)

QUEST_2 = Quest(
    id="q_scout_goblins",
    name="Scout's Duty",
    description="Venture east and defeat 5 goblins to understand the goblin threat.",
    objective="Defeat goblins",
    progress_key="goblins_killed",
    required=5,
    reward_xp=250,
    next_quest_id="q_dungeon_entrance"
)

# ==============================================
# QUEST LINE 3: "THE DUNGEON BECKONS"
# ==============================================

DIALOGUE_QUEST_3 = Dialogue(
    id="quest3_start",
    lines=[
        DialogueLine("Guild Master", "Your reports are troubling, traveler."),
        DialogueLine("Guild Master", "The goblins seem to be fleeing something greater..."),
        DialogueLine("Guild Master", "To the south lies an ancient ruin - likely a dungeon."),
        DialogueLine("Guild Master", "Venture there and discover what lurks within. Defeat 3 ogres."),
        DialogueLine("Guild Master", "Only then can we understand the true threat to our realm."),
    ],
)

QUEST_3 = Quest(
    id="q_dungeon_entrance",
    name="Into the Darkness",
    description="Explore the ancient dungeon to the south and defeat 3 ogres.",
    objective="Defeat ogres",
    progress_key="ogres_killed",
    required=3,
    reward_xp=500,
    next_quest_id=None  # Final quest in this arc
)

# Registry to get quest by ID
QUEST_REGISTRY = {
    "q_slime_cull": QUEST_1,
    "q_scout_goblins": QUEST_2,
    "q_dungeon_entrance": QUEST_3,
}

DIALOGUE_REGISTRY = {
    "intro": DIALOGUE_INTRO,
    "quest2_start": DIALOGUE_QUEST_2,
    "quest3_start": DIALOGUE_QUEST_3,
}
