"""Advent of Code: 2024 - Day 03."""

from __future__ import annotations
import re

from . import utils


def example() -> str:
    return """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
# xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))


def read_data(data: list[str] | None = None) -> str:
    if data is None:
        return example().strip()
    else:
        return "".join(data)


def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    p1, p2 = 0, 0

    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    for match in pattern.finditer(data):
        p1 += int(match.group(1)) * int(match.group(2))

    is_enabled = True
    pattern = re.compile(r"do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\)")
    for match in pattern.finditer(data):
        str = data[match.start():]
        if str.startswith("don't"):
            is_enabled = False
        elif str.startswith("do"):
            is_enabled = True
        elif is_enabled:
            p2 += int(match.group(1)) * int(match.group(2))

    return p1, p2


def test_solve() -> None:
    assert solve() == (161, 48)
