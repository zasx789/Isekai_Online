import pygame, sys
pygame.init()
screen = pygame.display.set_mode((400, 200))
font = pygame.font.SysFont(None, 24)
running = True
while running:
    screen.fill((20, 20, 20))
    text = font.render("Press keys. Close window to exit.", True, (255,255,255))
    screen.blit(text, (20, 90))
    pygame.display.flip()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            print("KEYDOWN:", e.key, file=sys.stderr, flush=True)
pygame.quit()