"""Advent of Code: 2024 - Day 19."""

from __future__ import annotations
import functools

from . import utils


def example() -> str:
    return """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

def read_data(data: list[str] | None = None) -> list[str]:
    return [line.strip() for line in data or utils.read_example(example())]

patterns = []

@functools.lru_cache(maxsize=100000)
def search(start, end):
    matches = 0
    for pattern in patterns:
        next = start + pattern
        if next == end:
            matches += 1
        elif end.startswith(next):
            matches += search(next, end)
    return matches

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    global patterns
    patterns = data[0].split(", ")

    p1, p2 = 0, 0
    for design in data[2:]:
        solutions = search("", design)
        p1 += 1 if solutions > 0 else 0
        p2 += solutions

    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
