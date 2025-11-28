# ===============================================================
# Isekai Online - Quest System (Server)
# ===============================================================
from typing import Dict

from shared.story import Quest, FIRST_QUEST


class QuestState:
    def __init__(self):
        self.active: Dict[str, Dict] = {}  # player_id -> quest data

    def give_first_quest(self, player_id: str):
        if player_id in self.active:
            return self.active[player_id]
        q = FIRST_QUEST
        data = {
            "id": q.id,
            "name": q.name,
            "objective": q.objective,
            "required": q.required,
            "progress": 0,
            "reward_xp": q.reward_xp,
        }
        self.active[player_id] = data
        return data

    def increment(self, player_id: str, key: str):
        # currently only supports slime kill objective
        q = self.active.get(player_id)
        if not q:
            return None
        if key == "slime":
            q["progress"] = min(q["required"], q["progress"] + 1)
        return q

    def check_complete(self, player_id: str):
        q = self.active.get(player_id)
        if not q:
            return None
        return q["progress"] >= q["required"]
