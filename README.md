# Raccoon's Revenge

## Table of Contents
1. [Overview](#overview)
2. [Gameplay](#gameplay)
3. [Features](#features)
4. [Technologies Used](#technologies-used)
5. [Game Mechanics](#game-mechanics)
7. [How to Play](#how-to-play)
8. [Future Improvements](#future-improvements)
9. [Acknowledgments](#acknowledgments)

---

## Overview
**Raccoon's Revenge** is a grid-based simulation game similar to Rodent's Revenge, where players take control of the player character and interact with raccoons and smart raccoons navigating a shared environment. The goal is to implement movement, interactions, and game mechanics. The score is determined based on the number of trapped raccoons, as well as the maximum number of adjacent recycling bins. The game demonstrates object-oriented programming principles and provides an engaging way to explore Python's capabilities.

---

## Gameplay
In **Raccoon's Revenge**, players simulate a grid environment where characters (raccoons and pandas) interact with trash cans and navigate obstacles:
- Raccoons collect trash to earn points.
- Pandas serve as opponents and can block paths or interact with trash in unique ways.
- Trash cans spawn randomly on the grid and provide points when collected.

---

## Features
- **Grid-Based Environment**: The game simulates a dynamic grid environment with real-time interactions.
- **Object-Oriented Design**: Character behaviors, grid elements, and interactions are implemented using Python's OOP principles.
- **Event Handling**: Real-time movement and interaction between game objects.
- **Dynamic Challenges**: Randomized trash can placements and character behaviors increase replayability.
- **Visual Feedback**: ASCII or simple visuals to depict the grid state and movements.

---

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - `unittest` for testing
  - `random` for grid and object placement
- **Concepts**:
  - Object-Oriented Programming (OOP)
  - Event-driven programming
  - Grid-based simulations

---

## Game Mechanics
1. **Grid Design**:
   - The game operates on a fixed-size grid where raccoons, pandas, and trash cans are placed.
   - Each grid cell can hold one object, and the game updates as characters move.

2. **Character Movement**:
   - Characters move in response to player input or predefined behaviors.
   - Raccoons can move up, down, left, or right to collect trash.
   - Pandas move in patterns to obstruct raccoons.

3. **Scoring System**:
   - Points are awarded for each trash can collected.
   - The game ends when all trash cans are cleared or a time limit is reached.

4. **Randomized Trash Placement**:
   - Trash cans appear in random grid positions at the start of each game.

---

## How to Play
Each character takes up exactly one tile, except that a raccoon can crawl inside an open garbage can, in which case there will be two characters (a raccoon and a garbage can) on the same tile.

Some characters are movable (the main player, raccoons, and recycling bins) while others are static (garbage cans). Some of the movable characters can take turns (the main player and raccoons). Each turn-taking character can move exactly one tile on its turn, in one of the following directions: up, down, left or right. Raccoons are given turns less frequently than the main player.

When the game starts, the player is placed on the top-left corner. Raccoons, garbage cans and recycling bins are placed randomly on the board. Two types of raccoons exist in the game: regular raccoons and smart raccoons (with glasses), that move randomly or smartly respectively, aiming to crawl inside the garbage cans.

When a raccoon reaches an unoccupied, unlocked garbage can, it crawls inside and stays there. If the garbage can is locked, the raccoon will use up its turn to unlock it.

The player’s objective is to prevent the raccoons from getting into the garbage cans by trapping them with recycling bins, while trying to keep as many recycling bins clumped together as possible. We want to trap the raccoons, but we do not want to leave recycling bins all over the neighbourhood in doing so!

The player moves using the four arrow keys and pushes around the recycling bins in an attempt to trap the raccoons.

Recycling bins can’t move autonomously but can be pushed by the main player in the hope of trapping the raccoons. When pushed by the main player, a recycling bin moves in the same direction as the player. If the new tile happens to be occupied with another recycling bin, this recycling bin is also moved in the same direction as well. If there is a row or column of recycling bins being pushed, they all move. A raccoon is considered trapped if it is surrounded in all four directions (diagonals don’t matter) by recycling bins, other raccoons (including ones in garbage cans), the player, or the border of the game board.

The game ends once all raccoons are either trapped or inside garbage cans.

When the game ends, your score is displayed. The score is determined based on the number of trapped raccoons, as well as the maximum number of adjacent recycling bins.

Note that sometimes you may get into a game state where it will become impossible for the game to end (i.e. you can’t possibly trap the remaining raccoons). You will just need to close the game window. In this case, you never see a score.
   
## Acknowledgements
This project was inspired by the classic game Rodent's Revenge and was developed as part of a Python programming course. Special thanks to the course instructors and teaching assistants for their guidance.
