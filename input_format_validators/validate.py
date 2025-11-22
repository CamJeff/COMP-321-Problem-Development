#!/usr/bin/env python3

# This is a sample input validator, written in Python 3.

# Please refer to the comments in README.md for a description of the syntax it
# is validating. Then, change it as you need.

import sys
import re

INT_NONNEG = r'(0|[1-9][0-9]*)'   # 0, 1, 2, ..., no leading zeros
INT_POS    = r'[1-9][0-9]*'       # 1, 2, ..., no leading zeros

# INPUT LINE 1: Reading numbers M, N
first_line = sys.stdin.readline()
assert re.match(rf'^{INT_NONNEG} {INT_POS}\n$', first_line), "Bad format on first line"

M_str, N_str = first_line.split()
M = int(M_str)
N = int(N_str)

# We must have at least one problem. Points needed must be non-negative.
assert N >= 1, "N must be at least 1"
assert M >= 0, "M must be non-negative"

# INPUT LINE 2: topic preference list
topics_line = sys.stdin.readline()

# There MUST be a non-empty topic preference list
assert topics_line != '\n', "Topic preference list cannot be empty when problems exist"
assert re.match(r'^\S+( \S+)*\n$', topics_line), "Bad format on topics line"

preferred_topics = topics_line.strip().split()

# topics must be distinct
assert len(preferred_topics) == len(set(preferred_topics)), "Duplicate topics in preference list"

# NEXT N INPUT LINES: the problems
#
# Format per line:
#   Problem_No  Points  Difficulty  Topic  Text_Length
#
# Constraints:
#   Problem_No   in [1, N], no leading zeros
#   Points       in [0, M], no leading zeros for non-zero
#   Difficulty   integer from 1 to 10 (no leading zeros)
#   Topic        non-empty string, no spaces (must be in preference list)
#   Text_Length  integer, 1 <= Text_Length <= 10^4, no leading zeros for non-zero
#

problem_id_pattern = INT_POS                  # Problem_No > 0, no leading zeros
points_pattern     = INT_NONNEG               # Points >= 0
difficulty_pattern = r'(10|[1-9])'            # 1..10, no leading zeros
topic_pattern      = r'\S+'                   # non-empty, no spaces
textlen_pattern    = r'[1-9][0-9]{0,4}'       # 1..99999, we'll clamp to <= 10000 later

problem_line_re = re.compile(
    rf'^{problem_id_pattern} {points_pattern} {difficulty_pattern} {topic_pattern} {textlen_pattern}\n$'
)

seen_ids = set()

for _ in range(N):
    line = sys.stdin.readline()
    assert line != '', "Unexpected end of input while reading problems"
    assert problem_line_re.match(line), "Bad format in problem line"

    p_id_str, pts_str, diff_str, topic, len_str = line.split()

    # Topic must appear in the preference list
    assert topic in preferred_topics, f"Topic '{topic}' not found in preference list"

    # Convert to integers and check ranges
    p_id = int(p_id_str)
    pts  = int(pts_str)
    diff = int(diff_str)
    length = int(len_str)

    # Problem_No in [1, N], all unique
    assert 1 <= p_id <= N, "Problem ID out of range"
    assert p_id not in seen_ids, "Duplicate problem ID"
    seen_ids.add(p_id)

    # Points in [0, M]
    assert 0 <= pts <= M, "Points out of range"

    # Difficulty in [1, 10]
    assert 1 <= diff <= 10, "Difficulty out of range"

    # Text length in [1, 10000]
    assert 1 <= length <= 10000, "Text length out of range"

    # Topic: already guaranteed non-empty and no spaces by regex.
    # Character set is not further restricted by the problem statement.

# Ensure we have exactly N problems and IDs are a permutation of 1..N
assert len(seen_ids) == N, "Incorrect number of distinct problem IDs"

# Ensure no extra input
assert sys.stdin.readline() == '', "Extra input detected"

# If we get here, the input is valid, yay!!!!
sys.exit(42)

