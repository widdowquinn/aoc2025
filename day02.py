#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""day02.py

Today's solution has two solution functions because solving
for the special case (number of repeats == 2) seemed easy enough
to brute force. I did think about generating all possible repeats
of appropriate size, but the puzzle could have gone any number of
ways in part two.
"""

from pathlib import Path


def get_invalid_ids_iter(limits: tuple[int]) -> list[int]:
    """Returns a list of invalid IDs in the passed range.

    This approach iterates over all values in the range and keeps
    a record of invalid values, those where the first and second
    half of the id - as a string - is the same.
    """
    invalid = []  # list of invalid IDs

    # Iterate over test values in the passed range
    for val in range(limits[0], limits[1] + 1):
        valstr = str(val)  # test value as string
        vallen = len(valstr)  # length of test value as string
        validx = vallen // 2  # length of twice-repeated unit
        if vallen % 2:  # Odd lengths can't be twice repeated sequences, so skip
            continue
        elif valstr[:validx] == valstr[validx:]:  # Test for repeat
            invalid.append(val)

    return invalid


def generate_invalid_ids(minlen, maxlen):
    """Return a set of invalid IDs of lengths minlen and maxlen

    This approach generates all invalid values - those where the number
    is a repeated sequence of any smaller set of numbers - between minlen
    and maxlen digits in length.

    We consider all numbers of length minlen to length maxlen to be test values,
    and note that the repeated elements must be a length that exactly divides
    the length of the test value. Then, rather than generate all test values,
    we generate all values that could be composed of repeated elements. So,
    instead of, e.g. generating all nine-digit numbers (of which there are
    1e8 - 1e7 = 90e6), we can generate all 9-fold repeats of the digits 1 to 9
    (nine numbers), and all the three-fold repeats of all the three digit numbers
    (100-999), i.e. fewer than 1e4 numbers, which is a bit quicker.

    We could refactor out the generation of all invalid IDs for a single number
    length into its own function, and use caching on that to speed things
    up further, but this is pretty quick already.
    """
    invalid = []  # list of invalid IDs

    # Iterate over all test number digit lengths in the passed range
    for numlen in range(minlen, maxlen + 1):
        for elemlen in range(
            1, (numlen // 2) + 1
        ):  # Element length can be at maximum half the digits of the test number
            if (
                numlen % elemlen == 0
            ):  # Element sizes must divide the test number length
                repeats = numlen // elemlen  # Number of element repeats
                # Generate all invalid repeat combinations and add them to the list
                for val in range(10 ** (elemlen - 1), 10**elemlen):
                    num = int(str(val) * repeats)
                    invalid.append(int(str(val) * repeats))

    return set(invalid)


def solve_part1(ranges: list[tuple]) -> list[int]:
    """Returns a list of invalid IDs for all passed ranges.

    Invalid here means that the ID is a direct repeat of a single number,
    e.g. 123123, 55, or 987654987654
    """
    invalid = []  # list of invalid IDs

    # Iterate over the passed ranges and compile invalid IDs
    for limits in ranges:
        invalid += get_invalid_ids_iter(limits)

    return invalid


def solve_part2(ranges: list[tuple]) -> list[int]:
    """Returns a list of invalid IDs for all passed ranges.

    Invalid here means that the ID is composed of two or more repeats of
    the same number, e.g. 123123, 555, or 9898989898
    """
    invalid = []  # list of invalid IDs

    # Iterate over the passed ranges and compile invalid IDs
    for limits in ranges:
        # To generate all invalid IDs we need the lengths of the limits as strings
        invalid_ids = generate_invalid_ids(len(str(limits[0])), len(str(limits[1])))
        elf_ids = set(range(limits[0], limits[1] + 1))  # All IDs in the passed range
        invalid += list(
            elf_ids.intersection(invalid_ids)
        )  # Set intersection identifies invalid IDs

    return invalid


def load_ranges(fpath: Path) -> list[tuple]:
    """Returns a list of product range tuples."""
    ranges = []

    with fpath.open() as ifh:
        for limits in ifh.read().strip().split(","):
            ranges.append(tuple(int(_) for _ in limits.split("-")))

    return ranges


## Run tests and solve
if __name__ == "__main__":
    testdata = load_ranges(Path("day02/test.txt"))
    invalid_pt1 = solve_part1(testdata)
    invalid_pt2 = solve_part2(testdata)
    print(sum(invalid_pt1))
    print(sum(invalid_pt2))

    inputdata = load_ranges(Path("day02/input.txt"))
    invalid_pt1 = solve_part1(inputdata)
    invalid_pt2 = solve_part2(inputdata)
    print(sum(invalid_pt1))
    print(sum(invalid_pt2))
