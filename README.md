# ⚔️ Isekai Online - MMORPG

**A 2D Multiplayer Online RPG with Isekai Story, Quests, and Real-Time Combat!**

## 🎮 Quick Start

```bash
cd Isekai_Online
python run.py
```


Or create a new account using the same credentials.

## 📖 Story

You wake up in a strange world called Isekai. Everything is unfamiliar. The only way home lies through proving your strength and gaining the trust of the local Guild. Your first task: defeat the slimes that plague the lands outside Haven City.

## 🎯 Features Implemented

### ✨ Core Gameplay
- 🗺️ **Procedural World Generation** - Infinite terrain with grass, water, sand, and trees
- ⚔️ **Real-Time Combat** - Attack enemies instantly with visual feedback
- 📊 **Level System** - Gain XP and level up to become stronger
- 👥 **Multiplayer** - Fight alongside other players in the same world
- 💬 **Chat System** - Press ENTER to chat with other players

### 🎭 Story & Quests
- 📜 **Isekai Story** - Transported to another world seeking a way home
- 🎯 **Quest System** - "Way Back Home - First Steps" main quest line
- 🤝 **NPCs** - Talk to Guild Master in Haven City (Press E)
- 📝 **Dialogue System** - Full story narratives from NPCs
- 🏆 **Quest Rewards** - XP and progression based on objectives

### ⚡ Classes & Skills
Each class has unique abilities:
- **Warrior**: PowerStrike - Heavy single-target damage
- **Mage**: Fireball - Area of Effect burst damage
- **Rogue**: ShadowStep - Teleport and strike combo

Press **1** to use your class skill!

### 🎨 Visual Effects
- 💥 **Damage Numbers** - Floating text showing damage/healing
  - Red: Normal Damage
  - Yellow: Critical Hits
  - Green: Healing
- ✨ **Skill Effects** - Colored visual flares for each skill
- 📺 **Screen Shake** - Impact feedback on powerful attacks
- 🎬 **Combat Animation** - Smooth character and enemy movements

### 🔐 Security Features
- 🔒 **Bcrypt Password Hashing** - Secure password storage
- ✅ **Anti-Cheat Movement Validation** - Prevents teleporting
- 🛡️ **Database Protection** - Thread-safe database access

## ⌨️ Controls

| Key | Action |
|-----|--------|
| **W/A/S/D** | Move character |
| **SPACE** | Basic Attack |
| **1** | Use Class Skill |
| **E** | Talk to NPC (when nearby) |
| **ENTER** | Toggle Chat Mode / Advance Dialogue |
| **SPACE** (in chat) | Skip chat, then SPACE again to advance dialogue |
| **Esc** | Exit (from login screen) |

## 🎮 Gameplay Loop

1. **Login/Create Account** - Enter your credentials
2. **Choose Class** - Select Warrior, Mage, or Rogue
3. **Explore City** - Find the Guild Master (golden name)
4. **Talk to NPC** - Press E to hear the story
5. **Get Quest** - First quest: Defeat 3 slimes
6. **Leave City** - Go outside the city walls
7. **Fight Slimes** - Use SPACE for attacks, 1 for skills
8. **Complete Quest** - Watch progress in top-right corner
9. **Level Up** - Gain XP and become stronger
10. **Continue Adventure** - More content coming!

## 📊 Quest Progress

- **Active Quest Tracker** - Top-right corner shows current quest
- **Progress Counter** - Kills / Objective updates in real-time
- **Quest Completion** - Bottom-center notification when quest is complete
- **XP Rewards** - Instant XP gain for quest completion

## 🌍 World Exploration

- **Haven City** - Safe zone with NPCs (city center area)
- **Grasslands** - Main exploration area with trees and slimes
- **Sand Dunes** - Desert biome (structure in place)
- **Water Areas** - Hazardous zones (can't swim)

## 🐛 Known Limitations

- Current version focuses on single quest line
- NPCs are limited to Guild Master (expandable architecture)
- Item system not yet implemented
- No player housing yet

## 🔮 Planned Features

- [ ] Item & Inventory System
- [ ] More Quests & Story Content
- [ ] Additional NPCs & Vendors
- [ ] Dungeons & Bosses
- [ ] Guild System
- [ ] PVP Arenas
- [ ] Trading System
- [ ] Housing System
- [ ] Day/Night Cycle
- [ ] Advanced Graphics

## 💾 Save System

- **Account-Based** - Your progress is saved to the server database
- **Auto-Save** - Happens automatically during gameplay
- **Cross-Session** - Log back in to continue where you left off

## 🛠️ Technical Details

- **Backend**: Python with WebSockets (asyncio)
- **Frontend**: Pygame for graphics
- **Database**: SQLite with bcrypt password hashing
- **Architecture**: Client-Server multiplayer
- **Performance**: 60 FPS target, optimized for most machines

## 📝 Test Checklist

- ✅ Login system working
- ✅ Account creation working
- ✅ Password hashing secure (bcrypt)
- ✅ Quest system functional
- ✅ NPC dialogue system working
- ✅ Combat visual effects displaying
- ✅ Damage numbers showing
- ✅ Skill effects rendering
- ✅ Screen shake on attacks
- ✅ Quest progress tracking
- ✅ XP rewards awarding
- ✅ Level progression working

## 🎓 Learning Points

This project demonstrates:
- Asynchronous networking with websockets
- Real-time multiplayer game architecture
- Procedural content generation
- Game state management
- Visual effects systems
- Quest and progression systems
- Security best practices (password hashing, input validation)

## 🚀 Getting Started with Development

### Prerequisites
```bash
pip install pygame websockets bcrypt
```

### Running the Game
```bash
python run.py
```

### Running Components Separately
```bash
# Server only
cd server
python main.py

# Client only (connects to existing server)
cd client
python main.py
```

## 📞 Support

For bugs or issues, check the console output for error messages. The game logs all important events.

---


**Enjoy your adventure in Isekai Online! The journey back home awaits! ⚔️✨**
