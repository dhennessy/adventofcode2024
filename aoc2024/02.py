"""Advent of Code: 2024 - Day 02."""

from __future__ import annotations

from . import utils


def example() -> str:
    return """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def is_safe(levels):
    increasing = False
    decreasing = False
    for i in range(1, len(levels)):
        l0 = levels[i-1]
        l1 = levels[i]
        if l0 == l1:
            return False
        if l1 < l0:
            decreasing = True
        if l1 > l0:
            increasing = True
        if abs(l1-l0) > 3:
            return False
    if increasing and decreasing:
        return False
    return True
        
def is_potentially_safe(levels):
    if is_safe(levels):
        return True
    for i in range(len(levels)):
        lt = levels[:i] + levels[i+1 :]
        if is_safe(lt):
            return True
    
def solve1(input):
    lines = input.splitlines()
    count = 0
    for line in lines:
        levels = [int(v) for v in line.split()]
        if is_safe(levels):
            count += 1
    return count
        
def solve2(input):
    lines = input.splitlines()
    count = 0
    for line in lines:
        levels = [int(v) for v in line.split()]
        if is_potentially_safe(levels):
            count += 1
    return count
        

def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    p1, p2 = 0, 0

    for line in data:
        levels = [int(v) for v in line.split()]
        if is_safe(levels):
            p1 += 1

    for line in data:
        levels = [int(v) for v in line.split()]
        if is_potentially_safe(levels):
            p2 += 1

    return p1, p2


def test_solve() -> None:
    assert solve() == (2, 4)
