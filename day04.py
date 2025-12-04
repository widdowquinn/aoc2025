#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""day04.py

Advent of Code day 4

I quite like the 2D map puzzles as they give me chance to remind myself
about numpy - whether it's the quickest solution or not.

This would be faster if, instead of considering all positions in the map
at each iteration, we instead only updated the neighbour counts of the
neighbours of removed rolls - as in Game of Life.
"""

from pathlib import Path

import numpy as np
import numpy.typing as npt


def load_data(fpath: Path) -> npt.NDArray:
    """Returns the map as a numpy array.

    We encode rolls of paper as `1` and empty space as `0`
    """
    map = []

    with fpath.open() as ifh:
        for line in [_.strip() for _ in ifh.readlines()]:
            map.append([int(_) for _ in line.replace(".", "0").replace("@", "1")])

    return np.array(map)


def get_neighbour_count(arr: npt.NDArray, idx: tuple) -> int:
    """Returns the count of neighbouring locations that hold rolls

    We take a radius 1 slice around the passed location and count
    the number of rolls in the neighbourhood (not including the
    passed location)
    """
    # Set 1-unit bounds around the passed location
    xmin, xmax = max(0, idx[0] - 1), min(idx[0] + 2, arr.shape[0])
    ymin, ymax = max(0, idx[1] - 1), min(idx[1] + 2, arr.shape[1])

    slice = arr[xmin:xmax, ymin:ymax]  # get the 2d slice

    # return the sum of neighbours minus the indexed location
    return np.sum(slice) - arr[idx]


def get_neighbour_roll_map(arr: npt.NDArray) -> npt.NDArray:
    """Returns a numpy array describing the count of neighbouring rolls

    If a location holds a roll, the count is presented as a positive
    number or zero. If there is no roll the location is encoded as `-1`.
    """
    ncounts = np.zeros(arr.shape)  # Holds count of adjacent rolls

    # Iterate over array elements and count the number of neighbours
    # If there's a roll in that location, populate ncounts with the
    # number of neighbouring rolls, otherwise insert -1
    with np.nditer(arr, flags=["multi_index"]) as itx:
        for _ in itx:
            if _ == 1:
                ncounts[itx.multi_index] = get_neighbour_count(arr, itx.multi_index)
            else:
                ncounts[itx.multi_index] = -1

    return ncounts


def count_accessible(arr: npt.NDArray) -> int:
    """Returns the count of axcessible rolls.

    Accessible rolls have fewer than 4 neighbouring rolls.
    """
    # Non-roll locations are coded as -1
    count = arr[(arr < 4) & (arr > -1)]

    return len(count)


def count_removed_rolls(arr: npt.NDArray) -> int:
    """Returns total number of removable rolls on the map.

    This iterates versions of the map where all accessible rolls are
    identified, then removed from the map. A count of all accessible
    rolls that were seen/removed is kept.
    """
    removed_count = 0

    while True:  # End state is no more removable rolls
        neighbour_map = get_neighbour_roll_map(arr)
        remove_count = count_accessible(neighbour_map)
        if remove_count == 0:  # No more removable rolls
            break
        else:
            removed_count += remove_count
            with np.nditer(neighbour_map, flags=["multi_index"]) as itx:
                for _ in itx:
                    if (
                        _.item() > -1 and _.item() < 4
                    ):  # accessible so remove from array
                        arr[itx.multi_index] = 0

    return removed_count


## Run tests and solve
if __name__ == "__main__":
    import time

    t0 = time.time()  # Start clock

    testdata = load_data(Path("day04/test.txt"))
    print(count_accessible(get_neighbour_roll_map(testdata)))
    print(count_removed_rolls(testdata))

    inputdata = load_data(Path("day04/input.txt"))
    print(count_accessible(get_neighbour_roll_map(inputdata)))
    print(count_removed_rolls(inputdata))

    print(f"Total time: {time.time() - t0:.3f}s")
