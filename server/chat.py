import json

class ChatManager:
    def __init__(self, server):
        self.server = server

    async def handle(self, pid, text):
        packet = {"type": "CHAT", "id": pid, "text": text}
        await self.server.broadcast(json.dumps(packet))