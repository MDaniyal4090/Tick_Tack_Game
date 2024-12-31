from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    if 'board' not in session:
        reset_game_state()
    return render_template('index.html', 
                         board=session['board'], 
                         current_player=session['current_player'],
                         game_over=session['game_over'],
                         winner=session['winner'],
                         game_mode=session.get('game_mode', 'player'))

def reset_game_state():
    session['board'] = ['' for _ in range(9)]
    session['current_player'] = 'X'
    session['game_over'] = False
    session['winner'] = None
    session['game_mode'] = session.get('game_mode', 'player')

@app.route('/set_game_mode', methods=['POST'])
def set_game_mode():
    mode = request.json.get('mode')
    if mode not in ['player', 'computer']:
        return jsonify({'error': 'Invalid game mode'}), 400
    session['game_mode'] = mode
    reset_game_state()
    return jsonify({
        'board': session['board'],
        'current_player': session['current_player'],
        'game_over': session['game_over'],
        'winner': session['winner'],
        'game_mode': session['game_mode']
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    if session['game_over']:
        return jsonify({'error': 'Game is over'}), 400

    position = request.json.get('position')
    if not isinstance(position, int) or position < 0 or position > 8:
        return jsonify({'error': 'Invalid position'}), 400

    if session['board'][position]:
        return jsonify({'error': 'Position already taken'}), 400

    # Make the move
    session['board'][position] = session['current_player']
    
    # Check for win after move
    game_status = check_game_status()
    if game_status['game_over']:
        return jsonify(game_status)

    if session['game_mode'] == 'computer' and session['current_player'] == 'X':
        # If it's computer mode and player just moved, switch to O and make computer move
        session['current_player'] = 'O'
        computer_move = make_computer_move()
        if computer_move is not None:
            session['board'][computer_move] = 'O'
            game_status = check_game_status()
            if not game_status['game_over']:
                session['current_player'] = 'X'
            return jsonify(game_status)
    else:
        # Regular player switch for both modes
        session['current_player'] = 'O' if session['current_player'] == 'X' else 'X'
    
    return jsonify({
        'board': session['board'],
        'current_player': session['current_player'],
        'game_over': session['game_over'],
        'winner': session['winner'],
        'game_mode': session['game_mode']
    })

def make_computer_move():
    empty_cells = [i for i, cell in enumerate(session['board']) if cell == '']
    if not empty_cells:
        return None

    # Try to win
    for pos in empty_cells:
        session['board'][pos] = 'O'
        if check_winner(session['board']) == 'O':
            session['board'][pos] = ''
            return pos
        session['board'][pos] = ''

    # Block player's winning move
    for pos in empty_cells:
        session['board'][pos] = 'X'
        if check_winner(session['board']) == 'X':
            session['board'][pos] = ''
            return pos
        session['board'][pos] = ''

    # Take center if available
    if session['board'][4] == '':
        return 4

    # Take corners
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for corner in corners:
        if corner in empty_cells:
            return corner

    # Take any available edge
    edges = [1, 3, 5, 7]
    random.shuffle(edges)
    for edge in edges:
        if edge in empty_cells:
            return edge

    return random.choice(empty_cells)

def check_game_status():
    winner = check_winner(session['board'])
    if winner:
        session['game_over'] = True
        session['winner'] = winner
    elif all(cell != '' for cell in session['board']):
        session['game_over'] = True
        session['winner'] = 'Tie'
    
    return {
        'board': session['board'],
        'current_player': session['current_player'],
        'game_over': session['game_over'],
        'winner': session['winner'],
        'game_mode': session['game_mode']
    }

@app.route('/reset_game', methods=['POST'])
def reset_game():
    reset_game_state()
    return jsonify({
        'board': session['board'],
        'current_player': session['current_player'],
        'game_over': session['game_over'],
        'winner': session['winner'],
        'game_mode': session['game_mode']
    })

def check_winner(board):
    # Winning combinations
    lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    
    for line in lines:
        if board[line[0]] and board[line[0]] == board[line[1]] == board[line[2]]:
            return board[line[0]]
    return None

if __name__ == '__main__':
    app.run(debug=True)
