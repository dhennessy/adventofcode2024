"""Advent of Code: 2024 - Day 13."""

from __future__ import annotations
import re
import z3
from . import utils


def example() -> str:
    return """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def cost(btns):
    return 3*btns[0] + btns[1]

def find_solutions(m):
    x = z3.Int("x")
    y = z3.Int("y")
    s = z3.Solver()
    s.add(x*m[0][0] + y*m[1][0] == m[2][0])
    s.add(x*m[0][1] + y*m[1][1] == m[2][1])
    answers = []
    while True:
        try:
            s.check()
            ans = s.model()
            ans_x, ans_y = int(str(ans[x])), int(str(ans[y])) 
            answers.append((ans_x, ans_y))
            s.add(x != ans_x)
        except z3.Z3Exception:
            break
    return answers  

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    machines = []
    for i in range(len(data)//4+1):
        pairs = []
        for j in range(3):
            numbers = [int(x) for x in re.findall(r'\d+', data[i*4+j])]
            pairs.append(numbers)
        machines.append(pairs)

    p1, p2 = 0, 0
    for m in machines:
        solutions = find_solutions(m)
        if len(solutions):
            best = sorted(solutions, key=cost)[0]
            p1 += cost(best)

    for m in machines:
        m_big = (m[0], m[1], (m[2][0]+10000000000000, m[2][1]+10000000000000))
        solutions = find_solutions(m_big)
        if len(solutions):
            best = sorted(solutions, key=cost)[0]
            p2 += cost(best)
    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
