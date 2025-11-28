# Minimal server launcher that avoids import issues
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_server():
    print("=== Initializing Server ===")
    
    # Load configuration directly
    from config import HOST, PORT
    
    print(f"Starting server at {HOST}:{PORT}")
    
    try:
        import asyncio
        import json
        import websockets
        
        # Simple echo server to test network connectivity
        async def echo(websocket, path):
            async for message in websocket:
                print(f"Received: {message}")
                await websocket.send(message)
        
        print("[Server] Starting test server...")
        
        async def main():
            async with websockets.serve(echo, HOST, PORT):
                print("[Server] Test server started successfully!")
                await asyncio.Future()  # run forever
        
        asyncio.run(main())
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_server()