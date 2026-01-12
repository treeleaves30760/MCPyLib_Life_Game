# MCPyLib - Conway's Game of Life - Minecraft Edition

A Python implementation of Conway's Game of Life that runs inside Minecraft using MCPyLib. Watch cellular automata come to life with glowing blocks, oscillating patterns, and glider guns that continuously spawn new structures.

## Features

- **Real-time cellular automata** simulation rendered in Minecraft
- **8 classic patterns** including glider, pulsar, glider gun, acorn, and more
- **5 preset configurations** with different visual themes and grid sizes
- **Flexible orientation** - display on ground (horizontal) or as vertical walls
- **Loop mode** to continuously repeat simulations for mesmerizing displays
- **High-performance rendering** using MCPyLib's bulk edit operations
- **Interactive menu** for easy pattern selection
- **Automatic platform building** with glass borders for better viewing

## Prerequisites

- Python 3.12 or higher
- Minecraft server with [MCPyLib](https://github.com/sakertooth/mcpylib) plugin installed
- MCPyLib authentication token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/treeleaves30760/MCPyLib_Life_Game.git
cd MCPyLib_Life_Game
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install mcpylib python-dotenv
```

3. Configure the environment:
```bash
cp .env.example .env
```

Edit `.env` and add your MCPyLib server details:
```env
SERVER_IP=127.0.0.1
SERVER_PORT=65535
SERVER_TOKEN=your_token_here
PLAYER_NAME=your_minecraft_username
DELAY=0.15
```

**Configuration Options:**
- `SERVER_IP` - Minecraft server address (default: 127.0.0.1)
- `SERVER_PORT` - Server port (default: 65535)
- `SERVER_TOKEN` - MCPyLib authentication token (required)
- `PLAYER_NAME` - Your Minecraft username for position detection
- `DELAY` - Seconds between generations (default: 0.15, adjust for faster/slower animation)

## Usage

Run the program:
```bash
python main.py
```

You'll be presented with an interactive menu to select from 5 preset configurations. After selecting a preset, you'll be asked to choose:

1. **Display Orientation:**
   - **Horizontal (ground)** - Traditional view on the ground (X-Z plane)
   - **Vertical wall (X-Y)** - Standing display facing North/South
   - **Vertical wall (Z-Y)** - Standing display facing East/West

2. **Run Mode:**
   - **Single run** - The simulation runs for the specified number of generations and stops
   - **Loop mode** - The pattern resets and restarts after each cycle, creating an endless animation (press Ctrl+C to stop)

### Available Presets

1. **Classic Glider** - Small grid with a glider pattern moving diagonally
   - 30x30 grid, 150 generations
   - Glowstone alive cells, black concrete dead cells

2. **Pulsar Show** - Medium grid showcasing beautiful pulsar oscillations
   - 40x40 grid, 100 generations
   - Sea lantern alive cells, blue concrete dead cells

3. **Glider Gun Factory** - Large grid with glider gun continuously producing gliders
   - 60x60 grid, 300 generations
   - Redstone lamp alive cells, gray concrete dead cells

4. **Chaos Lab** - Medium grid with fast-evolving chaotic acorn pattern
   - 50x50 grid, 500 generations
   - Emerald block alive cells, black concrete dead cells

5. **Rainbow Oscillators** - Small grid displaying beacon oscillator patterns
   - 35x35 grid, 80 generations
   - Diamond block alive cells, purple concrete dead cells

## Supported Patterns

The implementation includes these classic Game of Life patterns:

- **glider** - Simple 5-cell pattern that moves diagonally across the grid
- **blinker** - Simplest oscillator with period 2
- **toad** - Period 2 oscillator
- **beacon** - Period 2 oscillator
- **pulsar** - Large period 3 oscillator
- **glider_gun** - Gosper's Glider Gun, produces gliders indefinitely
- **r_pentomino** - Methuselah pattern that evolves for 1,103 generations
- **diehard** - Pattern that disappears after 130 generations
- **acorn** - Small methuselah pattern that takes 5,206 generations to stabilize

## How It Works

The program:
1. Connects to your Minecraft server using MCPyLib
2. Gets your player position as the origin point
3. Builds a stone platform/backing and glass border based on chosen orientation:
   - Horizontal: flat platform on the ground with raised borders
   - Vertical: stone backing wall with glass frame around the edges
4. Loads the selected pattern at the center of the grid
5. Simulates Conway's Game of Life rules:
   - Any live cell with 2-3 neighbors survives
   - Any dead cell with exactly 3 neighbors becomes alive
   - All other cells die or stay dead
6. Renders each generation using bulk block placement for optimal performance
7. In loop mode, automatically resets and restarts the pattern after completion

## Troubleshooting

**Connection error:**
- Ensure your Minecraft server is running
- Verify MCPyLib plugin is installed and enabled
- Check that `SERVER_IP`, `SERVER_PORT`, and `SERVER_TOKEN` are correct in `.env`

**Cannot get player position:**
- Verify `PLAYER_NAME` matches your in-game username exactly
- The program will fall back to coordinates (100, 64, 100) if player position cannot be retrieved

**Slow rendering:**
- The program uses bulk edit operations for performance
- Reduce grid size or increase delay between generations if needed

## Project Structure

```
MCPyLib_Life_Game/
├── main.py           # Main implementation with GameOfLife class and presets
├── pyproject.toml    # Project dependencies
├── .env.example      # Example environment configuration
├── .env              # Your actual configuration (not committed)
└── README.md         # This file
```

## Dependencies

- [MCPyLib](https://github.com/sakertooth/mcpylib) - Minecraft Python library for server interaction
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment variable management

## License

MIT License - feel free to use and modify this project.

## Acknowledgments

- Based on [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- Built with [MCPyLib](https://github.com/sakertooth/mcpylib)
