#!/usr/bin/env python3
import sys

def error(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def read_ints(line, expected=None):
    try:
        nums = list(map(int, line.strip().split()))
    except:
        error("Line must contain integers")
    if expected is not None and len(nums) != expected:
        error(f"Expected {expected} integers, got {len(nums)}")
    return nums

def main():
    data = sys.stdin.read().rstrip().split("\n")
    if len(data) < 2:
        error("Input too short")

    # -----------------------------------------
    # Line 1: M N   (NO K, matching PDF)
    # -----------------------------------------
    try:
        M, N = map(int, data[0].split())
    except:
        error("First line must contain two integers M N")

    if M < 0:
        error("M must be non-negative")
    if N < 0:
        error("N must be non-negative")

    # -----------------------------------------
    # Line 2: topic strings (distinct)
    # -----------------------------------------
    topics = data[1].split()
    if len(topics) == 0:
        error("At least one topic required")

    if len(topics) != len(set(topics)):
        error("Topic strings must be distinct")

    # -----------------------------------------
    # Next N lines: each problem
    # id points difficulty topic length
    # -----------------------------------------
    if len(data) != 2 + N:
        error("Number of problem lines does not match N")

    seen_ids = set()

    for i in range(N):
        parts = data[2 + i].split()
        if len(parts) != 5:
            error("Each problem line must have 5 values: id points difficulty topic length")

        pid_str, pts_str, diff_str, topic_str, length_str = parts

        # id must be integer
        try:
            pid = int(pid_str)
        except:
            error("Problem id must be an integer")

        if pid <= 0:
            error("Problem id must be positive")

        if pid in seen_ids:
            error("Duplicate problem id")
        seen_ids.add(pid)

        # points: any non-negative integer (CAN be > M)
        try:
            pts = int(pts_str)
        except:
            error("Points must be an integer")
        if pts < 0:
            error("Points must be non-negative")

        # difficulty: non-negative integer
        try:
            diff = int(diff_str)
        except:
            error("Difficulty must be an integer")
        if diff < 1 or diff > 10:
            error("Difficulty must be between 1-10")

        # topic must be in the topic list
        if topic_str not in topics:
            error("Problem topic must appear in topic list")

        # length: non-negative integer
        try:
            length = int(length_str)
        except:
            error("Length must be an integer")
        if length < 0:
            error("Length must be non-negative")

    # If all checks pass:
    return

if __name__ == "__main__":
    main()
