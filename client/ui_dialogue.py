# ===============================================================
# Isekai Online - Dialogue UI
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

class DialogueUI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.active = False
        self.current_dialogue = None
        self.current_line = 0
        self.lines = []
        self.speaker = ""

    def start_dialogue(self, speaker, lines):
        self.active = True
        self.speaker = speaker
        self.lines = lines
        self.current_line = 0

    def advance(self):
        self.current_line += 1
        if self.current_line >= len(self.lines):
            self.close()

    def close(self):
        self.active = False
        self.current_line = 0
        self.lines = []
        self.speaker = ""

    def draw(self):
        if not self.active or self.current_line >= len(self.lines):
            return

        # Large dialogue box centered
        box_w = 600
        box_h = 140
        box_x = (SCREEN_W - box_w) // 2
        box_y = SCREEN_H - box_h - 30
        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(self.screen, (20, 20, 30), box_rect)
        pygame.draw.rect(self.screen, (180, 150, 100), box_rect, 3)

        # Speaker name
        speaker_surf = self.font.render(self.speaker, True, (255, 215, 0))
        name_bg = pygame.Rect(box_x, box_y - 25, 200, 20)
        pygame.draw.rect(self.screen, (20, 20, 30), name_bg)
        pygame.draw.rect(self.screen, (180, 150, 100), name_bg, 2)
        self.screen.blit(speaker_surf, (box_x + 10, box_y - 25))

        # Text content (supports line breaks)
        text = self.lines[self.current_line].text
        # Simple word wrap for dialogue
        words = text.split()
        lines = []
        cur = ""
        for w in words:
            test = cur + w + " "
            if self.font.size(test)[0] > box_w - 20:
                lines.append(cur.strip())
                cur = w + " "
            else:
                cur = test
        if cur.strip():
            lines.append(cur.strip())
        y_offset = box_y + 10
        for i, line in enumerate(lines[:3]):  # max 3 lines visible
            surf = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(surf, (box_x + 10, y_offset + i * 25))

        # Advance prompt
        if self.current_line < len(self.lines) - 1:
            prompt_surf = self.font.render("Press SPACE to continue...", True, (150, 150, 150))
            self.screen.blit(prompt_surf, (box_x + box_w - 180, box_y + box_h - 25))
        else:
            close_prompt = self.font.render("Press SPACE to close...", True, (150, 150, 150))
            self.screen.blit(close_prompt, (box_x + box_w - 160, box_y + box_h - 25))