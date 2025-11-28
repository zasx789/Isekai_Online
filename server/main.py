# ===============================================================
# Isekai Online - Server Main (LOGIN/REGISTER + Combat + Chat)
# ===============================================================

import asyncio
import json
import threading
import websockets

import sys
import os
# Add project root to path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Import modules directly
import config as cfg
from server.player import PlayerManager
from server.enemies import EnemyManager
from server.combat_enhanced import EnhancedCombatSystem
from server.database import Database
from server.quest_enhanced import QuestState
from server.npc import NPCManager
# Shared story system
from shared.story_enhanced import DIALOGUE_REGISTRY

# Constants from config
HOST = cfg.HOST
PORT = cfg.PORT
MAX_MOVE_DISTANCE = cfg.MAX_MOVE_DISTANCE
MOVEMENT_VALIDATION_TOLERANCE = cfg.MOVEMENT_VALIDATION_TOLERANCE


# Shared database for accounts
db = Database()


class GameServer:
    """Main asynchronous WebSocket game server."""

    def __init__(self):
        self.clients = {}                 # websocket -> player_id
        self.player_manager = PlayerManager()
        self.enemy_manager = EnemyManager()
        self.enemy_manager.spawn_initial_enemies()
        self.combat = EnhancedCombatSystem(self.player_manager, self.enemy_manager)
        self.quest_state = QuestState()
        self.npc_manager = NPCManager()

    # -----------------------------------------------------------
    async def handler(self, websocket):
        pid = None
        try:
            # First packet decides the session flow
            raw = await websocket.recv()
            data = json.loads(raw)
            cmd = data.get("type", "INIT")

            player = None
            # -------- REGISTER flow --------
            if cmd == "REGISTER":
                username = data.get("username")
                password = data.get("password")
                class_name = data.get("class", "warrior")

                if not username or not password:
                    await websocket.send(json.dumps({"type": "LOGIN_FAIL", "reason": "Missing credentials"}))
                    return

                if db.account_exists(username):
                    await websocket.send(json.dumps({"type": "LOGIN_FAIL", "reason": "User exists"}))
                    return

                player = self.player_manager.create_player(class_name)
                pid = player.id
                db.create_account(username, password, pid)

            # -------- LOGIN flow --------
            elif cmd == "LOGIN":
                username = data.get("username")
                password = data.get("password")
                pid_from_db = db.verify_login(username, password)
                if not pid_from_db:
                    await websocket.send(json.dumps({"type": "LOGIN_FAIL", "reason": "Invalid credentials"}))
                    return

                player = self.player_manager.create_player("warrior", existing_id=pid_from_db)
                pid = player.id

            # -------- Legacy INIT (no accounts) --------
            else:  # "INIT"
                class_name = data.get("class", "warrior")
                player = self.player_manager.create_player(class_name)
                pid = player.id

            # Register client socket
            self.clients[websocket] = pid
            print(f"[JOIN] Player {pid} connected.")

            # Send world snapshot
            # Give first quest to new players
            quest = self.quest_state.give_first_quest(pid)
            await websocket.send(json.dumps({
                "type": "INIT",
                "id": pid,
                "state": self.player_manager.get_state(),
                "enemies": self.enemy_manager.get_state(),
                "npcs": self.npc_manager.get_state(),
                "quest": quest
            }))

            # Notify others
            await self.broadcast(json.dumps({
                "type": "JOIN",
                "id": pid,
                "data": player.serialize()
            }), exclude=websocket)

            # ---------------- Main loop ----------------
            async for message in websocket:
                msg = json.loads(message)
                mtype = msg.get("type", "")

                # Movement
                if mtype == "MOVE":
                    p = self.player_manager.players.get(pid)
                    if not p:
                        continue
                    new_x, new_y = msg["x"], msg["y"]
                    
                    # Basic movement validation (prevent teleporting)
                    dist = ((new_x - p.x) ** 2 + (new_y - p.y) ** 2) ** 0.5
                    if dist > MAX_MOVE_DISTANCE:
                        # Possible cheating or lag, send the current valid position back
                        await websocket.send(json.dumps({
                            "type": "CORRECT_POSITION",
                            "x": p.x,
                            "y": p.y
                        }))
                        continue
                    
                    # Update position with slight tolerance for network jitter
                    p.x, p.y = new_x, new_y
                    await self.broadcast(json.dumps({
                        "type": "UPDATE", "id": pid, "x": p.x, "y": p.y
                    }), exclude=websocket)

                # Basic attack
                elif mtype == "ATTACK":
                    p = self.player_manager.players.get(pid)
                    if not p:
                        continue
                    result = self.combat.player_attack(pid)
                    # Handle quest progress if slime was killed
                    if result.get("notify_type") == "SLIME_KILL":
                        q = self.quest_state.increment(pid, "slime")
                        if q:
                            await websocket.send(json.dumps({"type": "QUEST_UPDATE", "quest": q}))
                            if self.quest_state.check_complete(pid):
                                # award XP
                                if p:
                                    p.add_xp(q["reward_xp"])
                                    await websocket.send(json.dumps({"type": "QUEST_COMPLETE", "xp": q["reward_xp"], "p_data": p.serialize()}))
                    
                    await self.broadcast(json.dumps({
                        "type": "COMBAT",
                        "attacker": pid,
                        "mobs": self.mob_manager.get_state(),
                        "p_data": p.serialize(),
                        "result": result
                    }))

                # Skills (auto by class if 'skill' missing)
                elif mtype == "SKILL":
                    from .skills import SkillManager
                    sm = SkillManager(self.player_manager, self.mob_manager)
                    skill_name = msg.get("skill")  # can be None -> auto by class
                    result = sm.use_skill(pid, skill_name)
                    await self.broadcast(json.dumps({
                        "type": "SKILL_FX",
                        "attacker": pid,
                        "skill": result.get("skill", skill_name),
                        "result": result,
                        "mobs": self.mob_manager.get_state(),
                        "players": self.player_manager.get_state()
                    }))

                # Chat
                elif mtype == "CHAT":
                    text = msg.get("text", "")
                    packet = {"type": "CHAT", "id": pid, "text": text}
                    await self.broadcast(json.dumps(packet))
                
                
                # Dialogue requests when player is near NPC
                elif mtype == "TALK_NPC":
                    player = self.player_manager.players.get(pid)
                    if player:
                        npc_id, npc_data = self.npc_manager.nearby(player.x, player.y)
                        if npc_id:
                            # For simplicity send the entire dialogue block for now
                            await websocket.send(json.dumps({
                                "type": "DIALOGUE",
                                "npc_id": npc_id,
                                "npc_name": npc_data["name"],
                                "dialogue_id": npc_data.get("dialogue")
                            }))

        except websockets.exceptions.ConnectionClosed as e:
            print(f"[Server] Client disconnected gracefully: {e}")
        except json.JSONDecodeError as e:
            print(f"[Server] Invalid JSON from client: {e}")
        except Exception as e:
            print(f"[Server Error in handler] Unexpected error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup on disconnect
            if pid:
                print(f"[LEAVE] Player {pid} disconnected.")
                self.player_manager.remove_player(pid)
            if websocket in self.clients:
                del self.clients[websocket]
            await self.broadcast(json.dumps({"type": "LEAVE", "id": pid}))

    # -----------------------------------------------------------
    async def broadcast(self, msg, exclude=None):
        """Send a JSON string to all connected clients."""
        if not self.clients:
            return
        tasks = []
        for ws in list(self.clients.keys()):
            if ws != exclude:
                tasks.append(asyncio.create_task(ws.send(msg)))
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    # -----------------------------------------------------------
    async def run(self):
        print(f"[Server] Starting on ws://{HOST}:{PORT}")
        async with websockets.serve(self.handler, HOST, PORT):
            await asyncio.Future()  # run forever


# -----------------------------------------------------------
# Background thread launcher (used by run.py)
# -----------------------------------------------------------
def start_server_thread():
    """Start the server in a background thread."""
    def run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = GameServer()
        try:
            loop.run_until_complete(server.run())
        except KeyboardInterrupt:
            print("[Server] Shutting down...")
        finally:
            loop.close()

    t = threading.Thread(target=run, daemon=True)
    t.start()
    print(f"[Server] Background server thread started on {HOST}:{PORT}")


# -----------------------------------------------------------
# Direct launch
# -----------------------------------------------------------
if __name__ == "__main__":
    try:
        asyncio.run(GameServer().run())
    except KeyboardInterrupt:
        print("[Server] Stopped by user.")