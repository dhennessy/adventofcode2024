"""Advent of Code: 2024 - Day 04."""

from __future__ import annotations

from . import utils


def example() -> str:
    return """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def read_data(data: list[str] | None = None) -> list[int]:
    return data or utils.read_example(example())

DIRS = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]

def get_char(x: int, y: int, grid: list[str], w: int, h: int) -> str | None:
    if x<0 or x>=w or y<0 or y>=h:
        return None
    return grid[y][x]

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    w = len(data[0].strip())
    h = len(data)

    p1 = 0
    centers = []
    for dir in DIRS:
        for x in range(w):
            for y in range(h):
                if get_char(x, y, data, w, h) == "X" \
                   and get_char(x+dir[0], y+dir[1], data, w, h) == "M" \
                   and get_char(x+dir[0]*2, y+dir[1]*2, data, w, h) == "A" \
                   and get_char(x+dir[0]*3, y+dir[1]*3, data, w, h) == "S":
                    p1 += 1

    centers = []
    for dir in [DIRS[1], DIRS[3], DIRS[5], DIRS[7]]:
        for x in range(w):
            for y in range(h):
                if get_char(x, y, data, w, h) == "M" \
                   and get_char(x+dir[0], y+dir[1], data, w, h) == "A" \
                   and get_char(x+dir[0]*2, y+dir[1]*2, data, w, h) == "S":
                    centers.append((x+dir[0], y+dir[1]))

    p2 = 0
    for i in range(len(centers)):
        for j in range(i+1, len(centers)):
            if centers[i] == centers[j]:
                p2 += 1

    return p1, p2


def test_solve() -> None:
    assert solve() == (18, 9)
