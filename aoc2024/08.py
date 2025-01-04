"""Advent of Code: 2024 - Day 08."""

from __future__ import annotations

from aoc2024.grid import Dir, Grid, Point
from . import utils


def example() -> str:
    return """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def permute_antinodes(antennas: list[Point]):
    pt1 = antennas[0]
    if len(antennas) == 2:
        yield((pt1, antennas[1]))
        return
    for pt2 in antennas[1:]:
        yield((pt1, pt2))
    for pt1,pt2 in permute_antinodes(antennas[1:]): 
        yield((pt1, pt2))

def solve(data: list[str] | None = None) -> tuple[int, int]:
    grid = Grid.from_map(read_data(data=data))
    freqs = set([grid.get(Point(x, y)) for x in range(grid.w) for y in range(grid.h)])
    freqs.remove(".")
    p1, p2 = 0, 0

    antinodes = set()
    for freq in freqs:
        for pt1, pt2 in permute_antinodes(grid.find_all(freq)):
            dx = pt1.x-pt2.x
            dy = pt1.y-pt2.y
            for pt in [Point(pt1.x+dx, pt1.y+dy), Point(pt2.x-dx, pt2.y-dy)]:
                if pt.x>=0 and pt.x<grid.w and pt.y>=0 and pt.y<grid.h:
                    antinodes.add(pt)
    p1 = len(antinodes)

    antinodes = set()
    for freq in freqs:
        for pt1, pt2 in permute_antinodes(grid.find_all(freq)):
            antinodes.add(pt1)
            antinodes.add(pt2)
            dx = pt1.x-pt2.x
            dy = pt1.y-pt2.y
            for i in range(max(grid.w, grid.h)):
                pt = Point(pt1.x+dx*i, pt1.y+dy*i)
                if pt.x>=0 and pt.x<grid.w and pt.y>=0 and pt.y<grid.h:
                    antinodes.add(pt)
                else:
                    break
            for i in range(max(grid.w, grid.h)):
                pt = Point(pt2.x-dx*i, pt2.y-dy*i)
                if pt.x>=0 and pt.x<grid.w and pt.y>=0 and pt.y<grid.h:
                    antinodes.add(pt)
                else:
                    break
    p2 = len(antinodes)

    return p1, p2


def test_solve() -> None:
    assert solve() == (14, 0)
