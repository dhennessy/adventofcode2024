"""Advent of Code: 2024 - Day 15."""

from __future__ import annotations
from aoc2024.grid import Dir, Grid, Point
from . import utils


def example() -> str:
    return """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
def example2() -> str:
    return """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""
def example1() -> str:
    return """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def can_move(pt, dir, grid):
    pt_next = pt.move(dir)
    t = grid.get(pt_next)
    match t:
        case ".":
            return True
        case "#":
            return False
        case "O":
            return can_move(pt_next, dir, grid)
        case "[":
            match dir:
                case Dir.N | Dir.S:
                    return can_move(pt_next, dir, grid) and can_move(pt_next.move(Dir.E), dir, grid)
                case Dir.E:
                    return can_move(pt_next.move(Dir.E), dir, grid)
        case "]":
            match dir:
                case Dir.N | Dir.S:
                    return can_move(pt_next, dir, grid) and can_move(pt_next.move(Dir.W), dir, grid)
                case Dir.W:
                    return can_move(pt_next.move(Dir.W), dir, grid)

def move(pt, dir, grid):
    s = grid.get(pt)
    pt_next = pt.move(dir)
    t = grid.get(pt_next)
    if t == 'O':
        move(pt_next, dir, grid)
    elif t == "[":
        match dir:
            case Dir.N | Dir.S:
                move(pt_next, dir, grid)
                move(pt_next.move(Dir.E), dir, grid)
            case Dir.E:
                move(pt_next.move(Dir.E), dir, grid)
                grid.set(pt_next.move(Dir.E), t)
    elif t == "]":
        match dir:
            case Dir.N | Dir.S:
                move(pt_next, dir, grid)
                move(pt_next.move(Dir.W), dir, grid)
            case Dir.W:
                move(pt_next.move(Dir.W), dir, grid)
                grid.set(pt_next.move(Dir.W), t)
    grid.set(pt_next, s)
    grid.set(pt, ".")
        
def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = [line.strip() for line in read_data(data=data)]
    sep = data.index("")
    grid = Grid.from_map(data[:sep])
    steps = [Dir.from_sym(sym) for sym in "".join(data[(sep+1):])]
    p1, p2 = 0, 0

    for dir in steps:
        robot = grid.find("@")
        if can_move(robot, dir, grid):
            move(robot, dir, grid)
    p1 = sum([pt.y*100 + pt.x for pt in grid.find_all("O")])

    grid = Grid.from_map(data[:sep])
    wgrid = Grid(grid.w*2, grid.h)
    for pt in [Point(x, y) for x in range(wgrid.w) for y in range(wgrid.h)]:
        wgrid.set(pt, ".")
    pt = grid.find("@")
    wgrid.set(Point(pt.x*2, pt.y), "@")
    for pt in grid.find_all("O"):
        wgrid.set(Point(pt.x*2, pt.y), "[")
        wgrid.set(Point(pt.x*2+1, pt.y), "]")
    for pt in grid.find_all("#"):
        wgrid.set(Point(pt.x*2, pt.y), "#")
        wgrid.set(Point(pt.x*2+1, pt.y), "#")

    for dir in steps:
        robot = wgrid.find("@")
        if can_move(robot, dir, wgrid):
            move(robot, dir, wgrid)
    p2 = sum([pt.y*100 + pt.x for pt in wgrid.find_all("[")])

    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
