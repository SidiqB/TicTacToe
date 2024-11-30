import tkinter as tk
import random

# Constants
PLAYER = 'X'
AI = 'O'
EMPTY = ' '

# Initialize the board
def initialize_board():
    return [[EMPTY, EMPTY, EMPTY] for _ in range(3)]

# Check if the game has ended (win or draw)
def check_winner(board):
    # Check rows and columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    # Check for draw (no empty spaces)
    if all(board[i][j] != EMPTY for i in range(3) for j in range(3)):
        return 'Draw'

    return None  # Game still ongoing

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == AI:
        return 10 - depth
    elif winner == PLAYER:
        return depth - 10
    elif winner == 'Draw':
        return 0

    if is_maximizing:
        best = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = EMPTY
        return best
    else:
        best = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = EMPTY
        return best

# Get the best move for AI
def get_best_move(board):
    best_val = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                move_val = minimax(board, 0, False)
                board[i][j] = EMPTY
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    return best_move

# Create the main application window
class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        
        self.board = initialize_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        # Create the buttons for the grid
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text=EMPTY, font=('normal', 40), height=2, width=5,
                                   command=lambda i=i, j=j: self.player_move(i, j))
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    # Handle player's move
    def player_move(self, i, j):
        if self.board[i][j] == EMPTY:
            self.board[i][j] = PLAYER
            self.buttons[i][j].config(text=PLAYER)
            winner = check_winner(self.board)
            if winner:
                self.handle_winner(winner)
            else:
                self.ai_move()

    # AI's move using Minimax algorithm
    def ai_move(self):
        print("AI is thinking...")
        i, j = get_best_move(self.board)
        self.board[i][j] = AI
        self.buttons[i][j].config(text=AI)
        winner = check_winner(self.board)
        if winner:
            self.handle_winner(winner)

    # Handle the winner or draw
    def handle_winner(self, winner):
        if winner == 'Draw':
            result = "It's a draw!"
        else:
            result = f"{winner} wins!"
        print(result)
        self.show_result(result)

    # Show result in a pop-up message box
    def show_result(self, result):
        result_window = tk.Toplevel(self.root)
        result_window.title("Game Over")
        result_label = tk.Label(result_window, text=result, font=("Arial", 20))
        result_label.pack(pady=20)
        play_again_button = tk.Button(result_window, text="Play Again", command=self.play_again)
        play_again_button.pack(pady=10)

    # Restart the game
    def play_again(self):
        self.board = initialize_board()
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=EMPTY)
        self.root.update()

# Create the main window and run the game
root = tk.Tk()
app = TicTacToeApp(root)
root.mainloop()