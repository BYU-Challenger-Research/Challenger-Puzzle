import numpy as np
from typing import Optional
from typing_extensions import Self

from puzzle import Puzzle


class Generator:
    """
    A Challenger puzzle generator

    :attr n: the dimension of puzzles to generate
    :attr lower_bound: the lower bound of numbers to use for puzzle generation
    :attr upper_bound: the upper bound of numbers to use for puzzle generation
    :attr seed: the optional seed to use for random number generation
    """

    def __init__(self: Self, n: int=4, lower_bound: int=1, upper_bound: int=9, seed: Optional[int]=None) -> None:
        """
        Initializes a puzzle generator

        :param n: the dimension of Challenger puzzles to generate
        :param lower_bound: lower bound for random number generation
        :param upper_bound: upper bound for random number generation
        :param seed: optional seed for random number generation
        """
        self.n = n
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        if seed is not None:
            np.random.seed(seed)

    def generate(self: Self, n: Optional[int]=None, lower_bound: Optional[int]=None, upper_bound: Optional[int]=None, solution: bool=False) -> tuple[Puzzle, Optional[np.ndarray]]:
        """
        Randomly generates a challenger puzzle object

        :param n: optional dimension of puzzle array
        :param lower_bound: optional lower bound for random number generator
        :param upper_bound: optional upper bound for random number generator

        :return: a randomly generated Challenger puzzle and its generating solution (optional)
        """
        if n is None:
            n = self.n
        if lower_bound is None:
            lower_bound = self.lower_bound
        if upper_bound is None:
            upper_bound = self.upper_bound
        gen_array = np.random.randint(lower_bound, upper_bound, size=(n, n))
        available_indices = np.arange(n)
        np.random.shuffle(available_indices)
        prob_array = np.empty((n, n))
        prob_array.fill(np.nan)
        for i in range(n):
            prob_array[i, available_indices[i]] = gen_array[i, available_indices[i]]
        puzzle = Puzzle(
            prob_array,
            np.sum(gen_array, axis=1),
            np.sum(gen_array, axis=0),
            np.array([np.trace(gen_array), np.trace(np.fliplr(gen_array))]),
            lower_bound,
            upper_bound
        )
        return (puzzle, gen_array) if solution else puzzle


if __name__ == "__main__":
    # Generate random puzzle and view it
    my_puzzle = Generator().generate()
    print("Problem array:")
    print(my_puzzle.prob_array)
    print("Row sums:")
    print(my_puzzle.row_sums)
    print("Col sums:")
    print(my_puzzle.col_sums.reshape([-1, 1]))
    print("Diag sums:")
    print(my_puzzle.diag_sums)