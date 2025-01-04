"""Advent of Code: 2024 - Day 14."""

from __future__ import annotations
import re
from functools import reduce
from operator import mul
from aoc2024.grid import Dir, Grid, Point
from . import utils


def example() -> str:
    return """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def move_robot(pt, vel, count, width, height) -> Point:
    return Point((pt.x + vel.x*count) % width, (pt.y + vel.y*count) % height)

def quadrant(pt, width, height) -> int:
    midx, midy = width // 2, height // 2
    if pt.x < midx and pt.y < midy:
        return 0
    if pt.x > midx and pt.y < midy:
        return 1
    if pt.x < midx and pt.y > midy:
        return 2
    if pt.x > midx and pt.y > midy:
        return 3
    return -1
    
def draw_tree(positions, width, height):
    grid = Grid(width, height)
    for pt in [Point(x, y) for x in range(width) for y in range(height)]:
        grid.set(pt, ".")
    for pt in positions:
        grid.set(pt, "*")
    print(f"Tree:\n{grid.draw()}")

def solve(data: list[str] | None = None) -> tuple[int, int]:
    width, height = (11, 7) if data is None else (101, 103)
    data = read_data(data=data)
    robots = []
    for line in data:
        v = list(re.findall(r"(-?\d+)", line))
        robots.append((Point(int(v[0]), int(v[1])), Point(int(v[2]), int(v[3]))))
    p1, p2 = 0, 0

    positions = [move_robot(robot[0], robot[1], 100, width, height) for robot in robots]
    q = [quadrant(pt, width, height) for pt in positions]
    counts = [q.count(x) for x in range(4)]
    p1 = reduce(mul, counts)

    for i in range(1, 10000):
        positions = [move_robot(robot[0], robot[1], i, width, height) for robot in robots]
        if len(set(positions)) == len(positions):
            print(f"Possible tree at iteration {i}")
            draw_tree(positions, width, height)
            p2 = i
            break

    return p1, p2

def test_solve() -> None:
    assert solve() == (0, 0)
