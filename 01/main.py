SAMPLE="""3   4
4   3
2   5
1   3
3   9
3   3"""

def solve1(input: str):
    lines = input.splitlines()
    left = sorted([int(line.split()[0]) for line in lines])
    right = sorted([int(line.split()[1]) for line in lines])
    diffs = [abs(a - b) for a,b in zip(left, right)]
    return sum(diffs)

def solve2(input: str):
    lines = input.splitlines()
    left = sorted([int(line.split()[0]) for line in lines])
    right = sorted([int(line.split()[1]) for line in lines])
    sim = [right.count(a)*a for a in left]
    return sum(sim)

with open("input", "r") as f:
    input = f.read()
    print(f"Answer 1: {solve1(input)}")
    print(f"Answer 2: {solve2(input)}")
    
# print(f"Sample: {solve2(SAMPLE)}")

