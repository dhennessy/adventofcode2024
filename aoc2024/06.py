"""Advent of Code: 2024 - Day 06."""

from __future__ import annotations

from aoc2024.grid import Dir, Grid, Point
from . import utils


def example() -> str:
    return """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def walk_path(start: Point, dir: Dir, grid: Grid) -> list[Point, Dir] | None:
    path = []
    path_set = set()
    p = start
    while True:
        c = grid.get(p.move(dir))
        if c is None:
            break
        while c == "#":
            dir = dir.turn_right()
            c = grid.get(p.move(dir))
        p = p.move(dir)
        if (p, dir) in path_set:
            return None
        path.append((p, dir))
        path_set.add((p, dir))
    return path

def solve(data: list[str] | None = None) -> tuple[int, int]:
    grid = Grid.from_map(read_data(data=data))
    start = grid.find("^")

    path = walk_path(start, Dir.N, grid)
    positions = set()
    for p, dir in path:
        positions.add(p)
    p1 = len(positions)

    obstacles = set()
    for pt in positions:
        if grid.get(pt) == ".":
            grid.set(pt, "#")
            if walk_path(start, Dir.N, grid) is None:
                obstacles.add(pt)
            grid.set(pt, ".")
    p2 = len(obstacles)

    return p1, p2


def test_solve() -> None:
    assert solve() == (41, 6)
