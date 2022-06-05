# Tests for snake_game.py

import pytest
from pytest_mock import MockFixture
import numpy as np

from snake_game import SnakeGame
from board import Board


def test_init(mocker: MockFixture):
    # Arrange
    apples = 3
    mocker.patch.object(SnakeGame, "show_board")

    # Act
    snake = SnakeGame(game_size=6, num_apples=apples)

    # Assert
    assert snake.board_size > 0
    assert isinstance(snake.board, Board)
    assert len(snake.board.apples) == apples


@pytest.mark.parametrize(
    "board_size, n_apples, error_message",
    [(2, 2, "size must be at least 6"), (10, 50, "the size of the board")],
)
def test_init_errors(board_size: int, n_apples: int, error_message: str):
    # Act/Assert
    with pytest.raises(ValueError, match=error_message):
        SnakeGame(game_size=board_size, num_apples=n_apples)


def test_generate_apples(mocker: MockFixture):
    # Arrange
    num_apples = 31
    seed = 1
    mocker.patch.object(SnakeGame, "show_board")

    # Act
    snake = SnakeGame(game_size=6)
    snake.generate_apples(new_apples=num_apples, seed=seed)

    # Assert
    assert len(snake.board.apples) == num_apples + 1
    assert (
        np.sum(snake.board.state) == (num_apples + 1) * 3 + 4
    )  # 4 is the value of the starting snake (2 + 1 + 1)


def test_generate_apples_error(mocker: MockFixture):
    # Arrange
    num_apples = 33
    seed = 1
    mocker.patch.object(SnakeGame, "show_board")

    # Act/Assert
    snake = SnakeGame(game_size=6)
    with pytest.raises(RuntimeError, match="Could not generate a valid apple"):
        snake.generate_apples(new_apples=num_apples, seed=seed)


def test_move(mocker: MockFixture):
    # Arrange
    command_good = "drrrruull"
    mocker.patch.object(SnakeGame, "show_board")

    # Act
    snake = SnakeGame(game_size=6, num_apples=1)
    snake.move(command=command_good)

    # Assert
    assert len(snake.board.snake) == 3
    assert (
        np.sum(snake.board.state) == 3 + 2 + 1 + 1
    )  # apple + snake head + snake body + snake body


def test_move_error(mocker: MockFixture):
    # Arrange
    mocker.patch.object(SnakeGame, "show_board")

    # Act
    snake = SnakeGame()

    # Assert
    with pytest.raises(ValueError, match="Invalid letter"):
        snake.move(command="rru3")


@pytest.mark.parametrize(
    "new_loc, expected",
    [
        (np.array([1, 4]), True),
        (np.array([2, 1]), False),
        (np.array([-1, 1]), False),
        (np.array([3, 99]), False),
    ],
)
def test_check_new_loc(new_loc: np.array, expected: bool, mocker: MockFixture):
    # Arrange
    mocker.patch.object(SnakeGame, "show_board")

    # Act
    snake = SnakeGame(game_size=6, num_apples=1)
    output = snake.check_new_loc(loc=new_loc)

    # Assert
    assert output == expected


@pytest.mark.parametrize(
    "new_loc, expected", [(np.array([[5, 1]]), True), (np.array([[0, 0]]), False)]
)
def test_check_for_apple(new_loc: np.array, expected: bool, mocker: MockFixture):
    # Arrange
    mocker.patch.object(SnakeGame, "show_board")

    # Act
    snake = SnakeGame(game_size=6, num_apples=1)
    snake.board.apples = np.array([[4, 1], [5, 1]])
    output, _ = snake.check_for_apple(loc=new_loc)

    # Assert
    assert output == expected


@pytest.mark.parametrize(
    "apple, num_apples, snake_length, board_sum", [(True, 2, 4, 11), (False, 1, 3, 7)]
)
def test_update_board(
    apple: bool, num_apples: int, snake_length: int, board_sum: int, mocker: MockFixture
):
    # Arrange
    mocker.patch.object(SnakeGame, "show_board")
    new_snake = np.array([3, 1])
    apple_i = 1

    # Act
    snake = SnakeGame(game_size=6, num_apples=1)
    if apple:
        snake.board.apples = np.array([[5, 5], [3, 1]])
        snake.board.state[3, 1] = 3
    snake.update_board(new_snake=new_snake, apple=apple, apple_i=apple_i)

    # Assert
    assert len(snake.board.apples) == num_apples
    assert len(snake.board.snake) == snake_length
    assert np.sum(snake.board.state) == board_sum
