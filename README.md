# Breakthrough Board Game with AI

A Python-based implementation of a two-player board game featuring multiple AI strategies, including Minimax and Alpha-Beta pruning algorithms with different heuristic approaches.

## Project Overview

This project implements a strategic board game where players compete to either reach the opponent's side or capture all opposing pieces. The game features multiple AI strategies and a graphical interface built with Pygame.

### Key Features

- 8x8 board game implementation
- Multiple AI algorithms:
  - Minimax (depth 3)
  - Alpha-Beta Pruning (depth 4)
- Four different heuristic strategies:
  - Two offensive strategies
  - Two defensive strategies
- Performance metrics tracking
- Interactive GUI with Pygame

## Game Rules

- Initial Setup: 8x8 board with 16 pieces per player
- Movement:
  - Pieces can move one square forward
  - Pieces can move diagonally forward
- Capture: Diagonal moves can capture opponent pieces
- Victory Conditions:
  - Reach opponent's home base (last row)
  - Capture all opponent's pieces

## Setup Instructions

1. Prerequisites:
   ```bash
   pip install numpy pygame
   ```

2. File Structure:
   ```
   project_directory/
   ├── game.py
   └── imagesFolder/
       ├── chessboard.jpg
       ├── Pawn_Black_Color.png
       ├── Pawn_White_Color.png
       ├── reset.png
       ├── trophy.png
       └── [1-6].png
   ```

3. Run the Game:
   ```bash
   python game.py
   ```

## Game Controls

- Purple Reset Button: Restart the game
- Strategy Buttons:
  1. Minimax (Offensive 1) vs Alpha-beta (Offensive 1)
  2. Alpha-beta (Offensive 2) vs Alpha-beta (Defensive 1)
  3. Alpha-beta (Defensive 2) vs Alpha-beta (Offensive 1)
  4. Alpha-beta (Offensive 2) vs Alpha-beta (Offensive 1)
  5. Alpha-beta (Defensive 2) vs Alpha-beta (Defensive 1)
  6. Alpha-beta (Offensive 2) vs Alpha-beta (Defensive 2)

## AI Implementation Details

### Heuristic Strategies

1. Offensive Heuristic 1
   - Focuses on capturing opponent pieces
   - Weighs opponent score reduction heavily

2. Defensive Heuristic 1
   - Prioritizes protecting own pieces
   - Focuses on maintaining piece count

3. Offensive Heuristic 2
   - Balanced approach between advancement and captures
   - Considers both position and capture opportunities

4. Defensive Heuristic 2
   - Strategic defense with counter-attack possibilities
   - Equal weight to piece protection and positioning

### Performance Tracking

The game tracks various metrics:
- Number of nodes explored in search tree
- Time taken per move
- Capture statistics
- Average blocks traversed per move

## Technical Details

- Language: Python 3.x
- Libraries:
  - Pygame: GUI implementation
  - NumPy: Array operations
- AI Algorithms:
  - Minimax with depth 3
  - Alpha-Beta Pruning with depth 4

## Game Interface

- Main game board (8x8 grid)
- Visual indicators for:
  - Current player
  - Valid moves
  - Captured pieces
  - Game status
- Strategy selection buttons
- Reset functionality

## Requirements

- Python 3.x
- Required packages:
  ```
  numpy>=1.21.0
  pygame>=2.5.2
  ```

## Acknowledgments

This project was developed as an implementation of the Breakthrough board game, focusing on AI strategy development and algorithm optimization. It demonstrates the practical application of various game theory concepts and search algorithms.