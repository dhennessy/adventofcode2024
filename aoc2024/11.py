"""Advent of Code: 2024 - Day 11."""

from __future__ import annotations
import functools
from . import utils


def example() -> str:
    return """
125 17
"""


def read_data(data: list[str] | None = None) -> tuple[list[int], list[int]]:
    return data or utils.read_example(example())

@functools.lru_cache(maxsize=100000)
def derive_len(stone, blinks):
    if blinks == 0:
        return 1
    if stone == "0":
        return derive_len("1", blinks-1)
    elif len(stone) % 2 == 0:
        mid = len(stone) // 2
        return derive_len(stone[:mid], blinks-1) + derive_len(str(int(stone[mid:])), blinks-1)
    else:
        return derive_len(str(int(stone)*2024), blinks-1)

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)[0]
    p1, p2 = 0, 0

    stones = data.split()
    for stone in stones:
        p1 += derive_len(stone, 25)
        p2 += derive_len(stone, 75)
    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
