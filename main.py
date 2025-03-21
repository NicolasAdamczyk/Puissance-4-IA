import sys
import pygame
from constants import SQUARESIZE, ROW_COUNT, COLUMN_COUNT, PLAYER_PIECE, AI_PIECE
from game_logic import create_board, is_valid_location, get_next_open_row, drop_piece, winning_move
from ai import get_ai_move
from interface import draw_board, get_game_mode, get_difficulty, display_end_screen

def run_game(game_mode, difficulty, font, game_screen):
    """Exécute une partie avec les réglages donnés et retourne le message du vainqueur."""
    board = create_board()
    draw_board(board, game_screen)
    game_over = False
    turn = 0  # 0: Joueur 1, 1: Joueur 2 ou IA
    winner_message = ""
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = posx // SQUARESIZE
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    if turn == 0:
                        drop_piece(board, row, col, PLAYER_PIECE)
                        if winning_move(board, PLAYER_PIECE):
                            draw_board(board, game_screen)
                            winner_message = "Joueur 1 gagne!"
                            game_over = True
                    elif turn == 1:
                        if game_mode == "pvp":
                            drop_piece(board, row, col, AI_PIECE)
                            if winning_move(board, AI_PIECE):
                                draw_board(board, game_screen)
                                winner_message = "Joueur 2 gagne!"
                                game_over = True
                    draw_board(board, game_screen)
                    if not game_over:
                        turn = (turn + 1) % 2

        # Tour de l'IA pour le mode PvIA
        if game_mode == "pvai" and turn == 1 and not game_over:
            pygame.time.wait(500)
            col = get_ai_move(board, difficulty)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    draw_board(board, game_screen)
                    winner_message = "L'IA gagne!"
                    game_over = True
                draw_board(board, game_screen)
                if not game_over:
                    turn = (turn + 1) % 2
                    
    return winner_message

def main():
    pygame.init()
    font_menu = pygame.font.SysFont("Arial", 36)
    font = pygame.font.SysFont("Arial", 40)
    
    # Définir la taille de la fenêtre principale en 1280x720
    screen_width, screen_height = 1280, 720
    menu_screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Puissance 4 - Menu")
    
    while True:
        # Affichage du menu principal
        game_mode = get_game_mode(menu_screen, font_menu)
        difficulty = None
        if game_mode == "pvai":
            difficulty = get_difficulty(menu_screen, font_menu)
        
        # Boucle de jeu pour la session avec le même mode et difficulté
        while True:
            # Calculer la taille de la fenêtre de jeu en fonction du plateau
            board_width = COLUMN_COUNT * SQUARESIZE
            board_height = (ROW_COUNT + 1) * SQUARESIZE
            
            # Centrer la fenêtre de jeu dans l'écran 1280x720
            game_screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Puissance 4")
            
            # Calculer les offsets pour centrer le plateau
            offset_x = (screen_width - board_width) // 2
            offset_y = (screen_height - board_height) // 2
            
            # Dessiner le plateau centré
            game_screen.fill((0, 0, 0))  # Fond noir
            draw_board(board, game_screen, offset_x, offset_y)
            
            # Exécuter la partie et récupérer le message du vainqueur
            winner_message = run_game(game_mode, difficulty, font, game_screen)
            
            # Afficher l'écran de fin avec deux boutons : "Rejouer" et "Menu"
            result = display_end_screen(game_screen, font, winner_message)
            
            if result == "menu":
                # Retour au menu principal
                break
            elif result == "replay":
                # Rejoue avec les mêmes réglages en recommençant la partie
                continue
        
        # On revient ici pour réafficher le menu principal

if __name__ == "__main__":
    main()