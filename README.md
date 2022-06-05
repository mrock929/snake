# Snake

This repo contains code that allows users to play the classic game Snake.

## Repo setup
1. Clone the repo from github using `git clone repo-address`
2. Create and enter a virtual environment
3. Install requirements with `pip install -r requirements.txt` from the project root. `conda install --file requirements.txt` can also be used

## Playing the game

1. You can type `jupyter lab` to open up Jupyter Lab. Create a new notebook.
2. Start the game
   1. Add `from snake_game import SnakeGame` to get the game class
   2. Instantiate the class with `snake = SnakeGame(game_size=#, num_apples=#)`. Here the `#` should be replaced with whatever numbers you want to use for the game. `game_size` is the length and width of the game board and `num_apples` is how many apples are present at a time in the game.
3. Play the game
   1. Apples are shown in black, the head of the snake in dark gray, and the body of the snake in gray
   2. The snake can be moved with `snake.move('command')` where `'command'` is a string of directions. Valid directions are u, d, l, and r for up, down, left, and right, respectively. Multiple directions can be used in a single command. An example of a valid command is `dddrru` to move down 3 times, then right twice, and then up once.
   3. See how high of a score you can get!

# Running tests
Tests can be run from the virtual environment using `pytest` from the project root