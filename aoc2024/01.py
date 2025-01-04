"""Advent of Code: 2024 - Day 01."""

from __future__ import annotations

from . import utils


def example() -> str:
    return """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())


def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    left = sorted([int(line.split()[0]) for line in data])
    right = sorted([int(line.split()[1]) for line in data])
    diffs = [abs(a - b) for a,b in zip(left, right)]
    p1 = sum(diffs)
    
    sim = [right.count(a)*a for a in left]
    p2 = sum(sim)
    return p1, p2


def test_solve() -> None:
    assert solve() == (11, 31)
