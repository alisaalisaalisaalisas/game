# Project Documentation: 2D Platformer Game

## Table of Contents
1. [Overview](#overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Core Systems](#core-systems)
5. [Game Architecture](#game-architecture)
6. [Player System](#player-system)
7. [Level System](#level-system)
8. [Enemy System](#enemy-system)
9. [Collision System](#collision-system)
10. [UI System](#ui-system)
11. [Audio System](#audio-system)
12. [Asset Management](#asset-management)
13. [Configuration System](#configuration-system)
14. [Testing](#testing)
15. [Building and Distribution](#building-and-distribution)

---

## Overview

This is a 2D platformer game with RPG elements built in Python using Pygame. The game features:
- Smooth player controls with advanced physics (coyote time, jump buffering)
- Combat system where players defeat enemies by jumping on them
- TMX-based level loading with multiple tile layers
- Enemy AI with patrol behavior and state machines
- Health system with visual hearts display
- Collectible items (coins, keys, jewels)
- Environmental hazards (spikes, moving saws)
- Full audio system with music and sound effects

**Language**: Russian (UI and comments), but code identifiers are in English.

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.8+ |
| Game Framework | Pygame 2.6.1 |
| Level Format | TMX (Tiled Map Editor) |
| TMX Parsing | PyTMX 3.32 |
| Testing | unittest, pytest |
| Build Tool | PyInstaller |

---

## Project Structure

```
game/
├── main.py                 # Entry point - RPGPlatformer class
├── config.json             # Game configuration file
├── build_game.bat          # Windows build script
├── run_tests.py            # Test runner script
├── requirements.txt        # Python dependencies
│
├── game/                   # Core game logic
│   ├── player.py           # Player class with physics and combat
│   ├── camera.py           # Smooth camera following system
│   ├── platform.py         # Platform class with collision detection
│   ├── asset_loader.py     # Centralized asset management
│   ├── config.py           # Configuration dataclasses
│   ├── path_utils.py       # PyInstaller-compatible paths
│   ├── health.py           # Health component (shared)
│   ├── decorations.py      # Decorative elements and doors
│   │
│   ├── levels/
│   │   └── level1.py       # First level with TMX data
│   │
│   ├── enemies/
│   │   ├── slime.py        # Slime enemy with 4 animation states
│   │   ├── snail.py        # Snail enemy
│   │   └── fly.py          # Flying enemy with vertical patrol
│   │
│   ├── items/
│   │   └── items.py        # Collectible items (coins, keys, jewels)
│   │
│   ├── traps/
│   │   ├── spikes.py       # Static spike hazard
│   │   └── saw.py          # Moving rotating saw
│   │
│   └── assets/             # Game resources
│       ├── audio/          # Sound effects and music
│       ├── backgrounds/    # Background images
│       ├── player/         # Player sprites
│       ├── enemies/        # Enemy sprites
│       ├── Hud/            # UI elements
│       ├── items/          # Item sprites
│       ├── levels/         # TMX level files
│       └── Spritesheets/   # Tilesets for TMX
│
├── ui/                     # User interface
│   ├── menu.py             # Main menu with mouse/keyboard support
│   ├── hud.py              # In-game HUD (hearts, coins, keys)
│   └── credits.py          # Credits screen
│
└── tests/                  # Test suite
    ├── test_units.py       # Unit tests
    ├── test_integration.py # Integration tests
    ├── test_player.py      # Player-specific tests
    └── ...                 # Other test files
```

---

## Core Systems

### Game Loop (main.py)

The `RPGPlatformer` class manages the entire game:

```python
class RPGPlatformer:
    def __init__(self):
        # Initialize pygame, screen, clock
        # Load configuration from config.json
        # Initialize audio, menu, credits systems
        
    def run(self):
        while self.running:
            self.handle_events()  # Process input
            self.update()         # Update game state
            self.draw()           # Render frame
            self.clock.tick(60)   # Cap at 60 FPS
```

### State Machine

The game uses a simple state machine with three states:
- `menu` - Main menu displayed
- `game` - Active gameplay
- `credits` - Credits screen

State transitions are managed by methods like `start_game()`, `go_to_menu()`, `go_to_credits()`.

---

## Game Architecture

### Component-Based Design

The game uses a component-based architecture where entities have separate components:

1. **HealthComponent** - Manages health, damage, death
2. **Animation System** - State-based sprite switching
3. **Physics System** - Gravity, velocity, collision response

### Sprite Groups

Pygame sprite groups organize game objects for efficient updates and rendering:
- `platforms` - All solid platforms
- `enemies` - All enemy entities
- `items` - Collectible items
- `traps` - Hazards
- `decorations` - Visual-only elements

---

## Player System

### Player Class (game/player.py)

The player has sophisticated physics and combat mechanics:

#### Physics Properties
```python
self.speed = 5              # Horizontal movement speed
self.jump_power = -23       # Initial jump velocity
self.gravity = 0.8          # Gravity acceleration
self.coyote_time = 0.15     # Grace period after leaving platform
self.jump_buffer_time = 0.1 # Pre-jump input buffer
```

#### Hitbox System

The player has two rectangles:
- `rect` - Visual bounding box (80x100 pixels)
- `hitbox` - Collision box (60x90 pixels, offset 10,10)

```python
def get_actual_hitbox(self):
    """Returns world-space collision rectangle"""
    return pygame.Rect(
        self.rect.x + self.hitbox.x,
        self.rect.y + self.hitbox.y,
        self.hitbox.width,
        self.hitbox.height,
    )
```

#### State Machine

Player states: `idle`, `run`, `jump`, `land`

Animation updates based on current state in `update_animation()`.

#### Combat System

- **Stomping enemies**: When falling onto enemy's top, enemy takes damage
- **Taking damage**: Triggers invincibility frames and knockback
- **Death**: 2-second respawn timer, then teleport to spawn point

#### Health Component

```python
class HealthComponent:
    def __init__(self, max_health):  # Default: 60 HP (3 hearts × 20 HP)
        self.max_health = max_health
        self.current_health = max_health
    
    def take_damage(self, damage)  # Returns True if damage was applied
    def heal(self, amount)
    def is_dead()
```

---

## Level System

### Level Class (game/levels/level1.py)

Levels are loaded from base64+zlib encoded TMX data (embedded in Python files).

#### TMX Layers

Each level has multiple tile layers:
1. **ground** - Main solid platforms
2. **semiground** - Half-height platforms
3. **triangleleft** - Slope/ramp tiles
4. **traps** - Spike positions
5. **decoration** - Visual-only elements

#### Data Decoding

```python
def decode_layer_data(self, encoded_data):
    """Decode base64+zlib TMX layer data to tile GIDs"""
    decoded = base64.b64decode(encoded_data)
    decompressed = zlib.decompress(decoded)
    
    tile_data = []
    for i in range(0, len(decompressed), 4):
        tile_gid = int.from_bytes(decompressed[i:i+4], byteorder="little")
        tile_data.append(tile_gid)
    return tile_data
```

#### Tileset Mapping

Each tileset has a `firstgid` (first GID). Platform types are determined by GID:
```python
type_to_gid = {
    "grass1": 1,
    "grass_half": 2,
    "triangle": 25,
    "semitype1": 57,
    "box": 341,
    # ...
}
```

#### Level Callbacks

The level provides callbacks for game events:
- `on_level_complete` - Called when player reaches exit with key
- `on_respawn` (via player) - Called when player respawns (respawns enemies)
- `on_box_hit` (via player) - Called when player hits a breakable box from below

---

## Enemy System

### Base Enemy Pattern

All enemies inherit from `pygame.sprite.Sprite` and implement:
- `update(dt, level)` - Update logic per frame
- `draw(screen, camera)` - Render with camera offset
- `take_damage(amount)` - Handle damage with state changes

### Slime Enemy (game/enemies/slime.py)

Most complex enemy with full state machine:

#### States
- `idle` - Standing still
- `move` - Patrolling horizontally
- `hurt` - Damage received (0.5s animation)
- `dead` - Death animation (1.0s before removal)

#### Patrol System
```python
self.patrol_left = x - 200   # Left boundary
self.patrol_right = x + 200  # Right boundary
```

#### Invincibility System
After taking damage, 1 second of invincibility prevents damage stacking.

#### Delayed Death
When health reaches 0, the enemy first plays hurt animation, then transitions to dead state.

### Fly Enemy (game/enemies/fly.py)

Flying enemy with vertical patrol instead of horizontal.

### Snail Enemy (game/enemies/snail.py)

Slower ground enemy with higher durability.

---

## Collision System

### Platform Collision (game/platform.py)

Platforms have different collision behaviors based on type:

#### Standard Collision
```python
def check_collision(self, other_rect):
    if self.platform_type == "triangle":
        return self._check_triangle_collision(other_rect)
    return self.collision_rect.colliderect(other_rect)
```

#### Semiground Platforms
Half-height collision (only top half is solid):
```python
if self.platform_type.startswith("semitype"):
    return pygame.Rect(
        self.rect.x, self.rect.y,
        self.rect.width,
        self.rect.height // 2  # Only top half
    )
```

#### Triangle/Slope Collision
Slopes use mathematical surface calculation:
```python
def _check_triangle_collision(self, other_rect):
    # Calculate where player's X position intersects slope
    relative_x = (point_x - triangle_left) / triangle_width
    slope_height = relative_x * triangle_height
    surface_y = triangle_bottom - slope_height
    
    # Check if player's bottom is at or below surface
    if bottom >= surface_y - tolerance:
        return True
```

### Player Collision Handling

Player handles collisions in two phases:
1. **Horizontal** - `handle_horizontal_collisions()` - Wall collisions, step-up logic
2. **Vertical** - `handle_vertical_collisions()` - Ground landing, ceiling hits

---

## UI System

### Main Menu (ui/menu.py)

Features:
- Keyboard navigation (Up/Down arrows, Enter)
- Mouse click and hover support
- Dynamic options based on game state (shows "Continue" if game is active)
- Settings submenu for audio controls
- Level completion screen mode

#### Menu States
```python
# Standard menu options
["Новая игра", "Настройки", "Разработчики", "Выход"]

# With active game
["Продолжить игру", "Новая игра", "Настройки", "Разработчики", "Выход"]

# Level completed mode
["В МЕНЮ", "ВЫБОР УРОВНЯ", "СЛЕДУЮЩИЙ УРОВЕНЬ"]
```

### HUD (ui/hud.py)

Displays during gameplay:
- **Hearts** - 3 hearts representing 60 HP (20 HP each)
- **Coins** - Counter with icon
- **Keys** - Counter with icon
- **Death screen** - Pulsating overlay when player dies

### Credits (ui/credits.py)

Simple scrolling credits screen with developer information.

---

## Audio System

### AudioManager (game/assets/audio/)

Singleton pattern for global audio access:
```python
audio = AudioManager.get_instance(base_path="game/assets/audio")
```

#### Volume Controls
- `master_volume` - Overall volume multiplier
- `music_volume` - Background music volume
- `sfx_volume` - Sound effects volume
- `muted` - Global mute flag

#### Methods
```python
audio.on_menu_enter()           # Play menu music
audio.on_game_start("level1")   # Play level music
audio.sfx.play("player_jump")   # Play sound effect
audio.toggle_mute()             # Toggle mute
audio.set_master_volume(0.8)    # Set volume (0.0-1.0)
```

#### Sound Effects Keys
- `player_jump` - Jump sound
- `player_take_damage` - Damage received
- `player_death` - Death sound
- `player_collect_coin` - Item pickup
- `ui_menu_move` - Menu navigation
- `ui_button_click` - Menu selection

---

## Asset Management

### AssetLoader (game/asset_loader.py)

Centralized asset loading with caching:

```python
# Singleton instance
asset_loader = AssetLoader()

# Load single image with optional scale
sprite = asset_loader.load_image("player/alienPink_front.png", 0.6)

# Load tileset for TMX
asset_loader.load_tileset("Spritesheets/spritesheet_ground.png", 1, 128, 128)

# Get specific tile by GID
tile = asset_loader.get_tile_image(25)  # Triangle tile
```

#### Tileset System

Tilesets are loaded from spritesheets with metadata:
- `firstgid` - First GID in this tileset
- `tilewidth`, `tileheight` - Tile dimensions (128x128)
- `columns`, `rows` - Grid dimensions

### Path Utilities (game/path_utils.py)

PyInstaller-compatible path resolution:
```python
def resource_path(*args):
    """Returns correct path whether running as script or frozen exe"""
    # Returns path relative to bundle or script directory
```

---

## Configuration System

### config.json Structure

```json
{
    "video": {
        "width": 1400,
        "height": 800,
        "fullscreen": false
    },
    "audio": {
        "master": 1.0,
        "music": 1.0,
        "sfx": 1.0
    },
    "input": {
        "jump": "SPACE",
        "left": ["LEFT", "A"],
        "right": ["RIGHT", "D"],
        "escape_to_menu": "ESCAPE"
    },
    "ui": {
        "debug_overlay": false,
        "animations": false,
        "language": "ru"
    }
}
```

### Configuration Dataclasses (game/config.py)

```python
@dataclass
class GameConfig:
    video: VideoConfig
    audio: AudioConfig
    input: InputConfig
    ui: UIConfig

def load_config() -> GameConfig:
    """Load config from file or return defaults"""
```

---

## Testing

### Test Runner (run_tests.py)

Custom test runner that loads specific test modules:
```python
test_files = [
    'test_imports',
    'test_units',
    'test_integration',
    'test_enemy_respawn'
]
```

### Running Tests

```bash
# All tests via custom runner
python run_tests.py

# Via pytest
pytest tests/ -v

# Single test file
pytest tests/test_player.py -v

# Single test method
pytest tests/test_units.py::TestPlayer::test_player_jump -v
```

### Mock System

Tests use mock asset loader to avoid loading actual images:
```python
class MockAssetLoader:
    def load_image(self, name, scale=1):
        return MockImage()

# Replace in tests
game.player.asset_loader = MockAssetLoader()
```

### CI Configuration (.github/workflows/test.yml)

GitHub Actions runs tests on push/PR to main:
- Python 3.9 on Ubuntu
- Excludes visual tests that require display

---

## Building and Distribution

### PyInstaller Build

#### Windows Batch Script (build_game.bat)
```batch
pyinstaller game_build.spec
```

#### Output
- Executable: `dist/main/main.exe`
- All assets bundled in `dist/main/` folder
- Can be distributed as standalone folder

### Build Configuration (game_build.spec)

Key settings:
- One-folder mode (all files in single directory)
- Includes all assets from `game/assets/`
- PyInstaller-compatible path resolution via `resource_path()`

---

## Key Implementation Details

### Delta Time

All physics and animations use delta time for frame-rate independence:
```python
dt = self.clock.get_time() / 1000.0  # Delta time in seconds
dt = min(dt, 0.1)  # Cap to prevent tunneling on lag spikes
```

### Camera System (game/camera.py)

Smooth following with lerp:
```python
def update(self):
    # Lerp factor of 0.05 for smooth following
    self.offset_float.x += (target_x - self.offset_float.x) * 0.05
    self.offset_float.y += (target_y - self.offset_float.y) * 0.05
```

### Spawn/Respawn System

1. Player spawns at `player_spawn_point` defined in level
2. On death, player waits `respawn_duration` (2 seconds)
3. On respawn, player gets 3 seconds invincibility
4. Level's `respawn_killed_enemies()` is called to restore enemies

### Level Completion

1. Player collects yellow key (`has_yellow_key = True`)
2. Player touches yellow lock decoration
3. `on_level_complete` callback triggers
4. Menu switches to level completion mode

---

## Common Patterns

### Creating New Enemy

1. Create file in `game/enemies/`
2. Inherit from `pygame.sprite.Sprite`
3. Implement required methods:
   - `__init__(self, x, y)`
   - `update(self, dt, level)`
   - `draw(self, screen, camera)`
   - `take_damage(self, amount)`
4. Add sprite loading with fallback to placeholder
5. Add to level's enemy spawn data

### Creating New Item

1. Add item type to `game/items/items.py`
2. Add sprite path to item type mapping
3. Handle collection in `Level.check_item_collection()`
4. Add HUD display if needed

### Creating New Level

1. Create TMX file in Tiled Map Editor
2. Export layer data as base64+zlib
3. Create new level class in `game/levels/`
4. Define tilesets, layers, and object spawns
5. Update main.py to load new level
