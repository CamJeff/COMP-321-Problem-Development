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

    if M < 0 or M > 1e15:
        error("M out of range")
    if N < 0 or N > 60:
        error("N out of range")

    # -----------------------------------------
    # Line 2: topic strings (distinct)
    # -----------------------------------------
    topics = data[1].split()
    if len(topics) != 5:
        error("Five topics are required")

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

        # points: any non-negative integer that is at least 10% of M
        try:
            pts = int(pts_str)
        except:
            error("Points must be an integer")
        if pts < 0 or M*0.10 > pts:
            error("Points must be positive and 10% of M")

        # difficulty: non-negative integer
        try:
            diff = int(diff_str)
        except:
            error("Difficulty must be an integer")
        if diff < 5 or diff > 10:
            error("Difficulty must be between 5-10")

        # topic must be in the topic list
        if topic_str not in topics:
            error("Problem topic must appear in topic list")

        # length: non-negative integer
        try:
            length = int(length_str)
        except:
            error("Length must be an integer")
        if length < 0 or length > 1000:
            error("Length must be positive and at most 1000")

    # If all checks pass:
    return

if __name__ == "__main__":
    main()
