"""Advent of Code: 2024 - Day 20."""

from __future__ import annotations
from aoc2024.grid import Dir, Grid, Point

from . import utils


def example() -> str:
    return """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def compute_costs(end, grid, costs):
    cost = 0
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

def find_cheats(grid, costs, min_saving, cheat_len):
    cheat_range = []
    for dx in range(cheat_len+1):
        for dy in range(cheat_len+1):
            dist = dx+dy
            if dist <= cheat_len and dist != 0:
                cheat_range.extend([(dx, dy, dist), (-dx, dy, dist), (-dx, -dy, dist), (dx, -dy, dist)])
    cheat_range = list(set(cheat_range))
    cheats = set()
    for pt in grid.find_all("."):
        for dxdy in cheat_range:
            jump = pt.move(dxdy)
            if (pt, jump) not in cheats:
                if costs.get(jump) != None:
                    saving = costs.get(jump) - dxdy[2] - costs.get(pt)
                    if saving >= min_saving:
                        cheats.add((pt, jump))
    return len(cheats)

def solve(data: list[str] | None = None) -> tuple[int, int]:    
    data = read_data(data=data)
    grid = Grid.from_map(data)
    start, end = grid.find("S"), grid.find("E")
    grid.set(start, ".")
    grid.set(end, ".")
    p1, p2 = 0, 0

    costs = Grid(grid.w, grid.h)
    costs.set(start, 0)
    compute_costs(end, grid, costs)
    if grid.w == 15:  # Example
        p1 = find_cheats(grid, costs, 1, 2)
        p2 = find_cheats(grid, costs, 72, 20)
    else:
        p1 = find_cheats(grid, costs, 100, 2)
        p2 = find_cheats(grid, costs, 100, 20)

    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
