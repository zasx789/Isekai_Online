# ===============================================================
# Isekai Online - Enhanced Quest System (Server)
# ===============================================================
from typing import Dict, Optional

from shared.story_enhanced import Quest, QUEST_REGISTRY


class QuestState:
    def __init__(self):
        self.active: Dict[str, Dict] = {}  # player_id -> quest data
        self.completed: Dict[str, list] = {}  # player_id -> list of completed quest IDs

    def give_quest(self, player_id: str, quest_id: str):
        if player_id in self.active:
            return self.active[player_id]
        
        q = QUEST_REGISTRY.get(quest_id)
        if not q:
            return None
        
        data = {
            "id": q.id,
            "name": q.name,
            "description": q.description,
            "objective": q.objective,
            "required": q.required,
            "progress": 0,
            "reward_xp": q.reward_xp,
        }
        self.active[player_id] = data
        return data

    def give_first_quest(self, player_id: str):
        """Give the first quest in the story line"""
        return self.give_quest(player_id, "q_slime_cull")

    def increment(self, player_id: str, progress_key: str):
        q = self.active.get(player_id)
        if not q:
            return None
        
        if q["progress_key"] == progress_key:
            q["progress"] = min(q["required"], q["progress"] + 1)
        return q

    def check_complete(self, player_id: str):
        q = self.active.get(player_id)
        if not q:
            return None
        return q["progress"] >= q["required"]
    
    def complete_quest(self, player_id: str):
        """Mark current quest as complete and get next quest if available"""
        if player_id not in self.active:
            return None
            
        q = self.active[player_id]
        quest_id = q["id"]
        quest = QUEST_REGISTRY.get(quest_id)
        
        # Add to completed
        if player_id not in self.completed:
            self.completed[player_id] = []
        self.completed[player_id].append(quest_id)
        
        # Remove from active
        del self.active[player_id]
        
        # Get next quest if available
        next_quest_id = quest.next_quest_id if quest else None
        return next_quest_id