from enum import Enum
from typing import Any

class Dir(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)

    @classmethod
    def from_sym(cls, sym):
        match sym:
            case "^":
                return Dir.N
            case ">":
                return Dir.E
            case "v":
                return Dir.S
            case "<":
                return Dir.W
        print("Invalid symbol: '{sym}'")
        
    def sym(self):
        match self:
            case Dir.N:
                return "^"
            case Dir.E:
                return ">"
            case Dir.S:
                return "v"
            case Dir.W:
                return "<"

    def turn_left(self) -> "Dir":
        match self:
            case Dir.N:
                return Dir.W
            case Dir.E:
                return Dir.N
            case Dir.S:
                return Dir.E
            case Dir.W:
                return Dir.S

    def turn_right(self) -> "Dir":
        match self:
            case Dir.N:
                return Dir.E
            case Dir.E:
                return Dir.S
            case Dir.S:
                return Dir.W
            case Dir.W:
                return Dir.N

    def turn_around(self) -> "Dir":
        return self.turn_left().turn_left()
    

class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.x, self.y}"

    def __repr__(self) -> str:
        return f"{self.x, self.y}"

    def __hash__(self):
        return hash(self.x) + hash(self.y)
    
    def __eq__(self, other):
        return self.__class__ == other.__class__ and \
            self.x == other.x and \
            self.y == other.y
    
    def move(self, dir: Dir | tuple[int], dist: int = 1) -> "Point":
        if type(dir) is Dir:
            return Point(self.x+dir.value[0]*dist, self.y+dir.value[1]*dist)
        else:
            return Point(self.x+dir[0]*dist, self.y+dir[1]*dist)
    
    def manhattan_dist(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def dir_to(self, other):
        dx, dy = other.x-self.x, other.y-self.y
        if abs(dx) > abs(dy):
            if dx > 0:
                return Dir.E
            else:
                return Dir.W
        else:
            if dy > 0:
                return Dir.S
            else:
                return Dir.N


class Grid(object):
    def __init__(self, w: int, h: int, fill: Any = None):
        self.w, self.h = w, h
        grid: dict[Point, str] = {}
        self.grid = grid
        if fill is not None:
            self.fill(fill)

    @classmethod
    def from_map(cls, g: list[str]):
        grid = cls(len(g[0].strip()), len(g))
        for y in range(grid.h):
            for x in range(grid.w):
                grid.set(Point(x, y), g[y][x])
        return grid
    
    def draw(self) -> str:
        return "\n".join(
            ["".join([self.grid[Point(x, y)] for x in range(self.w)]) for y in range(self.h)]
        )
    
    def fill(self, fill: Any):
        for pt in self.all_points():
            self.set(pt, fill)

    def get(self, p: Point) -> None | Any:
        try:
            return self.grid[Point(p.x, p.y)]
        except KeyError:
            return None

    def set(self, p: Point, v: str) -> None | Any:
        self.grid[Point(p.x, p.y)] = v

    def find(self, s: Any) -> None | Point:
        for k, v in self.grid.items():
            if v == s:
                return k
        return None

    def find_all(self, s: Any) -> list[Point]:
        pts = []
        for k, v in self.grid.items():
            if v == s:
                pts.append(k)
        return pts
    
    def all_points(self):
        return [Point(x, y) for x in range(self.w) for y in range(self.h)]

# def example() -> str:
#     return """
# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...
# """

# g = read_example(example())
# g = Grid(g)

# print("-"*40)
# print(f"Size: {g.w, g.h}")
# print(g.draw())
# print(f"Start: {g.find("^")}")
