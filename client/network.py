# ===============================================================
# Isekai Online - Client Networking
# ===============================================================
# Handles all websocket communication between the client and server.

import asyncio
import json
import websockets
from Isekai_Online.config import HOST, PORT


class GameNetwork:
    """Simplified WebSocket manager for the client."""

    def __init__(self):
        self.ws = None
        self.connected = False

    # -----------------------------------------------------------
    # CONNECTION
    # -----------------------------------------------------------
    async def connect(self, player_class="warrior"):
        """Connect to the server and send init message."""
        for attempt in range(5):
            try:
                print(f"[Network] Connecting to {HOST}:{PORT} (Attempt {attempt + 1})...")
                self.ws = await websockets.connect(f"ws://{HOST}:{PORT}")
                await self.ws.send(json.dumps({"type": "INIT", "class": player_class}))
                self.connected = True
                print("[Network] Connected!")
                return True
            except Exception as e:
                print(f"[Network] Failed to connect: {e}")
                await asyncio.sleep(2)
        return False

    # -----------------------------------------------------------
    # OUTGOING
    # -----------------------------------------------------------
    async def send(self, payload: dict):
        """Send a message to the server."""
        if not self.ws or not self.connected:
            return
        try:
            await self.ws.send(json.dumps(payload))
        except Exception as e:
            print(f"[Network] Send error: {e}")
            self.connected = False

    # -----------------------------------------------------------
    # INCOMING
    # -----------------------------------------------------------
    async def listen(self, handler):
        """
        Listen for messages and forward to a provided handler.
        The handler should be an async method from the main game (receiver logic).
        """
        if not self.ws:
            print("[Network] No active websocket.")
            return

        try:
            async for message in self.ws:
                data = json.loads(message)
                await handler(data)
        except Exception as e:
            print(f"[Network] Disconnected: {e}")
            self.connected = False

    # -----------------------------------------------------------
    # UTILITIES
    # -----------------------------------------------------------
    async def close(self):
        """Close connection cleanly."""
        if self.ws:
            try:
                await self.ws.close()
            except Exception:
                pass
        self.connected = False
        print("[Network] Connection closed.")