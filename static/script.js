document.addEventListener('DOMContentLoaded', () => {
    const board = document.getElementById('board');
    const cells = document.querySelectorAll('.cell');
    const status = document.getElementById('status');
    const resetButton = document.getElementById('reset-button');
    const modal = document.getElementById('winner-modal');
    const winnerText = document.getElementById('winner-text');
    const playAgainButton = document.getElementById('play-again');
    const modeButtons = document.querySelectorAll('.mode-button');

    let isProcessingMove = false;

    cells.forEach(cell => {
        cell.addEventListener('click', handleCellClick);
    });

    resetButton.addEventListener('click', resetGame);
    playAgainButton.addEventListener('click', resetGame);

    modeButtons.forEach(button => {
        button.addEventListener('click', () => {
            const mode = button.dataset.mode;
            setGameMode(mode);
            
            // Update active button styles
            modeButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
        });
    });

    function setGameMode(mode) {
        fetch('/set_game_mode', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mode: mode })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }
            updateBoard(data);
        })
        .catch(error => console.error('Error:', error));
    }

    function handleCellClick(e) {
        if (isProcessingMove) return;
        
        const cell = e.target;
        const position = cell.dataset.index;

        isProcessingMove = true;
        fetch('/make_move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ position: parseInt(position) })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }
            updateBoard(data);
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            isProcessingMove = false;
        });
    }

    function updateBoard(data) {
        data.board.forEach((value, index) => {
            cells[index].textContent = value;
            cells[index].className = 'cell ' + value;
        });

        status.innerHTML = `Current Player: <span id="current-player">${data.current_player}</span>`;

        if (data.game_over) {
            showWinnerModal(data.winner);
        }
    }

    function showWinnerModal(winner) {
        winnerText.textContent = winner === 'Tie' ? "It's a Tie!" : `Player ${winner} Wins!`;
        modal.classList.add('show');
    }

    function resetGame() {
        if (isProcessingMove) return;
        
        fetch('/reset_game', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            updateBoard(data);
            modal.classList.remove('show');
        })
        .catch(error => console.error('Error:', error));
    }
});
