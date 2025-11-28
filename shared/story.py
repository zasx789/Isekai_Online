# ===============================================================
# Isekai Online - Story and Quest Data
# ===============================================================
# Minimal shared structures describing dialogues and quests.

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class DialogueLine:
    speaker: str
    text: str


@dataclass
class Dialogue:
    id: str
    lines: List[DialogueLine]
    next_id: Optional[str] = None  # simple linear flow for now


@dataclass
class Quest:
    id: str
    name: str
    description: str
    objective: str
    progress_key: str  # key in server state to track progress
    required: int = 1
    reward_xp: int = 50


# Sample starting story and first quest (Way Back Home - Prologue)
START_DIALOGUE = Dialogue(
    id="intro",
    lines=[
        DialogueLine("Mysterious Voice", "Wake up, traveler... this world is not your own."),
        DialogueLine("Mysterious Voice", "If you seek a way home, begin by proving your will."),
        DialogueLine("Guild Master", "Welcome to Haven City. Slimes gather outside our walls—deal with them."),
    ],
    next_id=None,
)

FIRST_QUEST = Quest(
    id="q_slime_cull",
    name="First Steps",
    description="Defeat 3 slimes outside the city to earn the Guild's trust.",
    objective="Defeat slimes",
    progress_key="slimes_killed",
    required=3,
    reward_xp=100,
)
