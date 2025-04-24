
# 8-Puzzle Game

## Introduction

The 8-puzzle is a classic sliding puzzle that consists of a 3×3 grid with 8 numbered square tiles and one empty position. The goal is to rearrange the tiles from a given starting configuration to reach the goal state, where all tiles are in numerical order (with the empty space in the top-left position).

This Python implementation provides a complete 8-puzzle game with both interactive and file-based command modes. It includes multiple search algorithms for automatically solving the puzzle, as well as tools for analyzing and comparing the performance of these algorithms.

## Features

- Interactive command-line interface
- File-based command execution
- Multiple solving algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A* Search with two different heuristics
- Performance analysis tools
- State visualization
- Puzzle scrambling functionality

## Installation

### Prerequisites

- Python 3.x
- Required libraries:
  - pandas
  - tabulate
  - random (standard library)
  - heapq (standard library)
  - math (standard library)
  - os (standard library)
  - sys (standard library)

### Installing Dependencies

```bash
pip install pandas tabulate
```

## Running the Program

### Interactive Mode

To start the program in interactive mode:

```bash
python EightPuzzle.py
```

This will open a command prompt where you can enter commands directly.

### File Mode

To execute commands from a file:

```bash
python EightPuzzle.py commands.txt
```

Where `commands.txt` is a text file containing the commands you want to execute.

## Commands

### Basic Commands

- `setState <tile1> <tile2> ... <tile9>`: Set the puzzle to a specific state (use 0 for the empty space)
- `printState`: Display the current puzzle state
- `move <direction>`: Move a tile in the specified direction (up, down, left, right)
- `scrambleState <n>`: Scramble the puzzle with n random moves
- `setSeed <seed>`: Set the random number generator seed
- `clear`: Clear the terminal screen
- `quit`: Exit the program (interactive mode only)

### Solving Commands

- `solve BFS [maxnodes=<number>]`: Solve using Breadth-First Search
- `solve DFS [maxnodes=<number>] [depthlimit=<number>]`: Solve using Depth-First Search
- `solve A* [heuristic=<h1|h2>] [maxnodes=<number>]`: Solve using A* search

### Analysis Commands

- `effectiveBranchingFactor <nodes_generated> <solution_depth>`: Calculate the effective branching factor
- `compareSearch [parameters]`: Compare different search algorithms
  - Parameters:
    - `bfs_maxnodes=<number>`
    - `dfs_depth_limit=<number>`
    - `dfs_maxnodes=<number>`
    - `astar_h1_maxnodes=<number>`
    - `astar_h2_maxnodes=<number>`

## Puzzle Representation

The puzzle is represented as a 1D array of 9 integers, where 0 represents the empty space. The 3×3 grid is flattened row by row:

```
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]
```

This is the goal state of the puzzle.

## Search Algorithms

### Breadth-First Search (BFS)

BFS explores the state space level by level, finding the shortest solution path. It's guaranteed to find the optimal solution but may use a lot of memory for complex puzzles.

```
solve BFS maxnodes=1000
```

### Depth-First Search (DFS)

DFS explores as far as possible along each branch before backtracking. It uses less memory than BFS but may not find the optimal solution.

```
solve DFS maxnodes=1000 depthlimit=31
```

### A* Search

A* uses heuristics to guide the search toward the goal state more efficiently. Two heuristics are implemented:

- `h1`: Number of misplaced tiles
- `h2`: Sum of Manhattan distances (typically more efficient)

```
solve A* heuristic=h2 maxnodes=1000
```

## Performance Analysis

The program includes tools to compare the performance of different search algorithms:

```
compareSearch bfs_maxnodes=10000 dfs_depth_limit=20000 dfs_maxnodes=10000000000 astar_h1_maxnodes=10000 astar_h2_maxnodes=10000
```

This will display a table comparing:
- Solution path length
- Number of nodes created during search
- Effective branching factor (b*)

## Examples

### Setting up a custom puzzle state

```
setState 1 2 3 4 0 5 6 7 8
printState
```

Output:
```
1 | 2 | 3
---------
4 | 0 | 5
---------
6 | 7 | 8
```

### Solving a scrambled puzzle

```
scrambleState 20
printState
solve A* heuristic=h2
```

### Creating a command file

Example `commands.txt`:
```
# This is a comment
setState 1 2 3 4 0 5 6 7 8
printState
solve BFS maxnodes=2000
```

## File Structure

- `EightPuzzle.py`: Main Python file containing the EightPuzzle class and command interface

## Implementation Details

### Effective Branching Factor

The effective branching factor (b*) is calculated using binary search to find the value b that satisfies:
```
N = 1 + b + b² + ... + bᵈ
```
where N is the number of nodes generated and d is the solution depth.

### State Representation

States are represented as tuples in the visited set for O(1) lookup time, improving search efficiency.

## Limitations

- The DFS algorithm has a depth limit to prevent infinite exploration
- All search algorithms have a maximum node limit to prevent excessive resource usage
- More complex puzzles may require higher limits for successful solving

## Troubleshooting

- If search algorithms fail to find a solution, try increasing the `maxnodes` parameter
- If DFS is not finding solutions, try increasing the `depthlimit` parameter
- Ensure the puzzle is in a solvable state (not all 8-puzzle configurations are solvable)

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Submit a pull request

## License

This project is available for educational and personal use.
