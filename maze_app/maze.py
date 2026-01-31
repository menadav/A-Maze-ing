from maze_app.render.render import render_ascii
from maze_app.themes import classic_theme


class Maze:
    def __init__(self, generator):
        self.generator = generator
        self.colors = classic_theme()
        self.current_solver = generator.solver
        self.current_algorithm = generator.algorithm

    def generate(self):
        self.generator.generate()

    def swap_generate(self):
        return self.generator.swap_generate(self.current_algorithm)

    def solve(self, mode="way"):
        return self.generator.get_solution(mode)

    def set_theme(self, theme_dict):
        self.colors = theme_dict

    def render(self, show_path=False):
        render_ascii(
            mz=self.generator,
            show_path=show_path,
            colors=self.colors
        )

