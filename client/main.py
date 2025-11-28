# ===============================================================
# Isekai Online - Client Main (Login + Chat + Combat)
# ===============================================================

import asyncio
import json
import pygame

import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

import config as cfg
import assets_generator
from client.engine import RenderEngine
from client.ui import GameUI
from client.ui_login import LoginUI
from client.ui_chat import ChatUI
from client.ui_quest import QuestUI
from client.ui_dialogue import DialogueUI
from client.visual_fx import VFXManager
from client.ui_title import TitleScreen
# Story data
from shared.story import START_DIALOGUE

# Config constants
SCREEN_W = cfg.SCREEN_W
SCREEN_H = cfg.SCREEN_H
HOST = cfg.HOST
PORT = cfg.PORT
TICK_RATE = cfg.TICK_RATE
PLAYER_SPEED = cfg.PLAYER_SPEED

# Assets function
generate_assets = assets_generator.generate_assets


class GameClient:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Isekai Online")

        print("[Client] Initializing...")
        generate_assets()

        # window & fonts
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.ui_font = pygame.font.SysFont("Arial", 20, bold=True)

        # Show title screen
        title_screen = TitleScreen(self.screen, self.font)
        title_screen.show()

        # assets
        self.imgs = {
            "warrior": pygame.image.load("assets/warrior.png").convert_alpha(),
            "mage": pygame.image.load("assets/mage.png").convert_alpha(),
            "rogue": pygame.image.load("assets/rogue.png").convert_alpha(),
            "slime": pygame.image.load("assets/slime.png").convert_alpha(),
            "tree": pygame.image.load("assets/tree.png").convert_alpha(),
            "grass": pygame.image.load("assets/grass.png").convert(),
            "water": pygame.image.load("assets/water.png").convert(),
            "sand": pygame.image.load("assets/sand.png").convert(),
        }

        # subsystems
        self.engine = RenderEngine(self.screen, self.imgs, self.font)
        self.ui = GameUI(self.screen, self.font)
        self.chat = ChatUI(self.screen, self.font)
        self.quest_ui = QuestUI(self.screen, self.font)
        self.dialogue_ui = DialogueUI(self.screen, self.font)
        self.vfx = VFXManager()
        self.npcs = {}

        # runtime state
        self.ws = None
        self.my_id = None
        self.my_class = "warrior"
        self.players = {}
        self.mobs = {}
        self.username = ""
        self.password = ""
        self.mode = "LOGIN"  # or REGISTER
        self.running = True

    # -----------------------------------------------------------
    # Class selection (used only for REGISTER)
    # -----------------------------------------------------------
    def select_class_screen(self):
        selected = False
        while not selected:
            self.screen.fill((30, 30, 30))
            title = self.ui_font.render("CHOOSE YOUR HERO", True, (255, 215, 0))
            self.screen.blit(title, (SCREEN_W // 2 - title.get_width() // 2, 100))

            classes = [("warrior", 200), ("mage", 400), ("rogue", 600)]
            mx, my = pygame.mouse.get_pos()

            for name, x in classes:
                r = pygame.Rect(x - 50, 250, 100, 100)
                color = (100, 100, 100) if r.collidepoint((mx, my)) else (50, 50, 50)
                if r.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
                    self.my_class = name
                    selected = True

                pygame.draw.rect(self.screen, color, r)
                pygame.draw.rect(self.screen, (255, 255, 255), r, 2)
                self.screen.blit(pygame.transform.scale(self.imgs[name], (80, 80)), (x - 40, 260))
                txt = self.font.render(name.upper(), True, (255, 255, 255))
                self.screen.blit(txt, (x - txt.get_width() // 2, 360))

            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
            self.clock.tick(30)

    # -----------------------------------------------------------
    # Networking
    # -----------------------------------------------------------
    async def connect(self):
        import websockets
        try:
            self.ws = await websockets.connect(f"ws://{HOST}:{PORT}")

            # First packet decides flow: REGISTER / LOGIN
            payload = {"type": self.mode, "username": self.username, "password": self.password}
            if self.mode == "REGISTER":
                payload["class"] = self.my_class
            await self.ws.send(json.dumps(payload))

            print("[Client] Connected.")
            return True
        except Exception as e:
            print("[Client] Connection failed:", e)
            return False

    async def receiver(self):
        try:
            async for msg in self.ws:
                data = json.loads(msg)
                t = data.get("type")
                if t == "INIT":
                    self.my_id = data["id"]
                    self.players = data["state"]
                    self.mobs = data["mobs"]
                    self.npcs = data.get("npcs", {})
                    print(f"[Client] Joined as {self.my_id}")
                    # Setup quest if any
                    if "quest" in data and data["quest"]:
                        self.quest_ui.set_quest(data["quest"])
                elif t == "JOIN":
                    self.players[data["id"]] = data["data"]
                elif t == "UPDATE":
                    pid = data["id"]
                    if pid in self.players:
                        self.players[pid]["x"] = data["x"]
                        self.players[pid]["y"] = data["y"]
                elif t == "COMBAT":
                    self.players[data["attacker"]] = data["p_data"]
                    self.mobs = data.get("mobs", self.mobs)
                    result = data.get("result", {})
                    if result.get("result") == "hit":
                        mid = result.get("mob_id")
                        dmg = result.get("damage")
                        if mid is not None and dmg is not None and mid in self.mobs:
                            mob = self.mobs[mid]
                            self.vfx.add_damage(mob["x"], mob["y"], dmg)
                            self.vfx.add_shake(1)
                    elif result.get("result") == "kill":
                        mid = result.get("mob_id")
                        dmg = result.get("damage")
                        if mid is not None and dmg is not None:
                            # Show damage numbers for last hit
                            self.vfx.add_damage(self.mobs.get(mid, {"x":0,"y":0})["x"], self.mobs.get(mid, {"x":0,"y":0})["y"], dmg, is_crit=True)
                            self.vfx.add_shake(3)
                elif t == "SKILL_FX":
                    # Trigger visual effects for skill usage
                    attacker = data.get("attacker")
                    skill_name = data.get("skill")
                    result = data.get("result", {})
                    if "events" in result:
                        for ev in result["events"]:
                            etype = ev.get("type")
                            if etype in ("hit", "aoe_hit", "step_hit", "slash_hit"):
                                if "mob" in ev:
                                    mob = self.mobs.get(ev["mob"])
                                    if mob:
                                        self.vfx.add_damage(mob["x"], mob["y"], ev["damage"])
                                        self.vfx.add_skill_flash(mob["x"], mob["y"], skill_name)
                                        self.vfx.add_shake(2)
                            elif etype == "heal":
                                player = self.players.get(ev.get("target"))
                                if player:
                                    self.vfx.add_heal(player["x"], player["y"], ev["amount"])
                    # Update mobs state from server
                    if "mobs" in data:
                        self.mobs = data["mobs"]
                elif t == "CHAT":
                    pid = data["id"]
                    name = self.players.get(pid, {}).get("class", f"Player-{pid}")
                    self.chat.add(name, data.get("text", ""))
                elif t == "LOGIN_FAIL":
                    print("[Client] Login failed:", data.get("reason"))
                    pygame.quit(); raise SystemExit
                elif t == "LEAVE":
                    self.players.pop(data["id"], None)
                elif t == "DIALOGUE":
                    # Start dialogue window
                    if "dialogue_id" in data and data["dialogue_id"] == "intro":
                        self.dialogue_ui.start_dialogue(data["npc_name"], START_DIALOGUE.lines)
                elif t == "QUEST_UPDATE":
                    if "quest" in data:
                        self.quest_ui.set_quest(data["quest"])
                elif t == "QUEST_COMPLETE":
                    if quest := self.quest_ui.quest:
                        self.quest_ui.complete_quest(data.get("xp", 0))
                        # Update player data if server sent new stats
                        if "p_data" in data:
                            self.players[self.my_id] = data["p_data"]
                elif t == "CORRECT_POSITION":
                    # Server correcting our position (anti-cheat)
                    if self.my_id in self.players:
                        self.players[self.my_id]["x"] = data["x"]
                        self.players[self.my_id]["y"] = data["y"]
        except Exception as e:
            print("[Client Receiver Error]", e)

    # -----------------------------------------------------------
    # Main game loop
    # -----------------------------------------------------------
    async def run(self):
        # Login UI
        login_ui = LoginUI(self.screen, self.font, self.ui_font)
        self.mode, self.username, self.password = login_ui.run()

        # If registering, pick a class before connecting
        if self.mode == "REGISTER":
            self.select_class_screen()

        if not await self.connect():
            return

        asyncio.create_task(self.receiver())

        while self.running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False

                elif ev.type == pygame.KEYDOWN:
                    # Chat typing mode
                    if self.chat.typing:
                        if ev.key == pygame.K_RETURN:
                            # Send chat message
                            txt = self.chat.current.strip()
                            if txt:
                                await self.ws.send(json.dumps({"type": "CHAT", "text": txt}))
                            self.chat.current = ""
                            self.chat.typing = False
                        elif ev.key == pygame.K_BACKSPACE:
                            self.chat.current = self.chat.current[:-1]
                        elif len(ev.unicode) == 1 and ev.unicode.isprintable():
                            self.chat.current += ev.unicode
                    else:
                        # Toggle chat input
                        if ev.key == pygame.K_RETURN:
                            self.chat.toggle()
                        # Combat input
                        elif ev.key == pygame.K_SPACE:
                            await self.ws.send(json.dumps({"type": "ATTACK"}))
                        elif ev.key == pygame.K_1:
                            # No skill name -> server auto-selects based on class
                            await self.ws.send(json.dumps({"type": "SKILL"}))
                        elif ev.key == pygame.K_e:
                            # Interact with nearby NPC
                            if not self.dialogue_ui.active:
                                await self.ws.send(json.dumps({"type": "TALK_NPC"}))
                        elif ev.key == pygame.K_SPACE and self.dialogue_ui.active:
                            # Advance dialogue
                            self.dialogue_ui.advance()

            # Movement
            if self.my_id and self.my_id in self.players:
                me = self.players[self.my_id]
                keys = pygame.key.get_pressed()
                dx = (keys[pygame.K_d] - keys[pygame.K_a]) * PLAYER_SPEED
                dy = (keys[pygame.K_s] - keys[pygame.K_w]) * PLAYER_SPEED
                if dx or dy:
                    me["x"] += dx
                    me["y"] += dy
                    await self.ws.send(json.dumps({
                        "type": "MOVE",
                        "x": int(me["x"]),
                        "y": int(me["y"])
                    }))

            # Update visual FX
            self.vfx.update()
            self.quest_ui.update()
            # Draw world with NPCs
            self.engine.draw_world(self.players.get(self.my_id), self.players, self.mobs, self.npcs)
            # Draw visual effects (behind UI)
            self.vfx.draw(self.screen, self.engine.cam_x, self.engine.cam_y)
            # Draw UIs
            if self.my_id in self.players:
                self.ui.draw_hud(self.players[self.my_id])
            self.chat.draw()
            self.quest_ui.draw()
            self.dialogue_ui.draw()

            pygame.display.flip()
            self.clock.tick(TICK_RATE)
            await asyncio.sleep(0)

        pygame.quit()
        print("[Client] Disconnected cleanly.")


def launch_client():
    game = GameClient()
    try:
        asyncio.run(game.run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    launch_client()