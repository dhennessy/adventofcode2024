"""Advent of Code: 2024 - Day 18."""

from __future__ import annotations
from aoc2024.grid import Dir, Grid, Point

from . import utils


def example() -> str:
    return """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())


def find_route(cost, end, grid, costs):
    for pt in costs.all_points():
        if costs.get(pt) is not None and costs.get(pt) > cost:
            costs.set(pt, None)
    while costs.get(end) is None:
        next_wave = costs.find_all(cost)
        if len(next_wave) == 0:
            return None
        for start in costs.find_all(cost):
            for pt in [start.move(dir) for dir in Dir]:
                if grid.get(pt) == "." and costs.get(pt) is None:
                        costs.set(pt, cost+1)
        cost += 1
    return costs.get(end)

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    blocks = []
    for line in data:
        vals = line.split(",")
        blocks.append(Point(int(vals[0]), int(vals[1])))
    dim = 7 if len(blocks) == 25 else 71

    grid = Grid(dim, dim, ".")
    end = Point(grid.w-1, grid.h-1)
    costs = Grid(grid.w, grid.h)
    costs.set(Point(0,0), 0)
    fill_cnt = 12 if len(blocks) == 25 else 1024
    for b in blocks[:fill_cnt]:
        grid.set(b, "#")
    p1 = find_route(0, end, grid, costs)

    grid = Grid(dim, dim, ".")
    costs.set(Point(0,0), 0)
    p2 = None
    for pt in blocks:
        grid.set(pt, "#")
        cost = costs.get(pt)        
        costs.set(pt, None)
        if cost is not None and find_route(cost, end, grid, costs) is None:
            p2 = f"{pt.x},{pt.y}"
            break

    return p1, p2

def test_solve() -> None:
    assert solve() == (0, 0)
