"""Advent of Code: 2024 - Day 05."""

from __future__ import annotations

from . import utils


def example() -> str:
    return """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def read_data(data: list[str] | None = None) -> tuple[list[tuple[int, int]], list[list[int]]]:
    data = data or utils.read_example(example())
    ordering: list[tuple[int, int]] = []
    updates: list[list[int]] = []
    for line in data:
        if len(line) > 4:
            if line[2] == "|":
                ordering.append((int(line[:2]), int(line[3:])))
            else:
                updates.append([int(x) for x in line.split(",")])
    return ordering, updates


def solve(data: list[str] | None = None) -> tuple[int, int]:
    ordering, updates = read_data(data=data)
    p1, p2 = 0, 0

    for update in updates:
        is_ok = True
        for i in range(len(update)):
            for j in range(i+1, len(update)):
                for order in ordering:
                    if update[i] == order[1] and update[j] == order[0]:
                        is_ok = False
                        update[i], update[j] = update[j], update[i]
        if is_ok:
            p1 += update[len(update)//2]
        else:
            p2 += update[len(update)//2]
    return p1, p2


def test_solve() -> None:
    assert solve() == (143, 123)
