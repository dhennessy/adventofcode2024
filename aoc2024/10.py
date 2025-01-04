"""Advent of Code: 2024 - Day 10."""

from __future__ import annotations
from aoc2024.grid import Dir, Grid, Point

from . import utils


def example() -> str:
    return """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())


def explore(grid, start):
    """
    Generate all routes from start where each point is one step higher than the previous
    """
    level = grid.get(start)
    if level == "9":
        yield [start]
    next_level = str(int(level)+1)
    for dir in Dir:
        step = start.move(dir)
        if grid.get(step) == next_level:     
            for route in explore(grid, step):
                yield [start]+route


def solve(data: list[str] | None = None) -> tuple[int, int]:
    grid = Grid.from_map(read_data(data=data))
    trailheads = grid.find_all("0")
    p1, p2 = 0, 0

    for trailhead in trailheads:
        trails = list(explore(grid, trailhead))
        p1 += len(set([trail[-1] for trail in trails]))
        p2 += len(trails)

    return p1, p2


def test_solve() -> None:
    assert solve() == (36, 0)
