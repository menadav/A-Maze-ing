_This project has been created as part of the 42 curriculum by dmena-li, rmarin-n._

# A-Maze-ing

--- 
# Description
A-Maze-ing is a technical exploration into the world of graph theory and procedural generation.   
The objective of this project is to create a robust system capable of generating "perfect" mazes (mazes where any two points are connected by exactly one path) and providing automated solutions.

The project features a modular architecture that separates the generation logic from the visual rendering, allowing for easy expansion and testing of different mathematical approaches to maze construction.

--- 
# Instructions

## Prerequisites
Python 3.10 or higher.   
pip (for dependency management).

## Execution
You can run the project using the provided Makefile:

(This will automatically check requirements, install missing dependencies, and launch the application).
```
make run
```

To clean temporary files (__pycache__), venv and others:
```
make clean
```
--- 

# Project Architecture & Configuration
```
|-- Makefile
|-- a-maze-ing.py
|-- config.txt
|-- maze_app
|   |-- generator
|   |   |-- __init__.py
|   |   |-- generator.py
|   |   `-- pyproject.toml
|   |-- maze_class.py
|   |-- maze_types.py
|   |-- render
|   |   `-- render.py
|   |-- solver
|   |   |-- __init__.py
|   |   `-- solver.py
|   `-- utils.py
|-- parse
|   `-- config_parser.py
|-- requirements.txt
`-- validation
    `-- config_model.py
```

## Configuration File Format
The project uses a config.txt file located in the root directory. It follows a key-value pair format:
```
WIDTH=10
HEIGHT=10
ENTRY=0,0
EXIT=9,9
SEED=
ALGORITHM='bfs' or 'dfs'
OUTPUT_FILE=maze.txt
PERFECT=false
```

Colors: Supports ANSI escape codes for terminal styling.

--- 

# Technical Decisions
## Generator
Maze Generation Algorithm: 

    - Randomized Prim's
    - Randomized Dfs

## Why Prim's?
Performance: 

    - It is highly efficient for grid-based graphs.

Aesthetics: 

    - It creates a maze that looks more natural and is harder to solve by simply following one direction.

## Why Dfs?
Aesthetics:
    -  Creates long, winding corridors with fewer dead ends, resulting in a "deep" maze feel.

Complexity: 
    - Highly efficient using a Stack (LIFO), making it ideal for large grids where recursion depth isn't an issue.

--- 
## Solver
Maze Solving Algorithm:
    - BFS
    - DFS

## Why BFS?
Optimality: 
    - Guaranteed to find the shortest path in an unweighted grid.

Visuals: 
    - Excellent for demonstrating "flood-fill" exploration.

## Why DFS?
Memory Efficiency: 
    - Uses less memory than BFS as it only stores the current path, not the entire frontier.

Speed: 
    - Often finds a solution faster than BFS by diving deep into branches, even if it’s not the shortest one.


# Reusable Code

The core logic in maze_app/maze_types.py and maze_app/utils.py is strictly decoupled.  
The Bitmask Wall System using:
(NORTH, SOUTH, EAST, WEST values) 
is designed to be imported into any grid-based game or simulation beyond this project.

Bitmask Reference
|Direction  |	Binary	| Decimal |
|-----------|-----------|---------|
| NORTH	    |0001	    |   1     |
| SOUTH	    |0010	    |   2     |
| EAST	    |0100	    |   4     |
| WEST	    |1000	    |   8     |


--- 

# Resources
## Documentation:

- Wikipedia - [Maze Generation Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm).

## Tutorials:
- Jamis Buck’s "The Buckblog" - [Maze Generation: Prim's Algorithm](https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm)
---

## Use of AI

    - Refactoring: Optimized the render_ascii function to improve terminal refresh rates and handle complex bitmasking for walls and paths efficiently.

    - Algorithm Hardening (Debugging): Assisted in troubleshooting the "42" pattern protection logic, ensuring that the Randomized Prim's algorithm could flow around specific coordinates without breaking the visual integrity of the numbers.

    - Solver Implementation: Guided the structural design of the BFS (Breadth-First Search) and DFS (Depth-First Search) solvers, focusing on the correct use of data structures (Queue vs. Stack) to ensure path reconstruction accuracy.

    - Generator Logic: Provided insights into the bitwise operations used to manage wall states (NORTH, SOUTH, EAST, WEST), allowing for a highly modular and memory-efficient maze representation.

---

# Team and Project Management
## Roles
dmena-li: Algorithm Implementation (Generator & Solver) and Rendering Engine.

rmarin-n: System Architecture (Config Parser & Validation), modulation, added features and readme.

## Planning and Evolution
Planned: Linear development (Generator -> Solver -> Render).


## Retrospective
The modular structure allowed us to work on the Solver and Generator simultaneously without merge conflicts.

## Improvements: 
Implementing a GUI using pygame instead of just ASCII would be the next logical step.

## Tools Used
    - Git/GitHub: Version control.

    - Pydantic: For configuration validation.

    - Makefile: For automation.
