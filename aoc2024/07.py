"""Advent of Code: 2024 - Day 07."""

from __future__ import annotations

from . import utils


def example() -> str:
    return """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def permute_list2(numbers: list[int]):
    last = numbers[-1]
    if len(numbers) == 1:
        yield last
    else:
        for n in permute_list2(numbers[:-1]):
            yield last + n
            yield last * n

def permute_list3(numbers: list[int]):
    last = numbers[-1]
    if len(numbers) == 1:
        yield last
    else:
        for n in permute_list3(numbers[:-1]):
            yield last + n
            yield last * n
            yield int(f"{n}{last}")

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    input: tuple[int, list[int]] = []
    for l in data:
        e = l.split(": ")
        total = int(e[0])
        vals = [int(v) for v in e[1].split()]
        input.append((total, vals))
    p1, p2 = 0, 0

    for total, vals in input:
        for v in permute_list2(vals):
            if v == total:
                p1 += total
                break
        for v in permute_list3(vals):
            if v == total:
                p2 += total
                break

    return p1, p2


def test_solve() -> None:
    assert solve() == (3749, 11387)
