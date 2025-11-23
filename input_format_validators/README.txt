README – Input Validators for COMP 321 Problem Selector

This directory contains two input validators:

- validate.ctd   
- validate.py   

They are designed to work together to ensure that the input format and
basic constraints of the problem are respected.

------------------------------------------------------------
1. validate.ctd
------------------------------------------------------------

This file uses the checktestdata language to verify the basic shape of
the input. It checks:

- Line 1:
    - Two tokens, both parsed as integers (M and N).

- Line 2:
    - A non-empty line consisting of one or more space-separated tokens.
      (These are interpreted as topic names.)

- Following lines:
    - Exactly N lines follow.
    - Each such line consists of:
        - an integer (problem id)
        - an integer (points)
        - an integer (difficulty)
        - a single token (topic string)
        - an integer (length)

This file does NOT check:
- Ranges on integers (e.g., non-negativity, upper bounds).
- Uniqueness of ids or topics.
- That topics on problems appear in the topic list.
- That the number of lines is consistent with N beyond the repeat N:
  structure itself.

Those semantic checks are handled in validate.py.

------------------------------------------------------------
2. validate.py
------------------------------------------------------------

This Python validator performs more detailed checks on the input
after the basic structure has passed the .ctd stage. It reads the
entire input and enforces the following:

General:
- Input must contain at least 2 lines (first line and topic line).
- First line must contain exactly two integers: M and N.
- M must be non-negative (M >= 0).
- N must be non-negative (N >= 0).
- The total number of lines must be exactly 2 + N
  (i.e., N problem lines after the topics line).

Topics (Line 2):
- The second line must contain at least one topic.
- Topics are space-separated tokens.
- All topics must be distinct (no duplicates).

Problem lines (next N lines):
Each of the N lines must have exactly 5 tokens:
    id  points  difficulty  topic  length

For each problem line, the validator checks:

- id:
    - Must be an integer.
    - Must be positive (id > 0).
    - Must be unique across all problems.

- points:
    - Must be an integer.
    - Must be non-negative (points >= 0).
    - May be larger than M (this is allowed).

- difficulty:
    - Must be an integer.
    - Must be non-negative (difficulty >= 0).
      (No upper bound is enforced here.)

- topic:
    - Must be one of the topics listed on line 2.
    - Any topic that appears in a problem line but not in the topic list
      causes validation to fail.

- length:
    - Must be an integer.
    - Must be non-negative (length >= 0).
