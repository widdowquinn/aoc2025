#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""day06.py

Advent of Code day 6

The operations themselves are fairly straightforward, but
managing the MyPy type hints introduced some new things for me.
NumPy arrays are very flexible!
"""

import math

import numpy as np
import numpy.typing as npt

from pathlib import Path
from typing import Iterable

# Dynamic assignment of functions, depending on symbol
OPDICT = {"*": math.prod, "+": sum}  # type: ignore


def load_data(fpath: Path):
    """Returns an array of input values and a list of operations.

    The array assumes numbers read left-to-right.
    """
    data = []

    with fpath.open() as ifh:
        for line in [_.strip() for _ in ifh.readlines()]:
            data.append(line.split())

    # Make numpy array from the first n-1 lines
    # Make operation list from the last line
    return np.array(data[:-1], dtype=int), data[-1]


def solve_vertical(data: npt.NDArray, ops: list[str]) -> Iterable[int]:
    """Returns the solution to each maths problem."""
    return (OPDICT[opn](column) for column, opn in zip(data.T, ops))  # type: ignore


def load_cephalopod(fpath: Path):
    """Returns an array of input values and a list of operations.

    The array assumes numbers read top-to-bottom.
    """
    data = []

    # To get numbers reading top-to-bottom we treat the input
    # as a character array
    with fpath.open() as ifh:
        for line in [_.replace("\n", "") for _ in ifh.readlines()]:
            data.append(list(line))

    # Make numpy array from the first n-1 lines
    # Make operation list from the last line
    return np.array(data[:-1]).T, [_ for _ in data[-1] if _ in OPDICT]


def solve_cephalopod(data: npt.NDArray, ops: list[str]):
    """Returns the solution to each maths problem."""
    solutions = []  # Solutions to each maths problem

    curvals = []  # Numbers in current problem
    for row in data:
        val = "".join(row).strip()
        if len(val):  # It's a number
            curvals.append(int(val))
        else:  # It's a break, so problem is complete: carry out the operation
            solutions.append(OPDICT[ops.pop(0)](curvals))  # type: ignore
            curvals = []  # Clear current data values
    solutions.append(OPDICT[ops.pop(0)](curvals))  # type: ignore

    return solutions


## Run tests and solve
if __name__ == "__main__":
    import time

    t0 = time.time()  # Start clock

    data, ops = load_data(Path("day06/test.txt"))
    print(sum(solve_vertical(data, ops)))
    data, ops = load_cephalopod(Path("day06/test.txt"))
    print(sum(solve_cephalopod(data, ops)))

    data, ops = load_data(Path("day06/input.txt"))
    print(sum(solve_vertical(data, ops)))
    data, ops = load_cephalopod(Path("day06/input.txt"))
    print(sum(solve_cephalopod(data, ops)))

    print(f"Total time: {time.time() - t0:.3f}s")
