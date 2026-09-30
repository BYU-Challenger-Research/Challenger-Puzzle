import numpy as np
from typing_extensions import Self


class Puzzle:
    """
    An object representing the Challenger Puzzle

    :attr prob_array: the problem array
    :attr lower_bound: the lower bound for random number generator
    :attr upper_bound: the upper bound for random number generator
    :attr row_sums: the sum of each row
    :attr col_sums: the sum of each column
    :attr diag_sums: the sum of each diagonal
    :attr _n: the dimension of the puzzle
    """

    def __init__(self: Self, prob_array: np.ndarray, row_sums: np.ndarray, col_sums: np.ndarray, diag_sums: np.ndarray, lower_bound: int, upper_bound: int) -> Self:
        """
        Initializes the puzzle generator object

        :param prob_array: the problem matrix
        :param row_sums: the row sum array
        :param col_sums: the column sum array
        :param diag_sums: the diagonal sum array
        :param lower_bound: the lower bound for cell values
        :param upper_bound: the upper bound for cell values
        """
        if len(prob_array.shape) != 2:
            raise ValueError("problem array must be two-dimensional")
        if prob_array.shape[0] != prob_array.shape[1]:
            raise ValueError("problem array must be square")
        self.prob_array = prob_array
        self._n = prob_array.shape[0]
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.diag_sums = diag_sums
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def __len__(self: Self) -> int:
        """
        Gets the dimension of the Challenger puzzle

        :return: the dimension of the Challenger puzzle
        """
        return self._n