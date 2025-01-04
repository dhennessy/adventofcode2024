"""Advent of Code: 2024 - Day 21."""

from __future__ import annotations
from aoc2024.grid import Dir, Grid, Point
import itertools
import functools

from . import utils


def example() -> str:
    return """
029A
980A
179A
456A
379A
"""


digit_keypad = Grid.from_map(["789", "456", "123", ".0A"])
move_keypad = Grid.from_map([".^A", "<v>"])


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())


@functools.lru_cache(maxsize=100000)
def find_move(grid, start, end) -> str:
    dx, dy = end.x - start.x, end.y - start.y
    v, h = "v" * dy + "^" * -dy, ">" * dx + "<" * -dx
    if dx > 0 and grid.get(Point(start.x, end.y)) != ".":
        return v + h + "A"
    elif grid.get(Point(end.x, start.y)) != ".":
        return h + v + "A"
    else:
        return v + h + "A"


@functools.lru_cache(maxsize=100000)
def expand(code, grid, initial, levels):
    move = ""
    for c in code:
        pt = grid.find(c)
        move += find_move(grid, initial, pt)
        initial = pt
    if levels == 0:
        return move
    else:
        return expand(move, move_keypad, move_keypad.find("A"), levels - 1)


numeric = {
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "0": (1, 3),
    "A": (2, 3),
}

directional = {"^": (1, 0), "A": (2, 0), "<": (0, 1), "v": (1, 1), ">": (2, 1)}


def is_valid(line, px, py, gapx, gapy):
    d = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}
    for c in line:
        if c == "A":
            continue
        dx, dy = d[c]
        py += dy
        px += dx
        if px == gapx and py == gapy:
            return False
    return True


@functools.cache
def move_actuator(px, py, nx, ny, max_depth, depth):
    # print(f"move_actuator {px,py=} {nx,ny=}, {depth=}")
    dx, dy = nx - px, ny - py
    best = []
    for perm in itertools.permutations(range(4)):
        ans = []
        for p in perm:
            if p == 0:
                if dx > 0:
                    ans.extend([">"] * abs(dx))
            if p == 1:
                if dy > 0:
                    ans.extend(["v"] * abs(dy))
            if p == 2:
                if dx < 0:
                    ans.extend(["<"] * abs(dx))
            if p == 3:
                if dy < 0:
                    ans.extend(["^"] * abs(dy))
        ans.append("A")
        ans = "".join(ans)
        # print(f"{perm=} {dx,dy=} {ans=}")
        gapx, gapy = (0, 0) if depth >= 0 else (0, 3)
        if is_valid(ans, px, py, gapx, gapy):
            best.append(enter_code(ans, max_depth, depth + 1))
        # else:
        #     print(f"invalid: {ans} {px, py, nx, ny, gapy, gapx=}")
    # print(f"{px,py=} {nx,ny=}, {depth=} -> {len(best)}")
    return min(best)


def enter_code(code, max_depth, depth) -> int:
    """Return number of keys needed to enter code, using robots as needed."""
    # print(f"enter_code {code}, {depth=}")
    if depth == max_depth:
        return len(code)
    table = directional if depth >= 0 else numeric
    px, py = table["A"]
    size = 0
    for c in code:
        nx, ny = table[c]
        size += move_actuator(px, py, nx, ny, max_depth, depth)
        px, py = nx, ny
    return size


def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = [l.strip() for l in read_data(data=data)]
    p1, p2 = 0, 0

    for code in data:
        print(code)
        n = enter_code(code, 2, -1)
        p1 += int(code[:3]) * n

        n = enter_code(code, 25, -1)
        p2 += int(code[:3]) * n
        # val = int(code[:-1])
        # p1 += val * len(expand(code, digit_keypad, digit_keypad.find("A"), 2))
        # p2 += val * len(expand(code, digit_keypad, digit_keypad.find("A"), 25))

    return p1, p2


# p1 243602 too high
# p1 241274 too high


def test_solve() -> None:
    assert solve() == (0, 0)
