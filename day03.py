#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""day03.py

Two solution functions today as I had to get somewhere and it
kind of disrupted my flow. The second (get_complex_joltage())
function is more general, and searches the valid "number space"
from the current largest number. The initial solution is a basic
logical route to getting the two-digit solution.
"""

from pathlib import Path


def largest_in_sequence(data: list[int]) -> tuple[int, int]:
    """Returns the largest value and its position in the passed list"""
    val = max(data)
    idx = data.index(val)

    return val, idx


def get_simple_joltage(data: list[list[int]]) -> list[int]:
    """Returns joltage for each bank in the passed list

    Each item in the list is a bank from the puzzle; each bank
    is a list of [0-9] ratings. The general approach is that
    the first instance of the largest integer must be in the
    number, and if it is the last number in the sequence, then
    we also need the first instance of the next-largest integer
    in the bank; but if it is in any other position, we need
    the largest integer that occurs _after_ that one, in
    the sequence.
    """
    bankvals = []  # Joltages for each bank

    for bank in data:
        lge_val, idx = largest_in_sequence(bank)  # Find largest value and location
        if idx < len(bank) - 1:  # Largest value is last in sequence
            # Find largest value preceding in the preceding list
            sml_val, _ = largest_in_sequence(bank[idx + 1 :])
            bankvals.append(int(str(lge_val) + str(sml_val)))
        else:  # Find largest value _following_ lge_val
            sml_val, _ = largest_in_sequence(bank[:idx])
            bankvals.append(int(str(sml_val) + str(lge_val)))

    return bankvals


def get_joltage(bank: list[int], length: int) -> int:
    """Return the highest joltage of requested length for a bank.

    We represent the sequence as a tree of 'activated' indices.
    At each iteration, we consider the result of activating each
    remaining position from the list of 'inactive' indices, and
    activate the position that gives us the largest number (removing
    it from the inactive list). This grows the largest number to
    an arbitrary number of digits.
    """
    inactive = list(range(len(bank)))  # Sorted list of inactive indices
    active = []  # Sorted list of active indices

    for _ in range(length):  # One iteration for each digit in final number
        newval, newidx = 0, None  # New best value and index list
        for index in inactive:  # Iterate over remaining active indices
            # What number would this give us?
            test_idx = sorted(active + [index])
            test_val = int("".join([str(bank[idx]) for idx in test_idx]))
            if test_val > newval:  # If bigger than the largest we've seen, keep it
                newval = test_val
                newidx = index
        active.append(newidx)  # Update active and inactive indices
        inactive.remove(newidx)

    return newval


def get_complex_joltage(data: list[list[int]], length: int = 12) -> list[int]:
    """Returns joltage of desired length for each bank in the list"""
    bankvals = []

    for bank in data:
        bankvals.append(get_joltage(bank, length))

    return bankvals


def load_data(fpath: Path) -> list[list[int]]:
    """Returns a list of banks as defined in the puzzle.

    Banks are stored as lists of ints.
    """
    banks = []

    with fpath.open() as ifh:
        for line in [_.strip() for _ in ifh.readlines()]:
            banks.append([int(_) for _ in line])

    return banks


## Run tests and solve
if __name__ == "__main__":
    import time

    t0 = time.time()  # Start clock

    testdata = load_data(Path("day03/test.txt"))
    print(sum(get_simple_joltage(testdata)))
    print(sum(get_complex_joltage(testdata, 12)))

    inputdata = load_data(Path("day03/input.txt"))
    print(sum(get_simple_joltage(inputdata)))
    print(sum(get_complex_joltage(inputdata, 12)))

    print(f"Total time: {time.time() - t0:.3f}s")
