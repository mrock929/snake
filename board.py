import numpy as np
from dataclasses import dataclass


@dataclass
class Board:
    """Dataclass that stores the board state, including the location of the snake and apple(s)"""

    def __init__(self, board_size: int) -> None:
        """
        Initialize the board state

        Args:
            board_size: Size of the game board. Only square boards are used.
        """

        self.state = np.zeros((board_size, board_size))
        self.apples = np.array(
            [[board_size - 2, board_size - 2]]
        )  # [x, y] coordinates of each apple
        self.snake = np.array(
            [[0, 1], [1, 1], [2, 1]]
        )  # Initial snake position, vertical line of length 3

        # Initialize the snake and apples on the board
        for point in self.snake:
            self.state[point[0], point[1]] = 1
        # Initialize head of snake as a different color
        self.state[self.snake[-1][0], self.snake[-1][1]] = 2

        for apple in self.apples:
            self.state[apple[0], apple[1]] = 3
