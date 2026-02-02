from typing import Any, Dict, Union, List, Tuple
from maze_app.render.render import render_ascii
from maze_app.themes import classic_theme
from maze_app.generator.MazeGenerator import MazeGenerator


class Maze:
    def __init__(self, generator: "MazeGenerator", file_name: str) -> None:
        self.generator = generator
        self.themes = classic_theme()
        self.current_solver = generator.solver
        self.current_algorithm = generator.algorithm
        self.file_name = file_name

    def generate(self) -> None:
        self.generator.generate()

    def swap_generate(self) -> Any:
        algo = (
            self.current_algorithm
            if self.current_algorithm is not None
            else "prim"
        )
        return self.generator.swap_generate(algo)

    def solve(self, mode: str = "way") -> Union[List[Tuple[int, int]], str]:
        return self.generator.get_solution(mode)

    def set_theme(self, theme_dict: Dict[str, str]) -> None:
        self.themes = theme_dict

    def render(self, show_path: bool = False) -> None:
        render_ascii(
            mz=self.generator,
            show_path=show_path,
            themes=self.themes,
            name_file=self.file_name,
        )
