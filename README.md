[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/hCr2pIQp)

# Escape Room AI Solver - Integrative Task 1 (APO III)

## Authors
- **Alejandro Mejía**

- **Santiago Angel Ordoñez**

- **Julio Prado**

## Objective

This project implements and compares different AI-based solvers for a multi-room escape room simulation. The primary goal is for an agent (the player) to find an optimal sequence of actions to navigate connected rooms, interact with objects (collect items, solve puzzles, find keys), unlock doors, and reach a final exit within a set turn limit. The project explores solutions using Logic Programming (Prolog) and Heuristic/Adversarial Search (Python).

## Game Versions & Approaches

This repository contains implementations exploring three distinct approaches to solving the escape room challenge:

1.  **Prolog-Based Solver:**
    Prolog integrated with Python using PySWIP. Models the escape room rules, object interactions, and navigation using logic programming principles. It leverages Prolog's inference engine to determine valid moves and potentially solve basic puzzles or provide hints based on defined logical rules. It also incorporate Constraint Logic Programming (CLP).

2.  **A\* Heuristic Search Solver:**
    Implements the A\* search algorithm to find the *optimal* path (minimum number of turns) from the start to the exit. It uses a state representation that includes player position, whether the item is held, and whether the puzzle is solved (key obtained). A custom Manhattan distance-based heuristic guides the search efficiently by estimating the remaining cost based on the current sub-goal (getting item, solving puzzle, reaching door).

3.  **A\* Search with Minimax Adversary:**
    Builds upon the A\* solver by introducing an adversarial agent (enemy). The Minimax algorithm is used to determine the enemy's moves. The enemy typically tries to *minimize* a score (representing a state favorable to the player), while the player implicitly aims to maximize it (by reaching the goal). The game state evaluation (`get_score`) considers relative positions of player, enemy, item, puzzle, and door to guide the Minimax decision-making.

## How to Run

### Prerequisites

*   `pytest` and `pytest-mock` (for running tests): `pip install pytest pytest-mock`
*   A Prolog environment and `PySWIP`.

### Menu
1.  Navigate to the project's root directory and run the `main.py` file.

2.  The script will present a menu:
    ```
    1. Escape Room Clásico (Prolog)
    2. Escape Room A*
    3. Enemy A*
    Enter -1 to exit
    ```
3.  Enter the number corresponding to the game version you wish to play (1, 2, or 3) and press Enter.
4.  To exit the menu, enter `-1`.


### Runing Tests
Navigate to the project's root directory in your terminal and run:
```bash
    pytest -s
```
