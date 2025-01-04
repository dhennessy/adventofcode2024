"""Advent of Code: 2024 - Day 22."""

from __future__ import annotations

from . import utils


def example() -> str:
    return """
1
2
3
2024
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def evolve(n, times):
    answers = []
    i1, i2, i3, i4 = None, None, None, None
    answers.append((n, n % 10, (i1, i2, i3, i4)))
    last_price = n % 10
    for _ in range(times):
        n = ((n * 64) ^ n) % 16777216
        n = ((n // 32) ^ n) % 16777216
        n = ((n * 2048) ^ n) % 16777216
        price = n % 10   
        i1, i2, i3 = i2, i3, i4
        i4 = price - last_price     
        answers.append((n, price, (i1, i2, i3, i4)))
        last_price = price
    return answers

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    secrets = [int(n) for n in data]
    p1, p2 = 0, 0

    buyers = []
    seqs = set()
    for secret in secrets:
        prices = {}
        ans = evolve(secret, 2000)
        p1 += ans[2000][0]
        for (_, price, seq) in ans:
            if seq not in prices and seq[0] is not None:
                prices[seq] = price
                seqs.add(seq)
        buyers.append(prices)
    print(f"Found {len(seqs)} sequences")
    for seq in seqs:
        count = 0
        for buyer in buyers:
            try:
                count += buyer[seq]
            except KeyError:
                pass
        if count > p2:
            p2 = count
            print(f"Improve count to {p2} with {seq}")
    return p1, p2

def test_solve() -> None:
    assert solve() == (0, 0)
