# Sudoku - Custom Project
**Student name:** Ngo Gia Hy
**Student ID:** 106217563

## 1. Introduction
This project is inspired by the original Sudoku game and developed entirely using Python and the Pygame library. 

**Core algorithm and technology**
* **Logic Engine:** Using Recursive Backtracking algorithm for procedural board generation and puzzle-solving.
* **Data Integrity:** Integrates a Multiple Solutions Check via the `count_solutions()` function, guaranteeing that every generated puzzle has a unique Solution.
* **GUI Architecture:** Implements a Finite State Machine (FSM) to independently manage 4 game states (`MENU`, `PLAYING`, `WIN`, `GAMEOVER`), completely eliminating UI conflict bugs.

## 2. Installation and Execution
**Step 1:** Install pygame library
- Use the command below in your terminal/command prompt:
> pip install pygame

**Step 2:** Execute the program
- Launch the game using:
> python main.py

## 3. Features & Controls
* **Rules:** Input numbers into the blank cells, ensuring that no numbers are repeated in the same row, column, or 3x3 subgrid.
* **Difficulty Levels:** Press `1` for EASY, `2` for MEDIUM, or `3` for HARD.
* **Controls:**
  - `Left Click`: Select a cell.
  - `Number Keys (1-9)`: Input a number.
  - `Backspace`: Delete the number from the selected cell.

