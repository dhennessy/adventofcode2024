"""Advent of Code: 2024 - Day 23."""

from __future__ import annotations

from . import utils


def example() -> str:
    return """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())


def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = [line.strip() for line in read_data(data=data)]
    connections = {}
    for line in data:
        a, b = str(line[:2]), str(line[3:])
        for _ in [1, 2]:
            if a in connections:
                connections[a].add(b)
            else:
                connections[a] = set([b])
            a, b = b, a
    computers = sorted(connections.keys())
    max_group = max([len(connections[c]) for c in computers])
    print(f"{len(computers)} computers, {len(list(connections))} connections, max_group: {max_group}")
    p1, p2 = 0, 0

    groups = set(computers)
    max_found = 0
    p2 = ""
    for len_group in range(max_group):
        print(f"{len_group} / {max_group}: groups: {len(groups)}, p2: {p2}")
        for c in computers:
            neighbours = connections[c]
            for g in [g for g in groups if c not in g and len(g) == 3*len_group-1]:
                if all(cg in neighbours for cg in g.split(",")):
                    g_new = g.split(",")
                    g_new.append(c)
                    group = ",".join(sorted(g_new))
                    if len(group) > max_found:
                        max_found = len(group)
                        p2 = group
                    groups.add(group)
                    # print(f"{len_group} {c}: Add {group}")
    max_group = max([len(g) for g in groups])
    # print(f"Groups: {groups}, max: {max_group}")

    print(f"Groups: {len(groups)}")
    for g in groups:
        if len(g) == 8 and (g.startswith("t") or ",t" in g):
            p1 += 1

    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
