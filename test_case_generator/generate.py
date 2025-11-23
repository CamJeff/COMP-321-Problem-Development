#!/usr/bin/env python3
import sys
import random
import subprocess
from pathlib import Path
import resource   # <-- for memory limit

# ---------------------------------------------------------
# Config
# ---------------------------------------------------------

RANDOM_SEED = 321321
MAX_M = 10**15
MAX_N = 25
NUM_SECRET = 20
SOLVER_TIMEOUT = 20              # seconds
SOLVER_MEM_LIMIT = 2 * 1024**3   # 2GB

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def set_memory_limit():
    """Limit memory usage for the solver process (Linux/macOS)."""
    resource.setrlimit(resource.RLIMIT_AS,
                       (SOLVER_MEM_LIMIT, SOLVER_MEM_LIMIT))


def write_case(in_path, case_text):
    with open(in_path, "w") as f:
        f.write(case_text)


def run_solver_and_write(in_path, ans_path, solver_cmd):
    with open(in_path, "r") as f:
        inp = f.read()

    try:
        proc = subprocess.run(
            solver_cmd,
            input=inp.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=SOLVER_TIMEOUT,
            preexec_fn=set_memory_limit  # <<<<<< memory limit added
        )
        out = proc.stdout.decode().rstrip() + "\n"

    except subprocess.TimeoutExpired:
        out = "-1\n"    # TLE → -1
    except MemoryError:
        out = "-1\n"    # hard fail → treat as MLE
    except Exception:
        out = "-1\n"

    with open(ans_path, "w") as f:
        f.write(out)


def save_case(dir_path, base_name, case_text, solver_cmd):
    dir_path.mkdir(parents=True, exist_ok=True)
    in_path = dir_path / f"{base_name}.in"
    ans_path = dir_path / f"{base_name}.ans"
    write_case(in_path, case_text)
    run_solver_and_write(in_path, ans_path, solver_cmd)

# ---------------------------------------------------------
# PDF Samples (fixed)
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
# Secret Case Generators
# ---------------------------------------------------------

BASE_TOPICS = [
    "dp", "graphs", "trees", "stacks", "queues",
    "greedy", "arrays", "heaps", "math", "strings"
]

def random_topics():
    k = random.randint(1, 5)
    return random.sample(BASE_TOPICS, k)

def random_problems(N, topics):
    problems = []
    for pid in range(1, N + 1):
        pts = random.randint(1, 10**12)
        diff = random.randint(0, 10)
        topic = random.choice(topics)
        length = random.randint(10, 2000)
        problems.append((pid, pts, diff, topic, length))
    return problems

def build_case(M, topics, problems):
    lines = []
    N = len(problems)
    lines.append(f"{M} {N}")
    lines.append(" ".join(topics))
    for pid, pts, diff, topic, length in problems:
        lines.append(f"{pid} {pts} {diff} {topic} {length}")
    return "\n".join(lines) + "\n"

def make_secret_reachable():
    N = random.randint(5, MAX_N)
    topics = random_topics()
    problems = random_problems(N, topics)
    total_points = sum(p[1] for p in problems)
    max_points = max(p[1] for p in problems)
    M = random.randint(max_points, total_points)
    return build_case(M, topics, problems)

def make_secret_unreachable():
    N = random.randint(5, MAX_N)
    topics = random_topics()
    problems = random_problems(N, topics)
    total_points = sum(p[1] for p in problems)
    max_points = max(p[1] for p in problems)
    extra = random.randint(1, max_points)
    M = min(total_points + extra, MAX_M)
    return build_case(M, topics, problems)

# ---------------------------------------------------------
# Generate Samples (PDF version)
# ---------------------------------------------------------

def generate_samples(sample_dir, solver_cmd):
    save_case(sample_dir, "sample1", PDF_SAMPLE_1, solver_cmd)
    save_case(sample_dir, "sample2", PDF_SAMPLE_2, solver_cmd)
    save_case(sample_dir, "sample3", PDF_SAMPLE_3, solver_cmd)

# ---------------------------------------------------------
# Generate Secrets
# ---------------------------------------------------------

def generate_secrets(secret_dir, solver_cmd):
    for i in range(1, NUM_SECRET + 1):
        if i % 2 == 0:
            case_text = make_secret_reachable()
        else:
            case_text = make_secret_unreachable()
        save_case(secret_dir, f"secret{i:02d}", case_text, solver_cmd)

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
    generate_samples(sample_dir, solver_cmd)

    print("Generating secret cases...")
    generate_secrets(secret_dir, solver_cmd)

    print("Done.")

if __name__ == "__main__":
    main()