#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""day01.py

Advent of Code day 1

As of this year at the authors' request I'm not including puzzle text,
so it doesn't seem to be worth using Jupyter Notebook.
"""

from pathlib import Path


# Attempt 1: analogue of a physical dial, as a class
#
# Some of the style here is future defensive. Using slots gives faster
# attribute access on larger datasets (probably won't be needed).
# Using reset_X() prepares the class in case we need to reset the dial
# for a problem.
# All attributes and methods are public - it's only a short problem.
class Dial:
    """Analogue of a physical dial that rotates left and right.

    The number of values on the dial is defined by the length argument.
    The dial stores the number of times the pointer ends at zero in
    zerocount, and the number of times it ever points at zero (including
    dutring rotations) in zeropasses."""

    # Slots give faster attribute access.
    # It's unlikely to give an advantage, here
    __slots__ = "mod", "curpos", "zerocount", "zeropasses"

    def __init__(self, startpos: int = 50, length: int = 100) -> None:
        """Initialise the Dial object."""
        self.mod = length  # modulo for dial
        self.curpos = startpos  # current pointer position
        # Clear counts
        self.reset_zerocount()
        self.reset_zeropasses()

    def rotate(self, move: str) -> int:
        """Rotate the dial according to the passed move.

        The move is expected in the format 'DN' as a string, where
        `D` is a direction in {R, L} and `N` is an integer of
        arbitrary size.

        Returns the position of the pointer after rotation ends.
        """
        # Split direction and rotation distance
        dir = move[0]
        val = int(move[1:])

        # Rotate the dial
        if dir == "L":
            self.rotate_left(val % 100)
        elif dir == "R":
            self.rotate_right(val % 100)
        else:
            print(f"Incorrect direction! {dir, val}")

        # Increment the zero count if we end on a zero
        if self.curpos == 0:
            self.zerocount += 1
        # Increment zeropasses by the number of full rotations of the dial
        self.zeropasses += val // self.mod

        return self.curpos

    def rotate_left(self, val: int) -> None:
        """Rotate the dial left"""
        # Increment zeropasses if the rotation includes zero
        # (not including zero as a starting position)
        # and update the current position
        if val >= self.curpos and self.curpos != 0:
            self.zeropasses += 1
        self.curpos = (self.curpos - val) % self.mod

    def rotate_right(self, val: int) -> None:
        """Rotate the dial right"""
        # Increment zeropasses if the rotation includes zero
        # and update the current position
        # NOTE: val cannot be greater than self.mod, so we don't
        # need to account for a zero starting position
        if val >= self.mod - self.curpos:
            self.zeropasses += 1
        self.curpos = (self.curpos + val) % self.mod

    def reset_zerocount(self) -> None:
        """Reset the zero count."""
        self.zerocount = 0

    def reset_zeropasses(self) -> None:
        """Reset the count of the pointer passing zero."""
        self.zeropasses = 0


def solve(data: list[str], verbose=False) -> tuple[int, int]:
    """Return zero counts and passses after all rotations.

    The rotation instructions are passed as a list of 'DN' strings,
    where `D` is a direction in {R, L} and `N` is an integer of
    arbitrary size.
    """
    dial = Dial()  # Instantiate a Dial object
    if verbose:
        print(f"Dial position: {dial.curpos}")

    # Iterate over rotations and move the dial
    for move in data:
        dial.rotate(move)
        if verbose:
            print(
                f"Instruction: {move} - rotate to {dial.curpos} [{dial.zerocount, dial.zeropasses}]"
            )

    return dial.zerocount, dial.zeropasses


def load_instructions(fpath: Path) -> list[str]:
    """Return a list of rotation instructions."""
    with fpath.open() as ifh:
        return [_.strip() for _ in ifh.readlines()]


## Run tests and solve
if __name__ == "__main__":
    testdata = load_instructions(Path("day01/test.txt"))
    zeros, passes = solve(testdata, verbose=True)
    print(f"Test part 1 solution: {zeros}")
    print(f"Test part 2 solution: {passes}")

    part1data = load_instructions(Path("day01/input.txt"))
    zeros, passes = solve(part1data)
    print(f"Part 1 solution: {zeros}")
    print(f"Test part 2 solution: {passes}")
