# Snake Game Project

A simple Snake game implementation that demonstrates separation of game logic from display interface.

---

## Project Structure

```plaintext

snake_game/
├── core.py # Core game logic
├── test.py # Tests for core logic
├── game.py # PyGame display interface
├── game_fancy.py # Enhanced PyGame display interface
└── readme.md # This file

```

## Setup

Create a virtual environment with VSCode and install PyGame:

- Ctrl/Cmd + Shift + P to open the command palette
- Python: Create Environment and keep pressing Enter
  - If done succssfully, you should see a `.venv` folder in the root directory
- Open your terminal and run `pip install pygame`

## Running the Tests

To run the tests, run the following command in the terminal:

```bash
python test.py
```

## Running the Game

To play the basic game, run the following command in the terminal:

```bash
python game.py
```

To play an enhanced, fancier version of the game, run the following command in the terminal:

```bash
python game_fancy.py
```

---
