"""Advent of Code: 2024 - Day 16."""

from __future__ import annotations
from astar import AStar
from dataclasses import dataclass

from aoc2024.grid import Dir, Grid, Point
from . import utils


def example() -> str:
    return """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
def example1() -> str:
    return """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example1())

@dataclass(unsafe_hash=True)
class Node:
    pt: Point
    dir: Dir | None

class ReindeerMaze(AStar):
    def __init__(self, grid):
        self.grid = grid

    def neighbors(self, n):
        for dir in Dir:
            pt = n.pt.move(dir)
            if self.grid.get(pt) == ".":
                yield Node(pt, dir)

    def distance_between(self, n1, n2):
        if n1.pt.move(n1.dir) == n2.pt:
            return 1
        else:
            return 1001
            
    def heuristic_cost_estimate(self, current, goal):
        dist = current.pt.manhattan_dist(goal.pt)
        if current.pt.dir_to(goal.pt) == current.dir:
            return dist
        else:
            return dist + 1000
    
    def is_goal_reached(self, current, goal):
        return current.pt == goal.pt

def cost(path):
    cost = len(path) - 1
    for i in range(1, cost):
        if path[i-1].dir != path[i].dir and path[i].dir is not None:
            cost += 1000
    return cost

# def all_solutions(grid, start, end):
#     maze = ReindeerMaze(grid)
#     path = list(maze.astar(start, end))
#     benchmark = cost(path)
#     yield path
#     if len(path) == 1:
#         return
#     dir = path[1].dir
#     left = dir.turn_left()
#     pt_left = start.pt.move(left)
#     if grid.get(pt_left) == ".":
#         path_left 
#     for dir in Dir:
#         alt_start = Node(start.pt.move(dir), dir)

        # if dir != path[0].dir:

def mark_route(grid, start, end, marks, starts):
    maze = ReindeerMaze(grid)
    path = list(maze.astar(start, end))

    best_cost = cost(path)
    for dir in Dir:
        pt = start.pt.move(dir)
        if grid.get(pt) == "." and pt != path[0].pt:
            alt_start = Node(pt, dir)
            if alt_start not in starts:
                starts.add(alt_start)
                p = maze.astar(alt_start, end)
                if p is not None:
                    alt_path = list(p)
                    if cost(path[:1]+alt_path) == best_cost:
                        mark_route(grid, alt_start, end, marks, starts)
    for n in path:
        marks.add(n.pt)

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    grid = Grid.from_map(data)
    p1, p2 = 0, 0

    start = Node(grid.find("S"), Dir.E)
    end = Node(grid.find("E"), None)
    grid.set(end.pt, ".")
    maze = ReindeerMaze(grid)
    path = list(maze.astar(start, end))
    p1 = cost(path)
    # for n in path:
    #     grid.set(n.pt, n.dir.sym())
    # print(f"P1 route:\n{grid.draw()}")

    grid = Grid.from_map(data)
    grid.set(end.pt, ".")
    marks = set()
    mark_route(grid, start, end, marks, set())
    p2 = len(marks)

    # for pt in marks:
    #     grid.set(pt, "O")
    # print(f"Final route:\n{grid.draw()}")
    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
