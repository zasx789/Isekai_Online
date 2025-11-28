import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing imports from Isekai_Online.config...")
    from Isekai_Online.config import HOST, PORT
    print(f"HOST={HOST}, PORT={PORT}")
    
    print("\nTesting imports from server.player...")
    from server.player import PlayerManager
    print("Successfully imported PlayerManager")
    
    print("\nTesting imports from shared.biome...")
    from shared.biome import get_biome
    print("Successfully imported get_biome")
    
    print("\nAll imports successful!")
except Exception as e:
    print(f"Import error: {e}")
    import traceback
    traceback.print_exc()