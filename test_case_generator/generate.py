#!/usr/bin/env python3
import sys
import random
import subprocess
from pathlib import Path

# ---------------------------------------------------------
# Global Config
# ---------------------------------------------------------

RANDOM_SEED = 321321
NUM_RANDOM = 10
NUM_EDGE = 10


# ---------------------------------------------------------
# Utility
# ---------------------------------------------------------

def write_file(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(text)

def run_solver(in_path, ans_path, solver_cmd):
    """Run accepted solver (no timeout)."""
    with open(in_path, "r") as f:
        inp = f.read()

    proc = subprocess.run(
        solver_cmd,
        input=inp.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out = proc.stdout.decode().rstrip() + "\n"

    with open(ans_path, "w") as f:
        f.write(out)

def save_case(directory, base, text, solver_cmd):
    in_path = directory / (base + ".in")
    ans_path = directory / (base + ".ans")
    write_file(in_path, text)
    run_solver(in_path, ans_path, solver_cmd)


# ---------------------------------------------------------
# Sample Inputs (from PDF)
# ---------------------------------------------------------

PDF_SAMPLE_1 = """10 4
dp graphs arrays
1 5 3 dp 120
2 6 5 graphs 200
3 4 1 arrays 50
4 8 4 dp 300
"""

PDF_SAMPLE_2 = """10 3
stacks queues trees
1 2 1 stacks 100
2 2 1 stacks 100
3 10 9 trees 100
"""

PDF_SAMPLE_3 = """100000000000000 4
greedy dijkstra strings
1 60000000000000 3 greedy 5000
2 50000000000000 2 dijkstra 8000
3 40000000000000 1 strings 2000
4 70000000000000 5 greedy 10000
"""


# ---------------------------------------------------------
# Secret Tests — Random (FAST VERSION)
# ---------------------------------------------------------

BASE_TOPICS = [
    "dp", "graphs", "trees", "stacks", "queues",
    "greedy", "arrays", "heaps", "math", "strings"
]

def make_random_case():
    """
    RANDOM CASE GENERATOR (final version)

    - N = 50–60
    - pts up to <= 1e15
    - difficulty in [5..10]
    - each problem >= 10% of M
    - assignment always solvable with <= 8 problems
    """

    N = random.randint(50, 60)
    topics = BASE_TOPICS[:]   # all 10 topics

    problems = []

    # ------------------------------------------------------
    # Step 1: choose base point P
    # P controls the entire scale of the instance.
    #
    # We choose P so that:
    #   pts ∈ [P, 2P] and max pts <= 1e15
    #   M  ∈ [5P, 10P]
    # → therefore min pts / M >= P / (10P) = 10%
    # ------------------------------------------------------
    P = random.randint(10**14, 10**15 // 2)   # ensures 2P <= 1e15

    # ------------------------------------------------------
    # Step 2: generate problems with points >= P
    # pts <= 2P <= 1e15
    # ------------------------------------------------------
    for pid in range(1, N + 1):
        pts = random.randint(P, 2 * P)
        diff = random.randint(5, 10)
        topic = random.choice(topics)
        length = random.randint(100, 1000)
        problems.append((pid, pts, diff, topic, length))

    # ------------------------------------------------------
    # Step 3: choose M so that:
    #   - each problem >= 10% M
    #   - solvable with <= 8 problems:
    #       Max sum from 8 problems ≥ M
    # ------------------------------------------------------
    M = random.randint(5 * P, 10 * P)   # ensures 10% rule exactly

    # ------------------------------------------------------
    # Build .in file
    # ------------------------------------------------------
    out = [f"{M} {N}", " ".join(topics)]
    for pid, pts, diff, topic, length in problems:
        out.append(f"{pid} {pts} {diff} {topic} {length}")

    return "\n".join(out) + "\n"



# ---------------------------------------------------------
# 10 Hand-Written Edge Cases (Secret 11–20)
# (Kept identical to your version; all N ≤ 60)
# ---------------------------------------------------------

EDGE_CASES = {}

EDGE_CASES["secret11"] = """500 25
dp graphs trees stacks queues greedy arrays heaps math strings
1 200 2 dp 500
2 150 3 graphs 400
3 180 4 trees 350
4 50 1 stacks 300
5 60 1 queues 250
6 70 2 greedy 200
7 40 1 arrays 180
8 30 2 heaps 160
9 25 1 math 140
10 20 2 strings 130
11 15 1 dp 120
12 14 1 graphs 110
13 13 1 trees 100
14 12 1 stacks 95
15 11 1 queues 90
16 10 1 greedy 85
17 9 1 arrays 80
18 8 1 heaps 75
19 7 1 math 70
20 6 1 strings 65
21 5 1 dp 60
22 4 1 graphs 55
23 3 1 trees 50
24 2 1 stacks 45
25 1 1 queues 40
"""

EDGE_CASES["secret12"] = """1500000000000000 18
dp graphs trees stacks queues greedy arrays heaps math strings
1 300000000000000 5 dp 500
2 250000000000000 4 graphs 480
3 200000000000000 4 trees 460
4 180000000000000 3 stacks 440
5 150000000000000 3 queues 420
6 140000000000000 3 greedy 400
7 130000000000000 2 arrays 380
8 120000000000000 2 heaps 360
9 110000000000000 2 math 340
10 100000000000000 1 strings 320
11 90000000000000  1 dp 300
12 80000000000000  1 graphs 290
13 70000000000000  1 trees 280
14 60000000000000  1 stacks 270
15 50000000000000  1 queues 260
16 40000000000000  1 greedy 250
17 30000000000000  1 arrays 240
18 20000000000000  1 heaps 230
"""

EDGE_CASES["secret13"] = """120 18
dp graphs trees stacks queues greedy arrays heaps math strings
1 7 3 dp 200
2 6 3 graphs 180
3 8 3 trees 160
4 5 3 stacks 210
5 9 3 queues 190
6 7 3 greedy 170
7 8 3 arrays 160
8 6 3 heaps 150
9 9 3 math 140
10 5 3 strings 130
11 7 3 dp 200
12 6 3 graphs 180
13 8 3 trees 160
14 5 3 stacks 210
15 9 3 queues 195
16 7 3 greedy 170
17 8 3 arrays 165
18 6 3 heaps 155
"""

EDGE_CASES["secret14"] = """180 25
dp graphs trees stacks queues greedy arrays heaps math strings
""" + "\n".join([f"{i} 60 3 {BASE_TOPICS[(i-1)%10]} 200" for i in range(1,10)]) + """
""" + "\n".join([f"{i} 30 3 {BASE_TOPICS[(i-1)%10]} 150" for i in range(10,20)]) + """
""" + "\n".join([f"{i} 10 3 {BASE_TOPICS[(i-1)%10]} 100" for i in range(20,26)]) + "\n"

EDGE_CASES["secret15"] = """200 25
dp
1 50 2 dp 2000
2 60 2 dp 1900
3 70 2 dp 1800
4 80 2 dp 1700
5 40 2 dp 1600
6 30 2 dp 1500
7 20 2 dp 1400
8 25 2 dp 1300
9 35 2 dp 1200
10 45 2 dp 1100
11 15 2 dp 1000
12 18 2 dp 900
13 22 2 dp 800
14 29 2 dp 700
15 33 2 dp 600
16 37 2 dp 500
17 41 2 dp 400
18 44 2 dp 300
19 48 2 dp 200
20 52 2 dp 100
21 5 2 dp 90
22 8 2 dp 80
23 10 2 dp 70
24 12 2 dp 60
25 14 2 dp 50
"""

EDGE_CASES["secret16"] = """220 20
dp graphs trees stacks queues greedy arrays heaps math strings
1 40 3 dp 200
2 35 3 graphs 190
3 30 3 trees 185
4 28 4 stacks 180
5 27 4 queues 175
6 10 2 greedy 150
7 10 2 arrays 145
8 9 2 heaps 140
9 9 2 math 135
10 8 2 strings 130
11 7 2 dp 120
12 7 2 graphs 115
13 6 2 trees 110
14 6 2 stacks 105
15 5 2 queues 100
16 4 1 greedy 90
17 4 1 arrays 80
18 4 1 heaps 70
19 3 1 math 60
20 3 1 strings 50
"""

EDGE_CASES["secret17"] = """500000000000 25
dp graphs trees stacks queues greedy arrays heaps math strings
1 300000000000 4 dp 2000
2 250000000000 3 graphs 1900
3 200000000000 5 trees 1800
4 100000000000 2 stacks 1700
5 150000000000 3 queues 1600
6 120000000000 2 greedy 1500
7 110000000000 4 arrays 1400
8 90000000000 5 heaps 1300
9 80000000000 3 math 1200
10 70000000000 2 strings 1100
11 60000000000 2 dp 1000
12 50000000000 3 graphs 900
13 40000000000 3 trees 800
14 30000000000 4 stacks 700
15 20000000000 5 queues 600
16 18000000000 1 greedy 500
17 16000000000 1 arrays 450
18 14000000000 1 heaps 400
19 12000000000 1 math 350
20 10000000000 1 strings 300
21 9000000000 1 dp 260
22 8000000000 1 graphs 240
23 7000000000 1 trees 220
24 6000000000 1 stacks 200
25 5000000000 1 queues 180
"""

EDGE_CASES["secret18"] = """300000000000000 25
dp graphs trees stacks queues greedy arrays heaps math strings
1 80000000000000 4 dp 500
2 70000000000000 5 graphs 480
3 60000000000000 3 trees 460
4 50000000000000 3 stacks 440
5 40000000000000 2 queues 420
6 30000000000000 1 greedy 400
7 25000000000000 2 arrays 380
8 20000000000000 1 heaps 360
9 18000000000000 1 math 340
10 16000000000000 1 strings 320
11 14000000000000 2 dp 300
12 13000000000000 2 graphs 290
13 12000000000000 3 trees 280
14 11000000000000 3 stacks 270
15 10000000000000 1 queues 260
16 9000000000000 1 greedy 250
17 8000000000000 1 arrays 240
18 7000000000000 1 heaps 230
19 6000000000000 1 math 220
20 5000000000000 1 strings 210
21 4000000000000 1 dp 200
22 3000000000000 1 graphs 190
23 2000000000000 1 trees 180
24 1000000000000 1 stacks 170
25 900000000000 1 queues 160
"""

EDGE_CASES["secret19"] = """300 25
dp graphs trees stacks queues greedy arrays heaps math strings
1 100 5 dp 500
2 100 5 graphs 450
3 100 5 trees 480
4 90 5 stacks 430
5 90 5 queues 420
6 80 5 greedy 410
7 80 5 arrays 400
8 70 5 heaps 390
9 70 5 math 380
10 60 5 strings 370
11 50 5 dp 360
12 50 5 graphs 350
13 50 5 trees 340
14 40 5 stacks 330
15 40 5 queues 320
16 40 5 greedy 310
17 30 5 arrays 300
18 30 5 heaps 290
19 30 5 math 280
20 30 5 strings 270
21 20 5 dp 260
22 20 5 graphs 250
23 20 5 trees 240
24 20 5 stacks 230
25 20 5 queues 220
"""

EDGE_CASES["secret20"] = """260 18
dp graphs trees stacks queues greedy arrays heaps math strings
1 60 3 dp      300
2 55 3 graphs  280
3 50 4 trees   260
4 45 4 stacks  240
5 40 5 queues  230
6 20 2 greedy  200
7 18 2 arrays  195
8 17 2 heaps   190
9 15 2 math    185
10 14 2 strings 180
11 12 1 dp      160
12 12 1 graphs  150
13 10 1 trees   140
14 10 1 stacks  130
15 9  1 queues  120
16 8  1 greedy  100
17 7  1 arrays   90
18 6  1 heaps    80
"""


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    random.seed(RANDOM_SEED)

    script_dir = Path(__file__).resolve().parent
    root_dir = script_dir.parent

    sample_dir = root_dir / "data" / "sample"
    secret_dir = root_dir / "data" / "secret"

    solver_path = root_dir / "submissions" / "accepted" / "solution.py"
    solver_cmd = [sys.executable, str(solver_path)]

    print("Generating sample cases...")
    save_case(sample_dir, "sample1", PDF_SAMPLE_1, solver_cmd)
    save_case(sample_dir, "sample2", PDF_SAMPLE_2, solver_cmd)
    save_case(sample_dir, "sample3", PDF_SAMPLE_3, solver_cmd)

    print("Generating random secret cases...")
    for i in range(1, NUM_RANDOM+1):
        txt = make_random_case()
        save_case(secret_dir, f"secret{i:02d}", txt, solver_cmd)

    print("Generating hand-written secret cases...")
    for idx, name in enumerate(EDGE_CASES.keys(), start=NUM_RANDOM+1):
        save_case(secret_dir, f"secret{idx:02d}", EDGE_CASES[name], solver_cmd)

    print("Done!")


if __name__ == "__main__":
    main()
