# ===============================================================
# Isekai Online - Login & Register Screen
# ===============================================================
import pygame

class LoginUI:
    def __init__(self, screen, font, ui_font):
        self.screen = screen
        self.font = font
        self.ui_font = ui_font
        self.username = ""
        self.password = ""
        self.mode = "LOGIN"  # or REGISTER

    def run(self):
        """Render loop; returns ('LOGIN'|'REGISTER', username, password)"""
        typing = "username"
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((25, 25, 35))
            title = self.ui_font.render(f"{self.mode} TO ISEKAI ONLINE", True, (255, 215, 0))
            self.screen.blit(title, (400 - title.get_width()//2, 100))

            # boxes
            self._draw_box("Username:", 240, typing == "username", self.username)
            self._draw_box("Password:", 280, typing == "password", "*"*len(self.password))

            tip = self.font.render(
                "TAB Switch | ENTER Confirm | F1 Register | F2 Login | ESC Quit", True, (200,200,200))
            self.screen.blit(tip, (400 - tip.get_width()//2, 350))

            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); raise SystemExit
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE: pygame.quit(); raise SystemExit
                    elif e.key == pygame.K_TAB:
                        typing = "password" if typing == "username" else "username"
                    elif e.key == pygame.K_RETURN:
                        return self.mode, self.username, self.password
                    elif e.key == pygame.K_F1: self.mode = "REGISTER"
                    elif e.key == pygame.K_F2: self.mode = "LOGIN"
                    elif e.key == pygame.K_BACKSPACE:
                        if typing == "username":
                            self.username = self.username[:-1]
                        else:
                            self.password = self.password[:-1]
                    else:
                        if len(e.unicode) == 1 and e.unicode.isprintable():
                            if typing == "username": self.username += e.unicode
                            else: self.password += e.unicode
            clock.tick(30)

    def _draw_box(self, label, y, active, text):
        l = self.font.render(label, True, (255,255,255))
        self.screen.blit(l, (200, y))
        rect = pygame.Rect(300, y-4, 300, 28)
        pygame.draw.rect(self.screen, (50,50,50), rect)
        pygame.draw.rect(self.screen, (255,255,255), rect, 2 if active else 1)
        val = self.font.render(text, True, (255,255,255))
        self.screen.blit(val, (310, y-2))