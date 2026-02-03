_This project has been created as part of the 42 curriculum by dmena-li, rmarin-n._
# MazeGenerator

A high-performance standalone Python engine for generating and solving grid-based mazes. This module uses a **Bitmask Wall System** to represent grid geometry, allowing for fast generation and compact data storage.

## Installation

**Build the package**:
```bash
python3 -m build
```

```bash
pip install dist/mazegen-1.0.0.tar.gz
```

Then import it:

```python
from mazegen import MazeGenerator
```

---
## Features

* **Generation Algorithms**: 
    * `prim`: Randomized Prim's (organic, branched feel).
    * `dfs`: Randomized Depth-First Search (long, winding corridors).
* **Integrated Solvers**: 
    * `bfs`: Breadth-First Search (guarantees the shortest path).
    * `dfs`: Depth-First Search (memory-efficient exploration).
* **Perfect & Imperfect Mazes**: Supports "perfect" mazes (one unique solution) or "imperfect" mazes (adds loops based on area-calculated probability).
* **The "42" Secret**: Automatically carves the number "42" into the center for mazes larger than 15x15.

---

## Technical Reference: Bitmask System

The `grid` is a 2D list of integers. Every cell starts with a value of **15** (binary `1111`), meaning all four walls are closed.

| Direction | Value | Binary | Bit |
| :--- | :---: | :---: | :---: |
| **NORTH** | 1 | `0001` | 0 |
| **EAST** | 2 | `0010` | 1 |
| **SOUTH** | 4 | `0100` | 2 |
| **WEST** | 8 | `1000` | 3 |



---

## How It Works (Internal Logic)

### 1. The Carving Process (`_connect_cells`)
Instead of storing walls as objects, the generator "carves" paths using bitwise operators. To connect two cells, it performs a bitwise **NOT** and **AND** operation:
* To open a path to the **NORTH**, it executes: `cell &= ~Wall.NORTH`.
* This flips the bit at position 0 to `0`, effectively "removing" that wall.

### 2. Perfect vs Imperfect (`perfect: bool`)
* **Perfect Mazes (`True`)**: The algorithm ensures that every cell is reachable and there is **exactly one** unique path between any two points. No loops are allowed.
* **Imperfect Mazes (`False`)**: After the initial generation, the `_apply_imperfect_logic` method runs. It scans the grid and randomly removes extra walls (usually `EAST` walls) based on a calculated probability. This creates multiple paths, loops, and "braid" sections.

### 3. Dynamic Probability (`calculate_chance`)
The "imperfection" isn't fixed. It scales with the maze size:
* **Small mazes (< 9 cells)**: High chance (90%) of extra paths.
* **Large mazes (> 120 cells)**: Low chance (10%) to prevent the maze from becoming too open.

### 4. The "42" Pre-Carving
The `_write_42` method is a hardcoded coordinate pattern. Before the main algorithm starts, these coordinates are marked as **visited**. This forces the generation algorithm to build the rest of the maze *around* the number 42, integrating it perfectly into the navigable structure.

---

## Exportability & Integration

This module is designed to be **platform-agnostic**. Since the output is a raw matrix of integers:

* **Game Engines**: Easily export the `List[List[int]]` as a **JSON** file to be read by **Unity**, **Godot**, or **Unreal**.
* **Frontend**: Ideal for React/Vue canvas visualizations where each bit corresponds to a CSS border.
* **Solvability**: The solvers (`bfs`/`dfs`) return standard coordinate lists, making it easy to implement AI agents or "hint" systems in any external application.
