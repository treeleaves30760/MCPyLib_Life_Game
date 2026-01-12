"""
Conway's Game of Life in Minecraft
Simulates cellular automata using blocks in Minecraft
"""
from mcpylib import MCPyLib
from dotenv import load_dotenv
import os
import time


class GameOfLife:
    def __init__(self, mc: MCPyLib, origin_x: int, origin_y: int, origin_z: int,
                 width: int, height: int):
        """
        Initialize Game of Life

        Args:
            mc: MCPyLib instance
            origin_x, origin_y, origin_z: Starting coordinates for the grid
            width: Grid width (x-axis)
            height: Grid height (z-axis)
        """
        self.mc = mc
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.origin_z = origin_z
        self.width = width
        self.height = height

        # Blocks for alive and dead cells
        self.alive_block = "minecraft:glowstone"
        self.dead_block = "minecraft:black_concrete"

        # Initialize grid (0 = dead, 1 = alive)
        self.grid = [[0 for _ in range(height)] for _ in range(width)]

    def clear_grid(self):
        """Clear the entire grid"""
        self.grid = [[0 for _ in range(self.height)]
                     for _ in range(self.width)]
        self.render()

    def set_cell(self, x: int, z: int, alive: bool):
        """Set a cell to alive or dead"""
        if 0 <= x < self.width and 0 <= z < self.height:
            self.grid[x][z] = 1 if alive else 0

    def get_cell(self, x: int, z: int) -> int:
        """Get cell state (with bounds checking)"""
        if 0 <= x < self.width and 0 <= z < self.height:
            return self.grid[x][z]
        return 0

    def count_neighbors(self, x: int, z: int) -> int:
        """Count alive neighbors for a cell"""
        count = 0
        for dx in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                if dx == 0 and dz == 0:
                    continue
                count += self.get_cell(x + dx, z + dz)
        return count

    def next_generation(self):
        """Calculate and apply the next generation"""
        new_grid = [[0 for _ in range(self.height)] for _ in range(self.width)]

        # Apply Conway's rules
        for x in range(self.width):
            for z in range(self.height):
                neighbors = self.count_neighbors(x, z)
                cell = self.grid[x][z]

                if cell == 1:  # Alive cell
                    # Survival: 2 or 3 neighbors
                    if neighbors in [2, 3]:
                        new_grid[x][z] = 1
                    else:
                        new_grid[x][z] = 0  # Dies
                else:  # Dead cell
                    # Birth: exactly 3 neighbors
                    if neighbors == 3:
                        new_grid[x][z] = 1

        self.grid = new_grid

    def render(self):
        """Render the current grid state in Minecraft using bulk edit"""
        # Build 3D block array for edit() - [x][y][z] structure
        blocks = []
        for x in range(self.width):
            x_layer = []
            z_layer = []
            for z in range(self.height):
                block = self.alive_block if self.grid[x][z] == 1 else self.dead_block
                z_layer.append(block)
            x_layer.append(z_layer)  # Single Y layer
            blocks.append(x_layer)

        # Use edit() for high-performance bulk placement
        self.mc.edit(self.origin_x, self.origin_y, self.origin_z, blocks)

    def load_pattern(self, pattern_name: str):
        """Load a predefined pattern"""
        self.clear_grid()

        # Center position
        cx, cz = self.width // 2, self.height // 2

        patterns = {
            "glider": [
                (0, 1), (1, 2), (2, 0), (2, 1), (2, 2)
            ],
            "blinker": [
                (0, 0), (0, 1), (0, 2)
            ],
            "toad": [
                (1, 0), (1, 1), (1, 2),
                (0, 1), (0, 2), (0, 3)
            ],
            "beacon": [
                (0, 0), (1, 0), (0, 1),
                (2, 3), (3, 3), (3, 2)
            ],
            "pulsar": [
                # Top section
                (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
                (0, 2), (5, 2), (7, 2), (12, 2),
                (0, 3), (5, 3), (7, 3), (12, 3),
                (0, 4), (5, 4), (7, 4), (12, 4),
                (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
                # Middle gap
                (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
                # Bottom section (mirror)
                (0, 8), (5, 8), (7, 8), (12, 8),
                (0, 9), (5, 9), (7, 9), (12, 9),
                (0, 10), (5, 10), (7, 10), (12, 10),
                (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12),
            ],
            "glider_gun": [
                # Left square
                (0, 4), (0, 5), (1, 4), (1, 5),
                # Left part
                (10, 4), (10, 5), (10, 6), (11, 3), (11, 7),
                (12, 2), (12, 8), (13, 2), (13, 8),
                (14, 5), (15, 3), (15, 7), (16, 4), (16, 5), (16, 6),
                (17, 5),
                # Middle part
                (20, 2), (20, 3), (20, 4), (21, 2), (21, 3), (21, 4),
                (22, 1), (22, 5), (24, 0), (24, 1), (24, 5), (24, 6),
                # Right square
                (34, 2), (34, 3), (35, 2), (35, 3),
            ],
            "r_pentomino": [
                (0, 1), (1, 0), (1, 1), (1, 2), (2, 0)
            ],
            "diehard": [
                (6, 0),
                (0, 1), (1, 1),
                (1, 2), (5, 2), (6, 2), (7, 2)
            ],
            "acorn": [
                (1, 0),
                (3, 1),
                (0, 2), (1, 2), (4, 2), (5, 2), (6, 2)
            ],
        }

        if pattern_name in patterns:
            for x, z in patterns[pattern_name]:
                # Center the pattern
                self.set_cell(cx + x - 5, cz + z - 5, True)
            print(f"Loaded pattern: {pattern_name}")
        else:
            print(f"Unknown pattern: {pattern_name}")
            print(f"Available patterns: {', '.join(patterns.keys())}")

    def run(self, generations: int = 100, delay: float = 0.5, loop: bool = False):
        """Run the simulation for a number of generations

        Args:
            generations: Number of generations to run per cycle
            delay: Delay between generations in seconds
            loop: If True, restart simulation after completing all generations
        """
        print(f"Starting Game of Life simulation...")
        print(f"Grid size: {self.width}x{self.height}")
        print(f"Location: ({self.origin_x}, {self.origin_y}, {self.origin_z})")

        if loop:
            print(f"Mode: Looping (Press Ctrl+C to stop)")
        else:
            print(f"Mode: Single run")

        cycle = 1
        while True:
            if loop:
                print(f"\n{'='*40}")
                print(f"Cycle {cycle}")
                print(f"{'='*40}\n")

            # Initial render
            self.render()
            time.sleep(2)  # Wait 2 seconds to see initial state

            for gen in range(generations):
                self.next_generation()
                self.render()
                if loop:
                    print(f"Cycle {cycle} - Generation {gen + 1}/{generations}")
                else:
                    print(f"Generation {gen + 1}/{generations}")
                time.sleep(delay)

            if not loop:
                print("Simulation complete!")
                break

            # Reset pattern for next cycle
            print(f"\nCycle {cycle} complete! Resetting pattern...")
            cycle += 1
            time.sleep(1)  # Brief pause between cycles


class Preset:
    """Configuration preset for Game of Life"""
    def __init__(self, name: str, description: str, pattern: str, width: int,
                 height: int, generations: int, delay: float,
                 alive_block: str, dead_block: str):
        self.name = name
        self.description = description
        self.pattern = pattern
        self.width = width
        self.height = height
        self.generations = generations
        self.delay = delay
        self.alive_block = alive_block
        self.dead_block = dead_block


# Define 5 preset configurations
PRESETS = [
    Preset(
        name="Classic Glider",
        description="Small grid with a classic glider pattern moving diagonally",
        pattern="glider",
        width=30,
        height=30,
        generations=150,
        delay=0.4,
        alive_block="minecraft:glowstone",
        dead_block="minecraft:black_concrete"
    ),
    Preset(
        name="Pulsar Show",
        description="Medium grid showcasing beautiful pulsar oscillations",
        pattern="pulsar",
        width=40,
        height=40,
        generations=100,
        delay=0.6,
        alive_block="minecraft:sea_lantern",
        dead_block="minecraft:blue_concrete"
    ),
    Preset(
        name="Glider Gun Factory",
        description="Large grid with glider gun continuously producing gliders",
        pattern="glider_gun",
        width=60,
        height=60,
        generations=300,
        delay=0.5,
        alive_block="minecraft:redstone_lamp",
        dead_block="minecraft:gray_concrete"
    ),
    Preset(
        name="Chaos Lab",
        description="Medium grid with fast-evolving chaotic acorn pattern",
        pattern="acorn",
        width=50,
        height=50,
        generations=500,
        delay=0.2,
        alive_block="minecraft:emerald_block",
        dead_block="minecraft:black_concrete"
    ),
    Preset(
        name="Rainbow Oscillators",
        description="Small grid displaying beacon oscillator patterns",
        pattern="beacon",
        width=35,
        height=35,
        generations=80,
        delay=0.5,
        alive_block="minecraft:diamond_block",
        dead_block="minecraft:purple_concrete"
    )
]


def display_menu():
    """Display preset selection menu"""
    print("\n" + "="*60)
    print("Conway's Game of Life - Minecraft Edition")
    print("="*60)
    print("\nPlease select a preset:\n")

    for i, preset in enumerate(PRESETS, 1):
        print(f"{i}. {preset.name}")
        print(f"   {preset.description}")
        print(f"   Pattern: {preset.pattern} | Size: {preset.width}x{preset.height} | "
              f"Generations: {preset.generations}\n")

    print("0. Exit")
    print("="*60)


def get_user_choice() -> int:
    """Get and validate user's preset choice"""
    while True:
        try:
            choice = input(f"\nEnter choice [0-{len(PRESETS)}]: ").strip()
            choice_num = int(choice)
            if 0 <= choice_num <= len(PRESETS):
                return choice_num
            else:
                print(f"Please enter a number between 0 and {len(PRESETS)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\nCancelled")
            return 0


def get_loop_choice() -> bool:
    """Ask user if they want to loop the simulation"""
    while True:
        try:
            choice = input("\nLoop simulation? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")
        except KeyboardInterrupt:
            print("\n\nDefaulting to single run")
            return False


def main():
    # Load environment variables
    load_dotenv()

    # Configuration from environment
    SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
    SERVER_PORT = int(os.getenv("SERVER_PORT", "65535"))
    TOKEN = os.getenv("SERVER_TOKEN", "")

    if not TOKEN:
        print("Error: SERVER_TOKEN not found in .env file")
        print("Please copy .env.example to .env and add your token")
        return

    try:
        # Initialize connection
        print("Connecting to Minecraft server...")
        mc = MCPyLib(ip=SERVER_IP, port=SERVER_PORT, token=TOKEN)
        print("Connected successfully!")
    except Exception as e:
        print(f"Connection error: {e}")
        return

    # Get player position
    try:
        player_name = os.getenv("PLAYER_NAME", "Player")
        ORIGIN_X, ORIGIN_Y, ORIGIN_Z = mc.getPos(player_name)
        print(f"Player position: ({ORIGIN_X}, {ORIGIN_Y}, {ORIGIN_Z})")
    except Exception as e:
        print(f"Cannot get player position: {e}")
        print("Using default position: (100, 64, 100)")
        ORIGIN_X, ORIGIN_Y, ORIGIN_Z = 100, 64, 100

    # Display menu and get user choice
    display_menu()
    choice = get_user_choice()

    if choice == 0:
        print("\nGoodbye!")
        return

    # Get selected preset
    preset = PRESETS[choice - 1]
    print(f"\nSelected: {preset.name}")

    # Ask if user wants to loop
    loop_enabled = get_loop_choice()
    print()

    try:
        # Create Game of Life instance with preset configuration
        game = GameOfLife(mc, ORIGIN_X, ORIGIN_Y, ORIGIN_Z,
                          preset.width, preset.height)

        # Apply preset block types
        game.alive_block = preset.alive_block
        game.dead_block = preset.dead_block

        # Build platform base
        print("Building platform...")
        mc.fill(ORIGIN_X - 1, ORIGIN_Y - 1, ORIGIN_Z - 1,
                ORIGIN_X + preset.width, ORIGIN_Y - 1, ORIGIN_Z + preset.height,
                "minecraft:stone")

        # Build border walls
        print("Building border...")
        mc.fill(ORIGIN_X - 2, ORIGIN_Y, ORIGIN_Z - 2,
                ORIGIN_X + preset.width + 1, ORIGIN_Y + 2, ORIGIN_Z - 2,
                "minecraft:glass")
        mc.fill(ORIGIN_X - 2, ORIGIN_Y, ORIGIN_Z + preset.height + 1,
                ORIGIN_X + preset.width + 1, ORIGIN_Y + 2, ORIGIN_Z + preset.height + 1,
                "minecraft:glass")
        mc.fill(ORIGIN_X - 2, ORIGIN_Y, ORIGIN_Z - 2,
                ORIGIN_X - 2, ORIGIN_Y + 2, ORIGIN_Z + preset.height + 1,
                "minecraft:glass")
        mc.fill(ORIGIN_X + preset.width + 1, ORIGIN_Y, ORIGIN_Z - 2,
                ORIGIN_X + preset.width + 1, ORIGIN_Y + 2, ORIGIN_Z + preset.height + 1,
                "minecraft:glass")

        # Store initial pattern
        initial_pattern = preset.pattern

        # Load pattern and run simulation
        print(f"Loading pattern: {preset.pattern}")
        game.load_pattern(preset.pattern)

        print(f"\nStarting simulation...")
        print(f"Grid size: {preset.width}x{preset.height}")
        print(f"Generations: {preset.generations}")
        print(f"Delay: {preset.delay}s")

        if loop_enabled:
            print(f"Mode: Looping (pattern will reset after each cycle)\n")

            # Override run method to reset pattern in loop mode
            original_run = game.run
            def run_with_reset(*args, **kwargs):
                cycle = 1
                while True:
                    if cycle > 1:
                        print(f"\nCycle {cycle} - Resetting pattern...")
                        game.load_pattern(initial_pattern)
                        time.sleep(1)

                    print(f"\n{'='*40}")
                    print(f"Cycle {cycle}")
                    print(f"{'='*40}\n")

                    # Run single cycle without loop parameter
                    kwargs_copy = kwargs.copy()
                    kwargs_copy['loop'] = False
                    game.render()
                    time.sleep(2)

                    for gen in range(kwargs['generations']):
                        game.next_generation()
                        game.render()
                        print(f"Cycle {cycle} - Generation {gen + 1}/{kwargs['generations']}")
                        time.sleep(kwargs.get('delay', 0.5))

                    cycle += 1

            game.run = run_with_reset
        else:
            print()

        game.run(generations=preset.generations, delay=preset.delay, loop=loop_enabled)

    except KeyboardInterrupt:
        print("\n\nSimulation paused")
        print("Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nPlease make sure:")
        print("1. Minecraft server is running")
        print("2. MCPyLib plugin is installed")
        print("3. TOKEN is correct")
        print("4. Server IP and PORT are correct")


if __name__ == "__main__":
    main()
