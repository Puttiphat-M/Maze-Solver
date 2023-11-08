# Maze Solver Application

## Introduction
This Python application allows the user to solve mazes using the A* algorithm implemented in Prolog. The user can select the grid size (8x8, 10x10, or 12x12), choose the start and end positions, and add walls to the maze. The Python script will then call a Prolog file containing the A* function, which will return the shortest path. The Python script will then display the shortest path to the user.

## Requirements
- Python 3.x
- SWI-Prolog

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/Puttiphat-M/Maze-Solver.git
   ```

2. Navigate to the project directory:
   ```
   cd Maze-Solver/ui
   ```

3. Run the Python script:
   ```
   python selectionUI.py
   ```

4. Follow the on-screen instructions to:
   - Select the grid size (8x8, 10x10, or 12x12).
   - Choose the start position and end position.
   - Add walls to the maze by clicking on the grid cells.

5. Once you're satisfied with the maze configuration, press `Solve` to solve the maze.

6. The Python script will call the Prolog file (`aStar.pl`) which contains the A* function. The Prolog code will find the shortest path and return it to the Python script.

7. The Python script will then display the shortest path on the grid for the user to see.

## Files

- `mazeSetup.py`: Python script responsible for user interaction, and grid visualization.
- `aStar.pl`: Prolog file containing the A* algorithm implementation.
- `grid.py`: Python module for generating and visualizing the grid.
- `selectionUI.py`: Python script responsible for selecting the grid size page.
- `resultMaze.py`: Python script responsible for displaying the shortest path.
- `prolog.py`: Python script responsible for calling the Prolog file.
- `README.md`: This file.
