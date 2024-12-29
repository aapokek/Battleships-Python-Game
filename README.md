# Battleships Python Game

This repository contains a Python implementation of a one-player-per-computer **Battleship game**. Players load their ship placements from a file and take turns shooting coordinates on the map, aiming to sink their opponent's ships. The game is designed to work on Windows computers due to the use of the `winsound` module for audio effects.

---

## Features
- Interactive graphical interface built with **Tkinter**.
- Ships are loaded from a text file (`Battleships.txt`) that defines ship positions.
- Visual feedback for hits, misses, and sunk ships with optional image assets.
- Sound effects for hits and misses (Windows only).
- Clear game-ending condition when all enemy ships are destroyed.

---

## Gameplay Overview
1. **Setup**: Each player loads their ship placements from a text file (e.g., `Battleships.txt`).
    - The format should include ship names and coordinates separated by semicolons (e.g., `Destroyer;A1;A2`).
2. **Objective**: Take turns clicking on the grid to shoot at enemy ships.
3. **Endgame**: The game ends when one player destroys all of the other's ships.

---

## Prerequisites
- **Python 3.8+** installed on your machine.
- Required libraries:
  - `tkinter` (included with Python)
  - `winsound` (Windows-only)

---

## Important Notes:
- Ensure ship coordinates do not overlap.
- Only letters `A-J` and numbers `0-9` are valid for coordinates.