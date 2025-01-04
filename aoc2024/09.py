"""Advent of Code: 2024 - Day 09."""

from __future__ import annotations

from . import utils


def example() -> str:
    return "2333133121414131402"


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())


def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)[0]
    p1, p2 = 0, 0

    files = []
    free_space = []
    blocks = []
    block = 0
    in_file = True
    for c in data:
        count = int(c)
        if in_file:
            blocks.extend([len(files)]*count)
            files.append((block, count))
            in_file = False
        else:
            blocks.extend([-1]*count)
            free_space.append((block, count))
            in_file = True
        block += count

    start_search = 0
    for i in range(block-1, -1, -1):
        if blocks[i] != -1:
            j = blocks.index(-1, start_search)
            if j < i:
                blocks[j],blocks[i] = blocks[i], -1
                start_search = j + 1
    p1 = sum([i*blocks[i] for i in range(block) if blocks[i] != -1])

    for id in range(len(files)-1, -1, -1):
        file_block, file_size = files[id]
        for free_idx, (block, size) in enumerate(free_space):
            if size >= file_size and block < file_block:
                files[id] = (block, file_size)
                free_space[free_idx] = (block+file_size, size-file_size)
                break
    for id, (block, size) in enumerate(files):
        for i in range(size):
            p2 += id*(block+i)


    return p1, p2


def test_solve() -> None:
    assert solve() == (1928, 0)
