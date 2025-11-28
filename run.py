# ===============================================================
# Isekai Online - Unified Launcher (Server + Client in one loop)
# ===============================================================
import asyncio
import threading
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server.main import GameServer
from client.main import GameClient


async def start_all():
    # Start server inside an asyncio task instead of a thread
    server = GameServer()
    server_task = asyncio.create_task(server.run())

    # Give the server time to start listening
    await asyncio.sleep(1)

    # Launch the client afterwards
    client = GameClient()
    await client.run()

    # Stop server when client closes
    server_task.cancel()


def main():
    print("=======================================")
    print("  ISEKAI ONLINE - UNIFIED LAUNCH")
    print("=======================================")
    asyncio.run(start_all())


if __name__ == "__main__":
    main()