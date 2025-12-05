#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""day05.py

Advent of Code day 5

An interval tree immediately suggested itself, and I've used the excellent
intervaltree package (https://github.com/chaimleib/intervaltree) for work
before.
"""

from intervaltree import IntervalTree  # type: ignore
from pathlib import Path


def load_data(fpath: Path) -> tuple[IntervalTree, set]:
    """Returns an IntervalTree of fresh ranges and a set of items.

    The IntervalTree is merged so that there are no overlapping
    intervals.
    """
    freshranges = IntervalTree()  # holds ranges of fresh items
    items = set()  # items in stocl

    with fpath.open() as ifh:
        for line in [_.strip() for _ in ifh.readlines()]:
            if "-" in line:  # each range is an interval in the tree
                loval, hival = tuple([int(_) for _ in line.split("-")])
                freshranges[loval : hival + 1] = True
            elif len(line):
                items.add(int(line))

    freshranges.merge_overlaps()  # merge overlapping intervals

    return freshranges, items


def count_fresh(ranges: IntervalTree, items: set) -> int:
    """Returns the count of items found in the fresh range."""
    return len([_ for _ in items if ranges[_]])


def count_freshrange(ranges: IntervalTree):
    """Returns the total size of fresh ranges."""
    return sum([_.end - _.begin for _ in ranges])


## Run tests and solve
if __name__ == "__main__":
    import time

    t0 = time.time()  # Start clock

    ranges, items = load_data(Path("day05/test.txt"))
    print(count_fresh(ranges, items))
    print(count_freshrange(ranges))

    ranges, items = load_data(Path("day05/input.txt"))
    print(count_fresh(ranges, items))
    print(count_freshrange(ranges))

    print(f"Total time: {time.time() - t0:.3f}s")
