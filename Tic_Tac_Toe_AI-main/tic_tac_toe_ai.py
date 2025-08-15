import tkinter as tk
from tkinter import messagebox
import random

# Constants for game pieces and board state
PLAYER = "X"
AI = "O"
EMPTY = ""

class TicTacToe:
    """
    Implements a Tic-Tac-Toe game with an AI opponent using the Minimax algorithm,
    featuring selectable difficulty levels (Easy, Normal, Hard).
    """
    def __init__(self, root):
        """
        Initializes the TicTacToe game.

        Args:
            root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("AI Tic Tac Toe (Minimax)") # Set window title
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)] # 3x3 game board
        self.buttons = [[None for _ in range(3)] for _ in range(3)] # Tkinter buttons for each cell
        self.game_over = False # Flag to indicate if the game has ended
        self.difficulty = "Hard"  # Default difficulty setting

        self.create_board() # Create the game board UI
        self.create_difficulty_buttons() # Create buttons for difficulty selection

    def create_board(self):
        """
        Creates the 3x3 grid of buttons for the Tic-Tac-Toe board
        and adds a restart button.
        """
        for i in range(3):
            for j in range(3):
                # Create a button for each cell on the board
                btn = tk.Button(self.root, text="", font=("Helvetica", 32), width=5, height=2,
                                command=lambda row=i, col=j: self.player_move(row, col))
                btn.grid(row=i, column=j) # Place button in the grid
                self.buttons[i][j] = btn # Store button reference

        # Create and place the restart button below the game board
        restart_btn = tk.Button(self.root, text="Restart", font=("Helvetica", 14),
                                command=self.restart_game, bg="orange", fg="white")
        restart_btn.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10)

    def create_difficulty_buttons(self):
        """
        Creates a frame with buttons to select the AI's difficulty level.
        """
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.grid(row=4, column=0, columnspan=3, pady=5) # Place frame below restart button

        # Easy difficulty button
        easy_btn = tk.Button(difficulty_frame, text="Easy", font=("Helvetica", 12),
                             command=lambda: self.set_difficulty("Easy"), bg="#4CAF50", fg="white")
        easy_btn.pack(side=tk.LEFT, padx=5)

        # Normal difficulty button
        normal_btn = tk.Button(difficulty_frame, text="Normal", font=("Helvetica", 12),
                               command=lambda: self.set_difficulty("Normal"), bg="#2196F3", fg="white")
        normal_btn.pack(side=tk.LEFT, padx=5)

        # Hard difficulty button
        hard_btn = tk.Button(difficulty_frame, text="Hard", font=("Helvetica", 12),
                             command=lambda: self.set_difficulty("Hard"), bg="#F44336", fg="white")
        hard_btn.pack(side=tk.LEFT, padx=5)

    def set_difficulty(self, level):
        """
        Sets the AI difficulty level and restarts the game.

        Args:
            level (str): The chosen difficulty level ("Easy", "Normal", or "Hard").
        """
        self.difficulty = level
        messagebox.showinfo("Difficulty Set", f"Difficulty set to {self.difficulty}. Starting a new game.")
        self.restart_game() # Restart the game with the new difficulty

    def player_move(self, row, col):
        """
        Handles a player's move.

        Args:
            row (int): The row index of the chosen cell.
            col (int): The column index of the chosen cell.
        """
        # Only allow a move if the cell is empty and the game is not over
        if self.board[row][col] == EMPTY and not self.game_over:
            self.board[row][col] = PLAYER # Update board with player's move
            self.buttons[row][col].config(text=PLAYER, state="disabled", fg="blue") # Update button appearance

            # Check for game end conditions after player's move
            if self.check_winner(self.board, PLAYER):
                self.end_game("You Win!")
            elif self.is_draw(self.board):
                self.end_game("It's a Draw!")
            else:
                # If game continues, schedule AI's move after a short delay
                self.root.after(300, self.ai_move)

    def ai_move(self):
        """
        Determines and executes the AI's move based on the current difficulty.
        """
        if self.game_over: # Prevent AI from moving if game is already over
            return

        if self.difficulty == "Easy":
            self.make_easy_move()
        elif self.difficulty == "Normal":
            self.make_normal_move()
        else:  # self.difficulty == "Hard"
            self.make_hard_move()

    def make_hard_move(self):
        """
        Calculates and executes the optimal AI move using the Minimax algorithm.
        """
        best_score = float('-inf')
        best_move = None
        # Iterate through all possible moves to find the best one
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = AI  # Try this move
                    # Recursively call minimax to evaluate the score of this move
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = EMPTY  # Undo the move

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        self._apply_ai_move(best_move) # Apply the best move found

    def make_normal_move(self):
        """
        Makes a move for the "Normal" difficulty AI.
        Has a chance to make an optimal move or a random move.
        """
        empty_cells = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == EMPTY:
                    empty_cells.append((r, c))

        if not empty_cells:
            self.end_game("It's a Draw!")
            return

        # 70% chance to make an optimal (hard) move, 30% chance for a random move
        if random.random() < 0.7:
            self.make_hard_move() # Call the hard move logic
        else:
            r, c = random.choice(empty_cells) # Pick a random empty cell
            self._apply_ai_move((r, c)) # Apply the random move

    def make_easy_move(self):
        """
        Makes a move for the "Easy" difficulty AI, which is always a random move.
        """
        empty_cells = []
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == EMPTY:
                    empty_cells.append((r, c))

        if not empty_cells:
            self.end_game("It's a Draw!")
            return

        r, c = random.choice(empty_cells) # Pick a random empty cell
        self._apply_ai_move((r, c)) # Apply the random move

    def _apply_ai_move(self, move):
        """
        Applies the AI's chosen move to the board and checks for game end conditions.

        Args:
            move (tuple): A tuple (row, col) representing the AI's chosen move.
        """
        if move and not self.game_over:
            i, j = move
            self.board[i][j] = AI # Update board with AI's move
            self.buttons[i][j].config(text=AI, state="disabled", fg="red") # Update button appearance

            # Check for game end conditions after AI's move
            if self.check_winner(self.board, AI):
                self.end_game("AI Wins!")
            elif self.is_draw(self.board):
                self.end_game("It's a Draw!")

    def minimax(self, board, depth, is_maximizing):
        """
        The Minimax algorithm to determine the best move.

        Args:
            board (list of list): The current state of the game board.
            depth (int): The current depth of the search tree.
            is_maximizing (bool): True if the current player is the maximizing player (AI),
                                  False if it's the minimizing player (Human).

        Returns:
            int: The score of the current board state from the perspective of the AI.
        """
        # Base cases: Check for winner or draw
        if self.check_winner(board, AI):
            return 1 # AI wins
        elif self.check_winner(board, PLAYER):
            return -1 # Player wins
        elif self.is_draw(board):
            return 0 # It's a draw

        if is_maximizing:
            best = float('-inf') # Initialize best score for AI (maximizing)
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = AI
                        score = self.minimax(board, depth + 1, False) # Recurse for player's turn
                        board[i][j] = EMPTY # Undo the move
                        best = max(best, score) # Take the maximum score
            return best
        else:
            best = float('inf') # Initialize best score for player (minimizing)
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        board[i][j] = PLAYER
                        score = self.minimax(board, depth + 1, True) # Recurse for AI's turn
                        board[i][j] = EMPTY # Undo the move
                        best = min(best, score) # Take the minimum score
            return best

    def check_winner(self, board, player):
        """
        Checks if the given player has won the game on the current board.

        Args:
            board (list of list): The current state of the game board.
            player (str): The player ('X' or 'O') to check for a win.

        Returns:
            bool: True if the player has won, False otherwise.
        """
        # Check rows
        for i in range(3):
            if all(board[i][j] == player for j in range(3)): return True
        # Check columns
        for i in range(3):
            if all(board[j][i] == player for j in range(3)): return True
        # Check main diagonal
        if all(board[i][i] == player for i in range(3)): return True
        # Check anti-diagonal
        if all(board[i][2 - i] == player for i in range(3)): return True
        return False

    def is_draw(self, board):
        """
        Checks if the game is a draw (all cells are filled and no winner).

        Args:
            board (list of list): The current state of the game board.

        Returns:
            bool: True if the game is a draw, False otherwise.
        """
        return all(cell != EMPTY for row in board for cell in row)

    def end_game(self, message):
        """
        Ends the game, displays a message, and disables all buttons.

        Args:
            message (str): The message to display (e.g., "You Win!", "AI Wins!").
        """
        self.game_over = True
        messagebox.showinfo("Game Over", message) # Show game over message
        # Disable all buttons to prevent further moves
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state="disabled")

    def restart_game(self):
        """
        Resets the game board and state to start a new game.
        """
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)] # Clear the board
        self.game_over = False # Reset game over flag
        # Re-enable and clear text for all buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal", fg="black") # Reset text color too

# Main part of the script to run the game
if __name__ == "__main__":
    root = tk.Tk() # Create the main Tkinter window
    game = TicTacToe(root) # Initialize the TicTacToe game
    root.mainloop() # Start the Tkinter event loop
