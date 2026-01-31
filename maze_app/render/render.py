from typing import Optional, Dict
from maze_app.output.file_maze import generetor_file_maze
from maze_app.generator.MazeGenerator import MazeGenerator, Wall
from maze_app.themes import classic_theme, dark_theme, forest_theme, neon_theme

def render_ascii(
    mz: MazeGenerator,
    show_path: bool = True,
    colors: Dict[str, str] = None,
    name_file: Optional[str] = "maze.txt"
):
    if colors is None:
        colors = {
            "wall": "\033[97m",
            "entry": "\033[92m",
            "exit": "\033[91m",
            "path": "\033[93m",
            "reset": "\033[0m"
        }

    wall_char = "\u2588\u2588"

    path_list = mz.get_solution("way") if show_path else []
    path_set = set(path_list)

    p42_set = mz.pattern42_coords if mz.pattern42_coords else set()
    pattern42_color = "\033[35m"

    w_col = colors["wall"]
    e_col = colors["entry"]
    x_col = colors["exit"]
    p_col = colors["path"]
    res = colors["reset"]

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

    generetor_file_maze(
        mz.grid,
        mz.entry,
        mz.exit,
        mz.get_solution(),
        name_file
    )
