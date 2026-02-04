#!/usr/bin/env python3

import sys
import random
import os

try:
    from pydantic import ValidationError
except ModuleNotFoundError:
    sys.stderr.write("\033[91mError: Pydantic not installed yet.\n"
                     "Run: make install\n\033[0m")
    sys.exit(1)

from typing import List, Tuple, Dict, Optional, Union
from maze_app.generator.MazeGenerator import MazeGenerator
from parse.config_parser import read_config, parse_config
from parse.config_model import MazeConfig
from maze_app.maze import Maze
from maze_app.themes import classic_theme, dark_theme, neon_theme


def main() -> None:
    """Run the maze application.

    Loads the configuration file, initializes the maze generator,
    renders the initial maze, and provides an interactive menu for
    regenerating, solving, and customizing the maze.

    Raises:
        SystemExit: If configuration loading or maze generation fails.
    """
    config_path = "config.txt"
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
        os.system("clear")

    except ValidationError as e:
        for error in e.errors():
            clean = error["msg"][13:]
            sys.stderr.write(f"Config error: {clean} \n")
        sys.exit(1)

    except ValueError as e:
        sys.stderr.write(f"Error: {e} \n")
        sys.exit(1)

    except Exception as e:
        sys.stderr.write(f"Error: {e} \n")
        sys.exit(1)

    blue = "\033[96m"
    orange = "\033[38;5;209m"
    pink = "\033[38;5;218m"
    purple = "\033[38;5;97m"
    brown = "\033[38;5;180m"
    red = "\033[91m"
    green = "\033[38;5;192m"
    reset = "\033[0m"

    if seed is not None:
        random.seed(seed)

    generator = MazeGenerator(
        height, width, entry, exit_pos, perfect, seed, algorithm, solver
    )
    maze = Maze(generator, file)

    try:
        maze.generate()
        maze.render()
    except Exception as e:
        sys.stderr.write(f"Generation error: {e}\n")
        sys.exit(1)

    print(f"\n{purple}--- Configuration Loaded ({config_path}) ---")
    print(
        f"Dimensions: {height}x{width} "
        f"| Perfect: {perfect} | Seed: {seed}{reset}"
    )

    show_path = False
    paths: Dict[str, Optional[Union[List[Tuple[int, int]], str]]] = {
        "bfs": None,
        "dfs": None,
    }
    try:
        while True:
            curr_alg = (
                maze.current_algorithm if maze.current_algorithm else "unknown"
            )
            curr_sol = (
                maze.current_solver if maze.current_solver else "unknown"
            )

            print("\n" + green + "=" * 20)
            print("  A-MAZE-ING MENU")
            print("=" * 20)
            print(
                f"{reset}{blue}1. Regenerate maze"
                f"(Current: {curr_alg.upper()})"
            )
            print(f"2. Show/Hide path (Current: {curr_sol.upper()})")
            print("3. Change algorithm")
            print("4. Change solver")
            print("5. Change color theme")
            print("6. Exit", reset)

            try:
                choice = input(f"\n{brown}Select an option: {reset}").strip()
            except EOFError:
                break

            if choice == "1":
                os.system("clear")
                maze.generate()
                paths = {"bfs": None, "dfs": None}
                show_path = False
                maze.render()
                print(
                    f"\n{purple}--- Configuration"
                    f"Loaded ({config_path}) ---"
                )
                print(
                    f"Dimensions: {height}x{width} "
                    f"| Perfect: {perfect} | Seed: {seed}{reset}"
                )

            elif choice == "2":
                os.system("clear")
                show_path = not show_path
                solver_key = maze.current_solver
                if show_path and isinstance(solver_key, str):
                    if paths.get(solver_key) is None:
                        paths[solver_key] = maze.solve("way")
                    path = paths[solver_key]
                    if isinstance(path, list):
                        maze.render(show_path=True)
                        print("\nCoordinates:")
                        print(path)
                        print(
                            "\nDirections:"
                            f"{generator.print_coordinates(path)}"
                        )
                    elif isinstance(path, str) and path != "":
                        maze.render(show_path=True)
                        print(f"\n{path}")
                    else:
                        print("\n[!] No path found!")
                        show_path = False
                else:
                    maze.render()
                    print(
                        f"\n{purple}--- Configuration"
                        f"Loaded ({config_path}) --"
                    )
                    print(
                        f"Dimensions: {height}x{width} "
                        f"| Perfect: {perfect} | Seed: {seed}{reset}"
                    )

            elif choice == "3":
                while True:
                    print(orange + "1: PRIM\n" "2: DFS\n" "3: Exit\n", reset)
                    a_choice = input(
                        f"{brown}Select Algorithm: "f"{reset}").strip()
                    if a_choice == "1":
                        maze.current_algorithm = "prim"
                        break
                    elif a_choice == "2":
                        maze.current_algorithm = "dfs"
                        break
                    elif a_choice == "3":
                        break
                    else:
                        print(f"{red}Invalid option. Try again. {reset}")

                os.system("clear")
                generator.algorithm = maze.current_algorithm
                maze.render(show_path)
                alg_display = (
                    maze.current_algorithm if maze.current_algorithm else ""
                )
                print(
                    f"\n{purple}Algorithm changed to:"
                    f"{alg_display.upper()}{reset}"
                )

            elif choice == "4":
                while True:
                    print(orange + "1: BFS\n" "2: DFS\n" "3: Exit\n", reset)
                    s_choice = input(f"{brown}Select Solver:{reset}").strip()
                    if s_choice == "1":
                        maze.current_solver = "bfs"
                        break
                    elif s_choice == "2":
                        maze.current_solver = "dfs"
                        break
                    elif s_choice == "3":
                        break
                    else:
                        print(f"{red}Invalid option. Try again.{reset}")
                os.system("clear")
                generator.solver = maze.current_solver
                maze.render(show_path)
                sol_display = (
                    maze.current_solver if maze.current_solver else ""
                )
                print(
                    f"\n{purple}Solver changed to:"
                    f"{sol_display.upper()}{reset}"
                )

            elif choice == "5":
                while True:
                    print(f"{orange}1. Classic")
                    print("2. Dark")
                    print("3. Neon")
                    print("4. Exit")

                    print()
                    t = input(f"{brown}Choose a theme:{reset}").strip()

                    if t == "1":
                        maze.set_theme(classic_theme())
                        break
                    elif t == "2":
                        maze.set_theme(dark_theme())
                        break
                    elif t == "3":
                        maze.set_theme(neon_theme())
                        break
                    elif t == "4":
                        break
                    else:
                        print(f"{red}Invalid option. Try again.{reset}")
                os.system("clear")
                maze.render(show_path)

            elif choice == "6":
                break
            else:
                os.system("clear")
                maze.render(show_path)
                print(f"\n{red}Invalid option. Try again.{reset}")
    except KeyboardInterrupt:
        pass
    finally:
        os.system("clear")
        print()
        print(f"{pink}=" * 21)
        print("      Goodbye!")
        print("Thanks for testing me")
        print("=" * 21 + reset)
        print()


if __name__ == "__main__":
    main()
