# ===============================================================
# Isekai Online - Chat UI
# ===============================================================
import pygame
import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg

# Config constant
SCREEN_H = cfg.SCREEN_H

class ChatUI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.messages = []      # list[str]
        self.typing = False     # input mode on/off
        self.current = ""       # text being typed

    def toggle(self):
        self.typing = not self.typing
        if not self.typing:
            self.current = ""

    def add(self, name, text):
        msg = f"{name}: {text}"
        self.messages.append(msg)
        if len(self.messages) > 8:
            self.messages.pop(0)

    def draw(self):
        # history (last 8 lines)
        y = SCREEN_H - 110
        for m in self.messages:
            surf = self.font.render(m, True, (255, 255, 255))
            self.screen.blit(surf, (20, y))
            y += 15

        # input line
        if self.typing:
            pygame.draw.rect(self.screen, (20, 20, 20), (15, SCREEN_H - 30, 420, 18))
            txt = self.font.render(self.current, True, (255, 255, 255))
            self.screen.blit(txt, (18, SCREEN_H - 28))