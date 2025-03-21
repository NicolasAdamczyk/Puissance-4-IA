# game_logic.py
import numpy as np
from constants import ROW_COUNT, COLUMN_COUNT, WINDOW_LENGTH, PLAYER_PIECE, AI_PIECE

def create_board():
    """Crée et retourne un plateau vide."""
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def is_valid_location(board, col):
    """Vérifie si la colonne est jouable (non pleine)."""
    return board[0][col] == 0

def get_next_open_row(board, col):
    """Retourne l’indice de la prochaine ligne vide dans la colonne donnée."""
    for r in range(ROW_COUNT-1, -1, -1):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    """Dépose une pièce dans le plateau."""
    board[row][col] = piece

def winning_move(board, piece):
    """Teste si la pièce donnée forme une combinaison gagnante."""
    # Vérification horizontale
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if all(board[r][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    # Vérification verticale
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c] == piece for i in range(WINDOW_LENGTH)):
                return True
    # Vérification diagonale (positive)
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if all(board[r + i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    # Vérification diagonale (négative)
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if all(board[r - i][c + i] == piece for i in range(WINDOW_LENGTH)):
                return True
    return False
