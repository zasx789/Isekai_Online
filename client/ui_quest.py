# ===============================================================
# Isekai Online - Quest UI
# ===============================================================
import pygame
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg

SCREEN_W = cfg.SCREEN_W
SCREEN_H = cfg.SCREEN_H

class QuestUI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.quest = None
        self.active = False
        self.completed_quest = None
        self.complete_timer = 0

    def set_quest(self, quest_data):
        if quest_data:
            self.quest = quest_data
            self.active = True

    def update(self):
        if self.complete_timer > 0:
            self.complete_timer -= 1
            if self.complete_timer == 0:
                self.completed_quest = None

    def complete_quest(self, xp_amount):
        self.completed_quest = self.quest
        self.quest = None
        self.active = False
        self.complete_timer = 180  # seconds

    def draw(self):
        if not self.active and not self.completed_quest:
            return

        # Quest tracker box (top right)
        if self.active and self.quest:
            # Box
            box_rect = pygame.Rect(SCREEN_W - 220, 10, 210, 80)
            pygame.draw.rect(self.screen, (40, 40, 40), box_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), box_rect, 2)
            # Title
            title = self.font.render(f"Quest: {self.quest['name']}", True, (255, 215, 0))
            self.screen.blit(title, (SCREEN_W - 210, 15))
            # Objective
            obj = self.font.render(f"{self.quest['objective']}: {self.quest['progress']}/{self.quest['required']}", True, (200, 200, 200))
            self.screen.blit(obj, (SCREEN_W - 210, 35))
            # Reward
            rew = self.font.render(f"Reward: {self.quest['reward_xp']} XP", True, (100, 200, 100))
            self.screen.blit(rew, (SCREEN_W - 210, 55))

        # Quest complete notification (bottom center)
        if self.completed_quest and self.complete_timer:
            # Background box
            notif_rect = pygame.Rect(SCREEN_W//2 - 150, SCREEN_H - 100, 300, 60)
            pygame.draw.rect(self.screen, (0, 80, 0), notif_rect)
            pygame.draw.rect(self.screen, (0, 255, 0), notif_rect, 3)
            # Text
            complete = self.font.render(f"{self.completed_quest['name']}", True, (255, 255, 255))
            self.screen.blit(complete, (SCREEN_W//2 - complete.get_width()//2, SCREEN_H - 90))
            reward = self.font.render(f"+{self.completed_quest['reward_xp']} XP!", True, (255, 215, 0))
            self.screen.blit(reward, (SCREEN_W//2 - reward.get_width()//2, SCREEN_H - 65))