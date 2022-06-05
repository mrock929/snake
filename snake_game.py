import numpy as np
import matplotlib.pyplot as plt
from board import Board
from typing import Optional, Tuple


class SnakeGame:
    """Main class for setting up and playing Snake"""

    def __init__(self, game_size: int = 10, num_apples: int = 1) -> None:
        """
        Initialize the game. Players move the snake through the board. When they eat an apple, the length of the snake
            increases by one. THe goal is to get the longest snake. If the player touches the snake or goes off the
            board (hits the wall) then they lose the game.

        Args:
            game_size: Single integer that sets the size of the game board. Only square boards are used. Number is the
                edge length of both the width and height
            num_apples: Number of concurrent apples on the board
        """

        if game_size < 6:
            raise ValueError("The game size must be at least 6")

        if num_apples > game_size:
            raise ValueError(
                "The number of apples should not be more than the size of the board"
            )

        self.board_size = game_size
        self.board = Board(board_size=game_size)
        if num_apples > 1:  # Board initializes the first apple in a constant location
            self.generate_apples(new_apples=num_apples - 1)
        self.show_board()

    def generate_apples(self, new_apples: int, seed: Optional[int] = None) -> np.array:
        """
        Initialize the apple generation

        Args:
            new_apples: Number of new apples to generate
            seed: Optional random seed to use

        Returns:
            Numpy array of [[x1, y1], [x2, y2]...] coordinates of new apples

        """

        apples = None

        if seed is None:
            seed = np.random.randint(low=0, high=9999)

        # Initialize random number generator
        rng = np.random.default_rng(seed)

        for i in range(new_apples):
            valid_apple = False
            count = 1
            while not valid_apple:
                new_apple = rng.integers(low=0, high=self.board_size, size=(1, 2))
                if self.board.state[new_apple[0][0], new_apple[0][1]] == 0:
                    valid_apple = True
                count += 1
                if count > self.board_size ** 3:
                    raise RuntimeError(
                        "Could not generate a valid apple on the board. You win!"
                    )

            # Add apple to board
            self.board.state[new_apple[0][0], new_apple[0][1]] = 3

            if apples is None:
                apples = new_apple
            else:
                apples = np.append(apples, new_apple, axis=0)

        self.board.apples = np.append(self.board.apples, apples, axis=0)

        return apples

    def move(self, command: str) -> None:
        """
        Move the snake

        Args:
            command: Command in a string. The only valid characters are l, r, u, d. Multiple commands may be issued at
                once. Example: "dddrr" would move the snake down 3 and then right 2

        """

        head = self.board.snake[
            -1
        ]  # head (front) of the snake, the part that moves to the new space

        # Rows are the up/down direction, columns are the left/right direction.
        # Origin is row=0, column=0 at the top left of board. Positive down and to the right.
        for letter in command:
            if letter == "u":
                new_loc = [head[0] - 1, head[1]]
                print("Moving up")
            elif letter == "r":
                new_loc = [head[0], head[1] + 1]
                print("Moving right")
            elif letter == "d":
                new_loc = [head[0] + 1, head[1]]
                print("Moving down")
            elif letter == "l":
                new_loc = [head[0], head[1] - 1]
                print("Moving left")
            else:
                raise ValueError(
                    f"Invalid letter in command string: {letter}. Only u, r, d, and l are valid."
                )

            valid_loc = self.check_new_loc(loc=new_loc)
            is_apple, apple_int = self.check_for_apple(loc=new_loc)

            if not valid_loc:
                print(
                    f"You died when you tried to move {letter}! Score: {len(self.board.snake) - 3}"
                )
                break

            self.update_board(new_snake=new_loc, apple=is_apple, apple_i=apple_int)
            head = new_loc

        self.show_board()

    def check_new_loc(self, loc: np.array) -> bool:
        """
        Check if the new location is valid. Valid locations are on the board and do not contain any part of the snake.
        All other locations are invalid (snake pieces or off the board) and cause the player to lose the game

        Args:
            loc: New location for the snake

        Returns: True if new location is valid, else false

        """

        # Check if on board
        if loc[0] < 0 or loc[0] > self.board_size - 1:
            return False
        if loc[1] < 0 or loc[1] > self.board_size - 1:
            return False
        # See https://stackoverflow.com/questions/39452843/in-operator-for-numpy-arrays?noredirect=1&lq=1
        if ((self.board.snake == loc).all(axis=1)).any():
            return False

        return True

    def check_for_apple(self, loc: np.array) -> Tuple[bool, int]:
        """
        Check if the new location contains an apple

        Args:
            loc: New location for the snake

        Returns: True if the new location contains an apple, else False

        """

        overlap_array = (self.board.apples == loc).all(axis=1)
        # See https://stackoverflow.com/questions/39452843/in-operator-for-numpy-arrays?noredirect=1&lq=1

        if overlap_array.any():
            return True, np.where(overlap_array)[0]
        else:
            return False, 0

    def update_board(self, new_snake: np.array, apple: bool, apple_i: int) -> None:
        """
        Update the board state based on the current move command

        Args:
            new_snake: New snake location
            apple: Is this location an apple. True if yes
            apple_i: Int of the row within self.board.apple to remove the apple from

        """

        # Update old head location to be a 1 instead of a 2
        self.board.state[self.board.snake[-1][0], self.board.snake[-1][1]] = 1

        # Add new snake location to snake and state
        self.board.snake = np.append(self.board.snake, [new_snake], axis=0)
        self.board.state[new_snake[0], new_snake[1]] = 2

        if apple:
            self.generate_apples(new_apples=1)
            print("You ate an apple! Score + 1")
            # Remove apple that was eaten
            self.board.apples = np.delete(self.board.apples, apple_i, axis=0)
        else:  # snake moves and does not grow, remove from snake and state
            self.board.state[self.board.snake[0][0], self.board.snake[0][1]] = 0
            self.board.snake = np.delete(self.board.snake, 0, axis=0)

    def show_board(self) -> None:
        """
        Create and display a plot of the current board, snake, and apples

        """

        plt.figure()
        plt.imshow(self.board.state, cmap="gray_r")
        plt.tick_params(axis="both", labelsize=0, length=0)
        plt.show()
