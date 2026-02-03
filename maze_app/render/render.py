from typing import Optional, Dict
from maze_app.output.file_maze import generetor_file_maze
from maze_app.generator.MazeGenerator import MazeGenerator, Wall
from maze_app.themes import classic_theme


def render_ascii(
    mz: MazeGenerator,
    show_path: bool = True,
    themes: Dict[str, str] = classic_theme(),
    name_file: Optional[str] = "maze.txt"
) -> None:
    """
    Draw the maze in ASCII using colors and,
    if enabled, the solution path.
    Also saves the maze and solution to a file.
    """
    wall_char = "\u2588\u2588"

    path_list = mz.get_solution("way") if show_path else []
    path_set = set(path_list)

    p42_set = mz.pattern42_coords if mz.pattern42_coords else set()
    pattern42_color = "\033[35m"

    w_col = themes["wall"]
    e_col = themes["entry"]
    x_col = themes["exit"]
    p_col = themes["path"]
    res = themes["reset"]

    for y, row in enumerate(mz.grid):
        line_h = ""
        line_w = ""
        for x, cell_bits in enumerate(row):
            pos = (y, x)
            if cell_bits & Wall.NORTH.value:
                line_h += (f"{w_col}{wall_char}{res}" * 3)
            else:
                if pos in path_set and (y - 1, x) in path_set:
                    line_h += (
                        f"{w_col}{wall_char}{res}"
                        f"{p_col}{wall_char}{res}"
                        f"{w_col}{wall_char}{res}"
                    )
                else:
                    line_h += (
                        f"{w_col}{wall_char}{res}"
                        f"  {w_col}{wall_char}{res}"
                    )
            if pos == mz.entry:
                char_center = f"{e_col}{wall_char}{res}"
            elif pos == mz.exit:
                char_center = f"{x_col}{wall_char}{res}"
            elif pos in path_set:
                char_center = f"{p_col}{wall_char}{res}"
            elif pos in p42_set:
                char_center = f"{pattern42_color}{wall_char}{res}"
            else:
                char_center = "  "
            if cell_bits & Wall.WEST.value:
                line_w += f"{w_col}{wall_char}{res}"
            else:
                line_w += (
                    f"{p_col}{wall_char}{res}"
                    if (pos in path_set and (y, x - 1) in path_set)
                    else "  "
                )
            line_w += char_center
            if cell_bits & Wall.EAST.value:
                line_w += f"{w_col}{wall_char}{res}"
            else:
                line_w += (
                    f"{p_col}{wall_char}{res}"
                    if (pos in path_set and (y, x + 1) in path_set)
                    else "  "
                )
        print(line_h)
        print(line_w)
    print(f"{w_col}{wall_char}{res}" * 3 * len(mz.grid[0]))
    sol = mz.get_solution()
    if not isinstance(sol, str):
        sol = mz.print_coordinates(sol) if sol else ""
    final_name = name_file if name_file is not None else "maze.txt"
    generetor_file_maze(
        mz.grid,
        mz.entry,
        mz.exit,
        sol,
        final_name
    )
