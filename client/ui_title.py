# ===============================================================
# Isekai Online - Title & Main Menu Screen
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


class TitleScreen:
    """Initial title and main menu before login"""

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.title_font = pygame.font.SysFont("Arial", 48, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.show_tips = False
        self.tip_timer = 0

    def show(self):
        """Display title screen and wait for player to continue"""
        waiting = True
        clock = pygame.time.Clock()
        
        while waiting:
            self.screen.fill((10, 5, 20))  # Dark purple background
            
            # Title
            title = self.title_font.render("ISEKAI ONLINE", True, (255, 215, 0))
            self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 80))
            
            # Subtitle
            subtitle = self.subtitle_font.render("A Journey Between Worlds", True, (180, 150, 200))
            self.screen.blit(subtitle, (SCREEN_W // 2 - subtitle.get_width() // 2, 150))
            
            # Story teaser
            teaser_font = pygame.font.SysFont("Arial", 18)
            teasers = [
                "You wake up in a strange world... unfamiliar, yet breathtaking.",
                "With no memory of how you got here, only one path remains:",
                "Forward. Into destiny. Toward home.",
                "",
                "Will you answer the call of adventure?"
            ]
            y_offset = 250
            for teaser in teasers:
                if teaser:
                    teaser_surf = teaser_font.render(teaser, True, (200, 200, 200))
                    self.screen.blit(teaser_surf, (SCREEN_W // 2 - teaser_surf.get_width() // 2, y_offset))
                y_offset += 35
            
            # Instructions
            instr_font = pygame.font.SysFont("Arial", 16)
            instr = instr_font.render("Press SPACE or CLICK to continue...", True, (100, 200, 255))
            self.screen.blit(instr, (SCREEN_W // 2 - instr.get_width() // 2, SCREEN_H - 80))
            
            # Version info
            ver_font = pygame.font.SysFont("Arial", 12)
            version = ver_font.render(cfg.GAME_VERSION, True, (100, 100, 100))
            self.screen.blit(version, (10, SCREEN_H - 20))
            
            pygame.display.flip()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            
            clock.tick(30)
    
    def show_loading(self):
        """Show loading screen while connecting"""
        clock = pygame.time.Clock()
        dots = 0
        for _ in range(60):  # 2 seconds at 30 FPS
            self.screen.fill((10, 5, 20))
            
            # Loading text
            loading_font = pygame.font.SysFont("Arial", 32, bold=True)
            loading = loading_font.render("Connecting to Isekai" + "." * (dots % 4), True, (100, 200, 255))
            self.screen.blit(loading, (SCREEN_W // 2 - loading.get_width() // 2, SCREEN_H // 2 - 50))
            
            # Progress bar
            bar_width = 300
            bar_height = 20
            bar_x = (SCREEN_W - bar_width) // 2
            bar_y = SCREEN_H // 2 + 50
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(self.screen, (100, 200, 255), (bar_x, bar_y, bar_width * (dots % 60) / 60, bar_height))
            
            pygame.display.flip()
            clock.tick(30)
            dots += 1
