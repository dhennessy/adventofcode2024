"""Advent of Code: 2024 - Day 24."""

from __future__ import annotations
from itertools import combinations
import random
from . import utils


def example() -> str:
    return """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

gates = {}
inputs = {}
z_len = 0

def read_data(data: list[str] | None = None) -> list[str]:
    return data or utils.read_example(example())

def resolve(wire):
    if wire in inputs:
        return inputs[wire]
    gate = gates[wire]
    a = resolve(gate[0])
    b = resolve(gate[2])
    match gate[1]:
        case "AND":
            return a & b
        case "OR":
            return a | b
        case "XOR":
            return a != b

def find_swap_gate(nbr_dependents):
    """ Find a XOR gate with this number of dependents """
    for wire, gate in gates.items():
        if gate[1] == "XOR": 
            dependents = dependents_of_wire(wire)
            if len(dependents) == nbr_dependents:
                return wire

def swap_gates(a, b):
    gates[a], gates[b] = gates[b], gates[a]

def dependents_of_wire(wire):
    """ Dependents are all the inputs that lead to this output wire """
    if wire in inputs:
        return set()
    gate = gates[wire]
    return set([gate[0], gate[2]]).union(dependents_of_wire(gate[0])).union(dependents_of_wire(gate[2]))

def find_z_anomalies():
    """
    Find z wire output gates that don't look right.
    Expected number of dependents (increases by 6 for each z wire) came
    from observation of listing # of dependents of each z wire.
    """
    swapped_outputs = []
    for z in range(z_len-1):
        wire = f"z{z:02}"
        gate = gates[wire]
        if gate[1] == "XOR": 
            continue
        print()
        print(f"Bad gate: {wire}: {gate}")
        expected_nbr_dependents = z * 6
        swap = find_swap_gate(expected_nbr_dependents)
        print(f"Swap with: {swap}")
        swapped_outputs.extend((wire, swap))
        swap_gates(wire, swap)

    return swapped_outputs

def find_last_pair(test_data, swapped_outputs):
    """ Test all combinations of gates, skipping those that output to z """
    print()
    print('Testing other combinations of gates...')

    # Create list of outputs to swap, without z wires, not including already swapped
    # Note: Not using a set because then you don't get repeatable results
    outputs = [output for output in gates.keys() if output[:1] != 'z' and output not in swapped_outputs]
    outputs.sort()

    tested = 0

    for out1, out2 in combinations(outputs, 2):
        # print(f"Try {out1}, {out2}")
        # if out2 in dependents_of_wire(out1):
        #     print(f"{out2} in dependencies of {out1}")
        # if out1 in dependents_of_wire(out2):
        #     print(f"{out1} in dependencies of {out2}")
        tested += 1 
        # g1_gate = gates[out1]
        # g2_gate = gates[out2]

        if out1 in dependents_of_wire(out2) or out2 in dependents_of_wire(out1):
            continue
        # if out1 == g2_gate[0] or out1 == g2_gate[2] or out2 == g1_gate[0] or out2 == g1_gate[2]:
        # if out1 in g2_gate or out2 in g1_gate:
        #     asafsdf
        #     continue
        # # if g1_gate['out'] in g2_gate['in']: continue    # would cause cycle
        # if g2_gate['out'] in g1_gate['in']: continue
                   
        swap_gates(out1, out2)

        for (x, y) in test_data:
            worked = run_test(x, y)
            if not worked: 
                break

        if worked:
            print()
            print('Tested', tested, 'combinations')
            print(f"Found a pair that works! - {out1}, {out2}")
            swapped_outputs.extend((out1, out2))
            return True

        swap_gates(out1, out2)

    print('No pair found')
    return False

def run_test(x, y):
    correct = x + y
    inputs.clear()       # very important!
    set_wires(inputs, 'x', x)
    set_wires(inputs, 'y', y)
    output = run_sim()
    result = correct == output
    return result

def set_wires(wires, w, value):
    if w == 'z':
        w_len = z_len
    else:
        w_len = z_len - 1
    for n in range(w_len):
        wire = f'{w}{n:02}'
        bit = value % 2
        wires[wire] = bit
        value //= 2
    return

def run_sim():
    val = 0
    for bit in range(z_len):
        val = val | (resolve(f"z{bit:02}") << bit)
    return val

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    p1, p2 = 0, 0
    for line in data:
        if len(line) > 4:
            if line[3] == ":":
                inputs[line[:3]] = int(line[5])
            else:
                elems = line.strip().split(" ")
                gates[elems[4]] = elems[:3]
    global z_len
    z_len = max([int(wire[1:]) for wire in gates if wire.startswith("z")]) + 1

    p1 = run_sim()

    swapped_outputs = find_z_anomalies()

    # Note: If doesn't work for input, increase number of randomly generated x,y pairs
    test_data = [(28872341726885, 28414614475596)]   # this pair finds answer in one test
    random.seed(2024)
    maxval = (1 << (z_len-2)) - 1
    test_data = [(random.randrange(maxval), random.randrange(maxval)) for _ in range(100)]
    find_last_pair(test_data, swapped_outputs)

    p2 = ",".join(sorted(swapped_outputs))
    return p1, p2


def test_solve() -> None:
    assert solve() == (0, 0)
