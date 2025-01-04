"""Advent of Code: 2024 - Day 12."""

from __future__ import annotations
from aoc2024.grid import Dir, Grid, Point

from . import utils


def example() -> str:
    return """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def explore_region(start, grid, region, fences):
    region.add(start)
    crop = grid.get(start)
    for dir in Dir:
        neighbour = start.move(dir)
        if neighbour in region:
            continue
        crop_t = grid.get(neighbour)
        if crop_t == crop:
            explore_region(neighbour, grid, region, fences)
        else:
            fences.add((start, dir))
    
def count_sides(fences):
    count = 0
    while len(fences) > 0:
        start, edge = fences.pop()
        dir = edge.turn_right()
        count += 1
        for _ in range(2):
            f = start.move(dir)
            while (f, edge) in fences:
                fences.remove((f, edge))
                f = f.move(dir)
            dir = dir.turn_around()
    return count

def solve(data: list[str] | None = None) -> tuple[int, int]:
    grid = Grid.from_map(read_data(data=data))
    p1, p2 = 0, 0
    for y in range(grid.h):
        for x in range(grid.w):
            point = Point(x, y)
            if grid.get(point) != ".":
                region = set()
                fences = set()
                explore_region(point, grid, region, fences)
                for pt in region:
                    grid.set(pt, ".")
                c_fences = len(fences)
                sides = count_sides(fences)
                p1 += len(region)*c_fences
                p2 += len(region)*sides
    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
