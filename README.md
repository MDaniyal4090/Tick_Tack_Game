# Flask Tic Tac Toe Game

A modern, responsive Tic Tac Toe game built with Flask, featuring a beautiful UI and smooth animations.

## Features

- Clean and modern user interface
- Responsive design that works on both desktop and mobile
- Smooth animations and transitions
- Game state management using Flask sessions
- Win detection and game over states
- Reset game functionality
- Winner announcement modal

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## How to Play

1. The game starts with Player X
2. Click on any empty cell to make a move
3. Players alternate turns between X and O
4. The first player to get three in a row (horizontally, vertically, or diagonally) wins
5. If all cells are filled and no player has won, the game is a tie
6. Click the "Reset Game" button to start a new game at any time

## Technologies Used

- Python Flask
- HTML5
- CSS3
- JavaScript
- Flask-Session
