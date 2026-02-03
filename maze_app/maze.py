from typing import Dict, Union, List, Tuple
from maze_app.render.render import render_ascii
from maze_app.themes import classic_theme
from maze_app.generator.MazeGenerator import MazeGenerator


class Maze:
    """Manage maze generation, solving, themes, and rendering."""

    def __init__(self, generator: "MazeGenerator", file_name: str) -> None:
        """Initialize the maze wrapper.

        Args:
            generator: Maze generator instance.
            file_name: Name of the output file.
        """
        self.generator = generator
        self.themes = classic_theme()
        self.current_solver = generator.solver
        self.current_algorithm = generator.algorithm
        self.file_name = file_name

    def generate(self) -> None:
        """Generate a new maze using the current settings."""
        self.generator.generate()

    def solve(self, mode: str = "way") -> Union[List[Tuple[int, int]], str]:
        """Solve the maze.

        Args:
            mode: Output format ("way" for coordinates or directions).

        Returns:
            A list of coordinates or a direction string.
        """
        return self.generator.get_solution(mode)

    def set_theme(self, theme_dict: Dict[str, str]) -> None:
        """Set the color theme used for rendering.

        Args:
            theme_dict: Mapping of color roles to ANSI codes.
        """
        self.themes = theme_dict

    def render(self, show_path: bool = False) -> None:
        """Render the maze in ASCII.

        Args:
            show_path: Whether to display the solution path.
        """
        render_ascii(
            mz=self.generator,
            show_path=show_path,
            themes=self.themes,
            name_file=self.file_name,
        )
