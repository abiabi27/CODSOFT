import tkinter as tk
from tkinter import messagebox
import random

def check_winner(board, player):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def check_draw(board):
    return all(cell != "" for row in board for cell in row)

def minimax(board, depth, is_maximizing):
    if check_winner(board, "O"):
        return 1
    if check_winner(board, "X"):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ""
                    best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    best_score = -float("inf")
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = ""
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

def on_click(row, col):
    global current_player, board, game_over

    if board[row][col] == "" and not game_over:
        board[row][col] = current_player
        buttons[row][col].config(text=current_player)
        
        if check_winner(board, current_player):
            messagebox.showinfo("Tic Tac Toe", f"Player {current_player} wins!")
            game_over = True
        elif check_draw(board):
            messagebox.showinfo("Tic Tac Toe", "It's a draw!")
            game_over = True
        else:
            # CPU's turn
            if not game_over:
                cpu_row, cpu_col = find_best_move(board)
                board[cpu_row][cpu_col] = "O"
                buttons[cpu_row][cpu_col].config(text="O")

                if check_winner(board, "O"):
                    messagebox.showinfo("Tic Tac Toe", "CPU wins!")
                    game_over = True
                elif check_draw(board):
                    messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                    game_over = True
                else:
                    current_player = "X"

app = tk.Tk()
app.title("Tic Tac Toe")

current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]
game_over = False

buttons = [[None, None, None] for _ in range(3)]

for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(app, text="", font=("normal", 20), width=5, height=2,
                                  command=lambda row=i, col=j: on_click(row, col))
        buttons[i][j].grid(row=i, column=j)

app.mainloop()
