README – Input Validators for COMP 321 Problem Selector

This directory contains two input validators for the problem

Both validators work together to fully verify that the input is properly
formatted and satisfies all constraints.

------------------------------------------------------------
validate.ctd
------------------------------------------------------------

This file is written in the checktestdata (CTD) language and performs
STRUCTURAL / SYNTAX validation only.

It checks:

- First line contains:
    - M: a non-negative integer (very large allowed)
    - N: a positive integer (number of problems)

- Second line:
    - Exists and contains only non-newline characters
    - (Topic correctness and uniqueness are handled in Python)

- Next N lines, each containing:
    - Problem ID: positive integer
    - Points: non-negative integer
    - Difficulty: integer in range 1 to 10
    - Topic: a non-empty string without whitespace
    - Text length: integer in range 1 to 10000

- Ensures there are exactly N problem lines
- Ensures all problem IDs are unique
- Ensures there is no extra data after the last line

This file does NOT check semantic constraints such as:
- problem IDs being in the range 1..N
- points being <= M
- topic preference ranking rules
- permutation correctness

------------------------------------------------------------
validate.py
------------------------------------------------------------

This file performs SEMANTIC / LOGIC validation in Python and exits
with code 42 if (and only if) the input is valid.

It checks:

- Strict formatting of all lines (no extra spaces, no leading zeros, etc.)
- N >= 1 and M >= 0
- The preferred topic list contains no duplicates
- Each problem line is correctly formatted
- Each problem ID is in [1, N]
- Problem IDs form a valid permutation (each appears exactly once)
- Each point value is in [0, M]
- Difficulty is in [1, 10]
- Text length is in [1, 10000]
- No extra input exists beyond what is expected
