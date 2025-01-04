"""Advent of Code: 2024 - Day 17."""

from __future__ import annotations
from . import utils


def example2() -> str:
    return """
Register A: 117440
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
def example1() -> str:
    return """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

class Device:
    def __init__(self, a, b, c, program):
        self.a = a
        self.b = b
        self.c = c
        self.program = program
        self.ip = 0
        self.output = []

    def inst(self):
        combo = ["0", "1", "2", "3", "A", "B", "C"][self.program[self.ip+1]]
        match self.program[self.ip]:
            case 0:
                return f"adv {combo}"
            case 1:
                return f"bxl {self.program[self.ip+1]}"
            case 2:
                return f"bst {combo}"
            case 3:
                return f"jnz {self.program[self.ip+1]}"
            case 4:
                return f"bxc"
            case 5:
                return f"out {combo}"
            case 6:
                return f"bdv {combo}"
            case 7:
                return f"cdv {combo}"
        
    def __str__(self):
        return f"[IP:{self.ip}, A:{self.a:o}, B:{self.b:o}, C:{self.c:o}]"
    
    def combo(self):
        operand = self.program[self.ip+1]
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
        print(f"ILLEGAL OPERAND: {self.ip}: {self.program[self.ip]} {self.program[self.ip+1]}")

    def step(self):
        initial = str(self)
        inst = self.inst()
        next_ip = self.ip + 2
        match self.program[self.ip]:
            case 0: # adv
                self.a = self.a // (1 << self.combo())
            case 1: # bxl
                self.b ^= self.program[self.ip+1]
            case 2: #bst
                self.b = self.combo() & 7
            case 3: #jnz
                if self.a != 0:
                    next_ip = self.program[self.ip+1]
            case 4: # bxc
                self.b = self.b ^ self.c
            case 5: # out
                self.output.append(self.combo() & 7)
            case 6: # bdv
                self.b = self.a // (1 << self.combo())
            case 7: # cdv
                self.c = self.a // (1 << self.combo())
        self.ip = next_ip
        final = str(self)
        # print(f"{initial} {inst} -> {final}: {self.output}")

    def run(self):
        self.output = []
        self.ip = 0
        while self.ip < len(self.program):
            self.step()


def read_data(data: list[str] | None = None) -> list[int]:
    return data or utils.read_example(example2())

def find_a(device, digits):
    if digits == 0:
        yield 0
        return
    for a_lhs in find_a(device, digits-1):
        for i in range(8):
            a = (a_lhs << 3) + i
            device.a = a
            device.run()
            if device.program[-digits:] == device.output[-digits:]:
                yield a

def solve(data: list[str] | None = None) -> tuple[int, int]:
    data = read_data(data=data)
    a = int(data[0][12:])
    b = int(data[1][12:])
    c = int(data[2][12:])
    program = [int(x) for x in data[4][9:].split(",")]

    device = Device(a, b, c, program)
    device.run()
    p1 = ",".join([str(i) for i in device.output])

    p2 = min(find_a(device, len(device.program)))

    # device.a = p2
    # device.run()
    # print(f"Solution: {p2:o}")
    # print(f"Program: {device.program}")
    # print(f"Output:  {device.output}")
    # print(f"Found answer: {device.program == device.output}")

    return p1, p2

def test_solve() -> None:
    assert solve() == (0, 0)
