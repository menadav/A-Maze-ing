import sys, random
from maze_app.generator.MazeGenerator import MazeGenerator
from parse.config_parser import read_config, parse_config
from parse.config_model import MazeConfig
from maze_app.maze import Maze
from maze_app.themes import classic_theme, dark_theme, forest_theme, neon_theme

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
        algorithm = config.algorithm
        solver = config.solver

        print(f"--- Configuración Cargada ({config_path}) ---")
        print(f"Dimensiones: {height}x{width} | Perfect: {perfect} | Seed: {seed}")

    except ValueError as e:
        print(f"Config error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


    if seed is not None:
        random.seed(seed)

    generator = MazeGenerator(height, width, entry, exit_pos, perfect, seed, algorithm, solver)
    maze = Maze(generator)

    maze.generate()
    maze.render()

    show_path = False
    paths = {"bfs": None, "dfs": None}

    while True:
        print("\n" + "="*20)
        print("  A-MAZE-ING MENU")
        print("="*20)
        print(f"1. Regenerate maze (Current: {maze.current_algorithm.upper()})")
        print(f"2. Show/Hide path (Current: {maze.current_solver.upper()})")
        print("3. Change algorithm (DFS/PRIM)")
        print("4. Change solver (BFS/DFS)")
        print("5. Change color theme")
        print("6. Exit")
        print(maze.generator.algorithm)

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            maze.generate()
            paths = {"bfs": None, "dfs": None}
            show_path = False
            maze.render()

        elif choice == "2":
            show_path = not show_path
            if show_path:
                if paths[maze.current_solver] is None:
                    paths[maze.current_solver] = maze.solve("way")

                path = paths[maze.current_solver]
                if path:
                    maze.render(show_path=True)
                    print("\nCoordinates:")
                    print(path)
                    print("\nDirections:", generator.print_coordinates(path))
                else:
                    print("\n[!] No path found!")
                    show_path = False
            else:
                maze.render()

        elif choice == "3":
            s_choice = input("Select Alghorithm (1: DFS, 2: PRIM): ").strip()
            maze.current_algorithm = "dfs" if s_choice == "1" else "prim"
            generator.algorithm = maze.current_algorithm
            print(f"Alghorithm changed to: {maze.current_algorithm.upper()}")

        elif choice == "4":
            s_choice = input("Select Solver (1: BFS, 2: DFS): ").strip()
            maze.current_solver = "bfs" if s_choice == "1" else "dfs"
            generator.solver = maze.current_solver
            print(f"Solver changed to: {maze.current_solver.upper()}")

        elif choice == "5":
            print("\n1. Classic")
            print("2. Dark")
            print("3. Forest")
            print("4. Neon")
            t = input("Choose a theme: ").strip()

            if t == "1":
                maze.set_theme(classic_theme())
            elif t == "2":
                maze.set_theme(dark_theme())
            elif t == "3":
                maze.set_theme(forest_theme())
            elif t == "4":
                maze.set_theme(neon_theme())

            maze.render(show_path)

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()

