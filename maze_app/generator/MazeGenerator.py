import random
from enum import IntEnum
from typing import List, Tuple, Set, Optional, Dict, Union


class Wall(IntEnum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class MazeGenerator:
    def __init__(
        self,
        height: int,
        width: int,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        perfect: bool,
        seed: Optional[int] = None,
        algorithm: Optional[str] = "prim",
        solver: Optional[str] = "bfs",
    ):
        self.height = height
        self.width = width
        self.entry = entry
        self.exit = exit_
        self.perfect = perfect
        self.seed = seed
        self.algorithm = algorithm
        self.solver = solver
        self.grid: List[List[int]] = []
        self.pattern42_coords: Set[Tuple[int, int]] = set()

    def generate(self) -> List[List[int]]:
        if self.seed is not None:
            random.seed(self.seed)
        self.grid = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        if self.algorithm == "prim":
            self._generate_prim()
        elif self.algorithm == "dfs":
            self._generate_dfs()
        return self.grid

    def _generate_dfs(self) -> List[List[int]]:
        self.pattern42_coords = set()
        visited: Set[Tuple[int, int]] = set()
        if self.width >= 15 and self.height >= 15:
            self._write_42(visited)
        start_f, start_c = self.entry
        pila: List[Tuple[int, int]] = [(start_f, start_c)]
        visited.add((start_f, start_c))
        while pila:
            f, c = pila[-1]
            unvisted_neighbors = []
            for direction in list(Wall):
                nf, nc = self._get_neighbor_coords(f, c, direction)
                if (
                    0 <= nf < self.height
                    and 0 <= nc < self.width
                    and (nf, nc) not in visited
                ):
                    unvisted_neighbors.append((nf, nc, direction))
            if unvisted_neighbors:
                nf, nc, direction = random.choice(unvisted_neighbors)
                self._connect_cells(f, c, direction)
                visited.add((nf, nc))
                pila.append((nf, nc))
            else:
                pila.pop()
        if self.perfect is False:
            self._apply_imperfect_logic(self.calculate_chance())
        return self.grid

    def _generate_prim(self) -> List[List[int]]:
        self.pattern42_coords = set()
        visited: Set[Tuple[int, int]] = set()
        if self.width >= 15 and self.height >= 15:
            self._write_42(visited)
        start_f, start_c = self.entry
        visited.add((start_f, start_c))
        walls: List[Tuple[int, int, Wall]] = [
            (start_f, start_c, d) for d in Wall
        ]
        while walls:
            idx = random.randrange(len(walls))
            f, c, direction = walls.pop(idx)
            nf, nc = self._get_neighbor_coords(f, c, direction)
            if (
                0 <= nf < self.height
                and 0 <= nc < self.width
                and (nf, nc) not in visited
                and (nf, nc) not in self.pattern42_coords
            ):
                self._connect_cells(f, c, direction)
                visited.add((nf, nc))
                for d in Wall:
                    walls.append((nf, nc, d))
        if self.perfect is False:
            self._apply_imperfect_logic(self.calculate_chance())
        return self.grid

    def get_solution(
        self, output_type: Optional[str] = "str"
    ) -> Union[List[Tuple[int, int]], str]:
        path = self.bfs() if self.solver == "bfs" else self.dfs_solution()
        if output_type == "way":
            return path if path is not None else []
        return self.print_coordinates(path) if path else ""

    def dfs_solution(self) -> Optional[List[Tuple[int, int]]]:
        way = self.entry
        objective = self.exit
        stack: List[Tuple[int, int]] = [way]
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {way: None}
        directions = [
            (-1, 0, Wall.NORTH),
            (0, 1, Wall.EAST),
            (1, 0, Wall.SOUTH),
            (0, -1, Wall.WEST),
        ]
        while stack:
            actual = stack.pop()
            y, x = actual
            if actual == objective:
                return self.reconstruct_path(parent, objective)
            for dy, dx, wall_type in directions:
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    if not (self.grid[y][x] & wall_type.value):
                        if (ny, nx) not in parent:
                            parent[(ny, nx)] = actual
                            stack.append((ny, nx))
        return None

    def reconstruct_path(
        self,
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]],
        target: Optional[Tuple[int, int]],
    ) -> List[Tuple[int, int]]:
        path: List[Tuple[int, int]] = []
        while target is not None:
            path.append(target)
            target = parent[target]
        return path[::-1]

    def bfs(self) -> Optional[List[Tuple[int, int]]]:
        way = self.entry
        objective = self.exit
        queue: List[Tuple[int, int]] = [way]
        head = 0
        parent: Dict[Tuple[int, int], Optional[Tuple[int, int]]] = {way: None}
        directions = [
            (-1, 0, Wall.NORTH),
            (0, 1, Wall.EAST),
            (1, 0, Wall.SOUTH),
            (0, -1, Wall.WEST),
        ]
        while head < len(queue):
            actual = queue[head]
            head += 1
            y, x = actual
            if actual == objective:
                return self.reconstruct_path(parent, objective)
            for dy, dx, wall_type in directions:
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    if not (self.grid[y][x] & wall_type.value):
                        if (ny, nx) not in parent:
                            parent[(ny, nx)] = actual
                            queue.append((ny, nx))
        return None

    def print_coordinates(self, way: List[Tuple[int, int]]) -> str:
        if not way:
            return ""
        coordinates = ""
        for i in range(len(way) - 1):
            f, c = way[i]
            nf, nc = way[i + 1]
            if f > nf:
                coordinates += "N"
            elif f < nf:
                coordinates += "S"
            elif c > nc:
                coordinates += "W"
            elif c < nc:
                coordinates += "E"
        return coordinates

    def _get_neighbor_coords(
        self, f: int, c: int, direction: Wall
    ) -> Tuple[int, int]:
        if direction == Wall.NORTH:
            return f - 1, c
        if direction == Wall.SOUTH:
            return f + 1, c
        if direction == Wall.EAST:
            return f, c + 1
        if direction == Wall.WEST:
            return f, c - 1
        return f, c

    def _connect_cells(self, f: int, c: int, direction: Wall) -> bool:
        if not (self.grid[f][c] & direction.value):
            return False
        if direction == Wall.NORTH and f > 0:
            self.grid[f][c] &= ~Wall.NORTH
            self.grid[f - 1][c] &= ~Wall.SOUTH
            return True
        elif direction == Wall.SOUTH and f + 1 < self.height:
            self.grid[f][c] &= ~Wall.SOUTH
            self.grid[f + 1][c] &= ~Wall.NORTH
            return True
        elif direction == Wall.EAST and c + 1 < self.width:
            self.grid[f][c] &= ~Wall.EAST
            self.grid[f][c + 1] &= ~Wall.WEST
            return True
        elif direction == Wall.WEST and c > 0:
            self.grid[f][c] &= ~Wall.WEST
            self.grid[f][c - 1] &= ~Wall.EAST
            return True
        return False

    def _get_neighbor_bits(self, f: int, c: int, direction: int = 0) -> int:
        return self.grid[f][c + direction]

    def calculate_chance(self) -> float:
        area = self.width * self.height
        steps: List[Tuple[int, float]] = [
            (9, 1.0),
            (25, 0.8),
            (45, 0.7),
            (60, 0.6),
            (90, 0.5),
            (120, 0.4),
        ]
        for limit, probability in steps:
            if area < limit:
                return probability
        return 0.1

    def _apply_imperfect_logic(self, chance: float) -> "MazeGenerator":
        walls_broken = 0
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 2):
                if (y, x) in self.pattern42_coords or (
                    y,
                    x + 1,
                ) in self.pattern42_coords:
                    continue
                if random.random() < chance and (
                    self.grid[y][x] & Wall.EAST.value
                ):
                    if (
                        self._get_neighbor_bits(y, x) != 2
                        and self._get_neighbor_bits(y, x, 1) != 8
                    ):
                        self._connect_cells(y, x, Wall.EAST)
                        walls_broken += 1
        if walls_broken == 0:
            possible = []
            for y in range(self.height):
                for x in range(self.width):
                    for d in list(Wall):
                        possible.append((y, x, d))
            random.shuffle(possible)
            for y, x, d in possible:
                if self._connect_cells(y, x, d):
                    break
        return self

    def _write_42(self, visited: Set[Tuple[int, int]]) -> None:
        start_f, start_c = (self.height // 2) - 2, (self.width // 2) - 3
        pattern = [
            (0, 0),
            (1, 0),
            (2, 0),
            (2, 1),
            (2, 2),
            (3, 2),
            (4, 2),
            (0, 4),
            (0, 5),
            (0, 6),
            (1, 6),
            (2, 6),
            (2, 5),
            (2, 4),
            (3, 4),
            (4, 4),
            (4, 5),
            (4, 6),
        ]
        move = [
            (0, 0),
            (-1, 0),
            (0, 1),
            (1, 0),
            (1, 0),
            (0, -1),
            (0, -1),
            (-1, 0),
            (-1, 0),
            (0, 1),
            (-1, -1),
        ]
        for df, dc in move:
            start_f += df
            start_c += dc
            current = {(r + start_f, col + start_c) for r, col in pattern}
            if (
                0 <= start_f <= self.height - 5
                and 0 <= start_c <= self.width - 7
            ) and not (self.entry in current or self.exit in current):
                for f, c in current:
                    self.pattern42_coords.add((f, c))
                    visited.add((f, c))
                return
