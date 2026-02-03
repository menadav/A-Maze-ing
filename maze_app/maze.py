from typing import Dict, Union, List, Tuple
from maze_app.render.render import render_ascii
from maze_app.themes import classic_theme
from maze_app.generator.MazeGenerator import MazeGenerator


class Maze:
    """
    Simple wrapper that manages the maze: generating it, solving it,
    choosing a theme, and showing it on screen.
    """

    def __init__(self, generator: "MazeGenerator", file_name: str) -> None:
        """Store the generator, default theme, and output file name."""
        self.generator = generator
        self.themes = classic_theme()
        self.current_solver = generator.solver
        self.current_algorithm = generator.algorithm
        self.file_name = file_name

    def generate(self) -> None:
        """Create a new maze using the current settings."""
        self.generator.generate()

    def solve(self, mode: str = "way") -> Union[List[Tuple[int, int]], str]:
        """Solve the maze and return either coordinates or directions."""
        return self.generator.get_solution(mode)

    def set_theme(self, theme_dict: Dict[str, str]) -> None:
        """Change the color theme used when rendering."""
        self.themes = theme_dict

    def render(self, show_path: bool = False) -> None:
        """Draw the maze in ASCII, with or without the solution path."""
        render_ascii(
            mz=self.generator,
            show_path=show_path,
            themes=self.themes,
            name_file=self.file_name,
        )
