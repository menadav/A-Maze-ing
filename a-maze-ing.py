import sys, random
from maze_app.maze_class import Maze
from maze_app.generator import PrimGenerator, ImperfectGenerator
from maze_app.utils import print_coordinates
from parse.config_parser import read_config, parse_config
from validation.config_model import MazeConfig


def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.txt"

    try:
        raw_config = read_config(config_path)
        parsed_config = parse_config(raw_config)
        config = MazeConfig(**parsed_config)

        height = config.height
        width = config.width
        entry = config.entry
        exit_pos = config.exit_
        seed = config.seed
        file = config.output_file
        perfect = config.perfect
        print(f"--- Configuración Cargada ({config_path}) ---")
        print(f"Dimensiones: {height}x{width} | Perfect: {perfect} | Seed: {seed}")
    except ValueError as e:
        for error in e.errors():
            print(f"Error {error['msg'][11:]}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    if seed is not None:
        random.seed(seed)

    maze = Maze(height, width, entry, exit_pos, file)

    if perfect:
        generator = PrimGenerator()
    else:
        generator = ImperfectGenerator()

    maze.generate(generator, seed)
    maze.render()

    show_path = False
    paths = {"bfs": None, "dfs": None}

    while True:
        print("\n" + "="*20)
        print("  A-MAZE-ING MENU")
        print("="*20)
        print("1. Regenerate maze")
        print(f"2. Show/Hide path (Current: {maze.current_solver.upper()})")
        print("3. Change solver (BFS/DFS)")
        print("4. Change maze wall color")
        print("5. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            maze.generate(generator, seed)
            paths = {"bfs": None, "dfs": None}
            show_path = False
            maze.render()

        elif choice == "2":
            show_path = not show_path
            if show_path:
                if paths[maze.current_solver] is None:
                    paths[maze.current_solver] = maze.solve()

                path = paths[maze.current_solver]
                if path:
                    maze.render(path)
                    print("\nCoordinates:")
                    print(path)
                    print("\nDirections:", print_coordinates(path))
                else:
                    print("\n[!] No path found!")
                    show_path = False
            else:
                maze.render()

        elif choice == "3":
            s_choice = input("Select Solver (1: BFS, 2: DFS): ").strip()
            maze.current_solver = "bfs" if s_choice == "1" else "dfs"
            print(f"Solver changed to: {maze.current_solver.upper()}")

        elif choice == "4":
            print("\n1. Blue | 2. Purple | 3. Orange | 4. White")
            c_idx = input("Choose wall color: ").strip()
            cmap = {
                "1": "\033[94m",
                "2": "\033[35m",
                "3": "\033[38;2;255;165;0m",
                "4": "\033[97m"
            }
            if c_idx in cmap:
                maze.set_colors({"wall": cmap[c_idx]})
                current_p = paths[maze.current_solver] if show_path else None
                maze.render(current_p)

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
