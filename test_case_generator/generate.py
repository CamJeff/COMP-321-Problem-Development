#!/usr/bin/env python3
import sys
import random
import subprocess
from pathlib import Path

# ---------------------------------------------------------
# Global Config
# ---------------------------------------------------------

RANDOM_SEED = 999
NUM_RANDOM = 13
NUM_EDGE = 7


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
dp graphs arrays trees queues
1 5 8 dp 120
2 6 10 graphs 200
3 4 6 arrays 50
4 8 9 dp 300
"""

PDF_SAMPLE_2 = """10 3
stacks queues trees strings dp
1 2 5 stacks 100
2 2 5 stacks 100
3 10 10 trees 100
"""

PDF_SAMPLE_3 = """100000000000000 4
greedy dijkstra strings stacks dp
1 60000000000000 8 greedy 5000
2 50000000000000 7 dijkstra 8000
3 40000000000000 6 strings 2000
4 70000000000000 10 greedy 10000
"""


# ---------------------------------------------------------
# Secret Tests — Random (FAST VERSION)
# ---------------------------------------------------------

# 10 topics
BASE_TOPICS = [
    "dp", "graphs", "trees", "stacks", "queues",
    "greedy", "arrays", "heaps", "math", "strings"
]

def make_random_case():
    """
    RANDOM CASE GENERATOR (final version)

    - N = 50-60
    - pts up to <= 1e15
    - difficulty in [5..10]
    - each problem >= 10% of M
    - assignment always solvable with <= 8 problems
    """

    N = random.randint(10, 60)
    topics = random.sample(BASE_TOPICS, 5) # 5 out of the 10 topics

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
        pts = random.randint(P, 2 * P) # Points from 10^14 to 10^15
        diff = random.randint(5, 10) # Difficulty from 5 to 10
        topic = random.choice(topics) # Any one of the listed topics
        length = random.randint(10, 1000) # Up to 1000 words
        problems.append((pid, pts, diff, topic, length))

    # ------------------------------------------------------
    # Step 3: choose M so that:
    #   - each problem >= 10% M
    #   - solvable with <= 8 problems:
    #       Max sum from 8 problems ≥ M
    # ------------------------------------------------------
    M = random.randint(5 * P, 10 * P) # ensures 10% rule exactly

    # ------------------------------------------------------
    # Build .in file
    # ------------------------------------------------------
    out = [f"{M} {N}", " ".join(topics)]
    for pid, pts, diff, topic, length in problems:
        out.append(f"{pid} {pts} {diff} {topic} {length}")

    return "\n".join(out) + "\n"


# ---------------------------------------------------------
# 6 Hand-Written Edge Cases (Secret 15–20)
# ---------------------------------------------------------

EDGE_CASES = {}

# "Anti-DP" Case, M is too large ~10^15
# And different point values creates a huge
# memoization table
# Solution: 51 to 60
EDGE_CASES["secret14"] = """1664648579257252 55
math dp heaps stacks graphs
1 275310451627982 5 math 345
2 224009644306391 7 dp 93
3 188000472827997 6 stacks 963
4 301480838346260 10 stacks 252
5 184414918810168 6 heaps 442
6 299480454747019 9 stacks 191
7 299059026814417 9 graphs 78
8 175235932836036 5 graphs 957
9 326870514668770 10 math 814
10 193303974366425 8 dp 472
11 327895540618812 6 math 688
12 283680593358882 9 stacks 920
13 309532162001267 9 math 600
14 332071500748619 10 heaps 459
15 228272562764032 7 graphs 744
16 230326866153622 8 stacks 780
17 292918769611773 5 heaps 576
18 268129752880351 7 dp 939
19 195075483730569 7 dp 350
20 326174706380959 9 dp 58
21 319307589275198 10 math 792
22 269828422248613 7 dp 77
23 200223343709352 10 graphs 63
24 347438158075416 6 math 520
25 282378177924615 10 dp 379
26 207682653369411 9 math 554
27 276592400475259 8 stacks 93
28 189084174661945 7 heaps 16
29 209083199907267 8 graphs 853
30 300252654192848 9 math 349
31 341763040153840 10 stacks 258
32 185739524095963 7 graphs 386
33 262345201004631 9 dp 227
34 259191744366721 9 math 425
35 304764584529719 9 stacks 486
36 348273622635810 9 math 411
37 311980650721309 6 dp 821
38 248685991757844 8 heaps 35
39 276158241789185 7 graphs 657
40 187044366505866 10 stacks 224
41 241252263336039 7 dp 628
42 271013716579990 10 math 968
43 266007797061341 10 dp 962
44 218199478646947 8 graphs 999
45 259907490443315 8 stacks 695
46 319218820989082 7 heaps 726
47 286247499923336 7 heaps 581
48 329589022188347 10 dp 179
49 232103924170895 10 dp 276
50 336489504195733 7 graphs 896
51 328185991506878 9 graphs 308
52 273631897542288 5 heaps 108
53 333069586055821 10 stacks 578
54 232269256360166 5 dp 513
55 251734738602598 7 dp 829
"""

# "Anti-Brute Force" Case, N = 60, too slow
# Solution: 51 to 60
EDGE_CASES["secret15"] = """1000000000000000 60
dp graphs trees stacks queues
1 100000000000000 10 dp 100
2 100000000000000 10 dp 100
3 100000000000000 10 dp 100
4 100000000000000 10 dp 100
5 100000000000000 10 dp 100
6 100000000000000 10 dp 100
7 100000000000000 10 dp 100
8 100000000000000 10 dp 100
9 100000000000000 10 dp 100
10 100000000000000 10 dp 100
11 100000000000000 10 dp 100
12 100000000000000 10 dp 100
13 100000000000000 10 dp 100
14 100000000000000 10 dp 100
15 100000000000000 10 dp 100
16 100000000000000 10 dp 100
17 100000000000000 10 dp 100
18 100000000000000 10 dp 100
19 100000000000000 10 dp 100
20 100000000000000 10 dp 100
21 100000000000000 10 dp 100
22 100000000000000 10 dp 100
23 100000000000000 10 dp 100
24 100000000000000 10 dp 100
25 100000000000000 10 dp 100
26 100000000000000 10 dp 100
27 100000000000000 10 dp 100
28 100000000000000 10 dp 100
29 100000000000000 10 dp 100
30 100000000000000 10 dp 100
31 100000000000000 10 dp 100
32 100000000000000 10 dp 100
33 100000000000000 10 dp 100
34 100000000000000 10 dp 100
35 100000000000000 10 dp 100
36 100000000000000 10 dp 100
37 100000000000000 10 dp 100
38 100000000000000 10 dp 100
39 100000000000000 10 dp 100
40 100000000000000 10 dp 100
41 100000000000000 10 dp 100
42 100000000000000 10 dp 100
43 100000000000000 10 dp 100
44 100000000000000 10 dp 100
45 100000000000000 10 dp 100
46 100000000000000 10 dp 100
47 100000000000000 10 dp 100
48 100000000000000 10 dp 100
49 100000000000000 10 dp 100
50 100000000000000 10 dp 100
51 100000000000000 5 dp 100
52 100000000000000 5 dp 100
53 100000000000000 5 dp 100
54 100000000000000 5 dp 100
55 100000000000000 5 dp 100
56 100000000000000 5 dp 100
57 100000000000000 5 dp 100
58 100000000000000 5 dp 100
59 100000000000000 5 dp 100
60 100000000000000 5 dp 100
"""

# "Anti-Greedy" Case
# A "bait" problem has Difficulty 5. The solution has Difficulty 6
# Solution: 2
EDGE_CASES["secret16"] = """1000000000000000 2
greedy arrays heaps math strings
1 100000000000000 5 greedy 1
2 1000000000000000 6 greedy 1
"""

# "Tie-Breaker" Case, the only differences are 
# Topics and Length. Solution: 2
EDGE_CASES["secret17"] = """1000000000000000 40
arrays heaps stacks queues trees
1 1000000000000000 5 heaps 1000
2 1000000000000000 5 arrays 1
3 1000000000000000 5 stacks 5000
4 1000000000000000 5 queues 10
5 1000000000000000 5 trees 100
6 1000000000000000 5 heaps 1000
7 1000000000000000 5 arrays 10000
8 1000000000000000 5 stacks 5000
9 1000000000000000 5 queues 10
10 1000000000000000 5 trees 100
11 1000000000000000 5 heaps 1000
12 1000000000000000 5 arrays 10000
13 1000000000000000 5 stacks 5000
14 1000000000000000 5 queues 10
15 1000000000000000 5 trees 100
16 1000000000000000 5 heaps 1000
17 1000000000000000 5 arrays 10000
18 1000000000000000 5 stacks 5000
19 1000000000000000 5 queues 10
20 1000000000000000 5 trees 100
21 1000000000000000 5 heaps 1000
22 1000000000000000 5 arrays 10000
23 1000000000000000 5 stacks 5000
24 1000000000000000 5 queues 10
25 1000000000000000 5 trees 100
26 1000000000000000 5 heaps 1000
27 1000000000000000 5 arrays 10000
28 1000000000000000 5 stacks 5000
29 1000000000000000 5 queues 10
30 1000000000000000 5 trees 100
31 1000000000000000 5 heaps 1000
32 1000000000000000 5 arrays 10000
33 1000000000000000 5 stacks 5000
34 1000000000000000 5 queues 10
35 1000000000000000 5 trees 100
36 1000000000000000 5 heaps 1000
37 1000000000000000 5 arrays 10000
38 1000000000000000 5 stacks 5000
39 1000000000000000 5 queues 10
40 1000000000000000 5 trees 100
"""

# "Overshoot" Case, traps greedy solution
# Solution: 3
EDGE_CASES["secret18"] = """1000000000000000 3
dp graphs trees stacks queues
1 500000000000000 5 dp 100
2 500000000000000 5 dp 100
3 1000000000000000 9 dp 100
"""

# "Count" Tie-Breaker Case
# Fewer problems must win (not 1 and 2)
# Solution: 3
EDGE_CASES["secret19"] = """1000000000000000 3
dp graphs trees stacks queues
1 500000000000000 5 dp 100
2 500000000000000 5 dp 100
3 1000000000000000 10 dp 100
"""

# "Topic" Tie-Breaker Case
# Must choose the "better" topic
# Solution: 3
EDGE_CASES["secret20"] = """1000000000000000 3
dp graphs trees stacks queues
1 1000000000000000 10 graphs 100
2 1000000000000000 10 queues 100
3 1000000000000000 10 dp 100
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
