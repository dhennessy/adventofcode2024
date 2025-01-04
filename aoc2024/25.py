"""Advent of Code: 2024 - Day 25."""

from __future__ import annotations

from . import utils


def example() -> str:
    return """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return [l.strip() for l in data or utils.read_example(example())]


def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    p1, p2 = 0, 0

    keys = []
    locks = []
    for i in range(0, len(data), 8):
        heights = []
        for j in range(5):
            h = 0
            for k in range(5):
                if data[i+k+1][j] == "#":
                    h += 1
            heights.append(h)
        if data[i] == "#####":
            locks.append(heights)
        else:
            keys.append(heights)
    # print(f"Locks:\n{locks}")
    # print(f"Keys:\n{keys}")

    for l in locks:
        for k in keys:
            fit = True
            for p in range(5):
                if l[p]+k[p] > 5:
                    fit = False
            # print(f"Lock {l}, Key {k}: {fit}")
            if fit:
                p1 += 1

    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
