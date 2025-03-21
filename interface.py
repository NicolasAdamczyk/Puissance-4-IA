import pygame
import sys

class Button:
    def __init__(self, rect, text, font, bg_color, text_color, border_color=None, border_width=0):
        """
        Initialisation du bouton.
        - rect: tuple (x, y, width, height)
        - text: texte affiché sur le bouton
        - font: objet Font de pygame
        - bg_color: couleur de fond (RGB)
        - text_color: couleur du texte (RGB)
        - border_color: couleur de la bordure (RGB)
        - border_width: épaisseur de la bordure
        """
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_width = border_width
        self.hover_color = (  # Couleur plus claire pour le survol
            min(bg_color[0] + 50, 255),
            min(bg_color[1] + 50, 255),
            min(bg_color[2] + 50, 255)
        )

    def draw(self, screen, mouse_pos):
        """Dessine le bouton sur l'écran avec un effet de survol."""
        # Change la couleur si la souris est sur le bouton
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)

        if self.border_color and self.border_width:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        """Retourne True si la position pos est à l'intérieur du bouton."""
        return self.rect.collidepoint(pos)

def display_mode_menu(screen, font):
    """
    Affiche un menu sobre avec deux boutons disposés verticalement sur fond gris.
    Renvoie un dictionnaire de boutons pour la détection des clics.
    """
    gris = (50, 50, 50)
    bleu = (0, 0, 255)
    blanc = (255, 255, 255)
    
    screen.fill(gris)
    
    # Calcul dynamique de la taille des boutons avec padding
    padding_x, padding_y = 20, 10
    text_pvp = font.render("Joueur vs Joueur", True, blanc)
    text_pvai = font.render("Joueur vs IA", True, blanc)
    button_width = max(text_pvp.get_width(), text_pvai.get_width()) + 2 * padding_x
    button_height = max(text_pvp.get_height(), text_pvai.get_height()) + 2 * padding_y
    spacing = 40
    x = (screen.get_width() - button_width) // 2
    y1 = 200
    y2 = y1 + button_height + spacing
    
    button_pvp = Button(
        rect=(x, y1, button_width, button_height),
        text="Joueur vs Joueur",
        font=font,
        bg_color=bleu,
        text_color=blanc,
        border_color=blanc,
        border_width=2
    )
    button_pvai = Button(
        rect=(x, y2, button_width, button_height),
        text="Joueur vs IA",
        font=font,
        bg_color=bleu,
        text_color=blanc,
        border_color=blanc,
        border_width=2
    )
    
    # Récupère la position de la souris pour l'effet de survol
    mouse_pos = pygame.mouse.get_pos()
    button_pvp.draw(screen, mouse_pos)
    button_pvai.draw(screen, mouse_pos)
    pygame.display.update()
    
    return {"pvp": button_pvp, "pvai": button_pvai}

def get_game_mode(screen, font):
    """Attend que l'utilisateur clique sur un bouton et renvoie 'pvp' ou 'pvai'."""
    buttons = display_mode_menu(screen, font)
    mode = None
    while mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if buttons["pvp"].is_clicked(pos):
                    mode = "pvp"
                elif buttons["pvai"].is_clicked(pos):
                    mode = "pvai"
        # Change le curseur en mode pointer si la souris est sur un bouton
        mouse_pos = pygame.mouse.get_pos()
        if buttons["pvp"].is_clicked(mouse_pos) or buttons["pvai"].is_clicked(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    return mode

def display_difficulty_menu(screen, font):
    """
    Affiche le menu de choix de difficulté pour le mode PvIA avec trois boutons.
    Renvoie un dictionnaire de boutons.
    """
    screen.fill((50, 50, 50))
    title_text = font.render("Choisissez la difficulté", True, (255, 255, 255))
    screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 50))
    
    button_width, button_height = 180, 80
    spacing = 40
    total_width = 3 * button_width + 2 * spacing
    start_x = (screen.get_width() - total_width) // 2
    y = 200
    
    easy_button = Button(
        rect=(start_x, y, button_width, button_height),
        text="Facile",
        font=font,
        bg_color=(0, 0, 255),
        text_color=(255, 255, 255),
        border_color=(255, 255, 255),
        border_width=2
    )
    medium_button = Button(
        rect=(start_x + button_width + spacing, y, button_width, button_height),
        text="Moyen",
        font=font,
        bg_color=(0, 0, 255),
        text_color=(255, 255, 255),
        border_color=(255, 255, 255),
        border_width=2
    )
    hard_button = Button(
        rect=(start_x + 2 * (button_width + spacing), y, button_width, button_height),
        text="Difficile",
        font=font,
        bg_color=(0, 0, 255),
        text_color=(255, 255, 255),
        border_color=(255, 255, 255),
        border_width=2
    )
    
    # Récupère la position de la souris pour l'effet de survol
    mouse_pos = pygame.mouse.get_pos()
    easy_button.draw(screen, mouse_pos)
    medium_button.draw(screen, mouse_pos)
    hard_button.draw(screen, mouse_pos)
    pygame.display.update()
    
    return {"easy": easy_button, "medium": medium_button, "hard": hard_button}

def get_difficulty(screen, font):
    """Attend que l'utilisateur clique sur un bouton et renvoie la difficulté choisie."""
    buttons = display_difficulty_menu(screen, font)
    difficulty = None
    while difficulty is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if buttons["easy"].is_clicked(pos):
                    difficulty = "easy"
                elif buttons["medium"].is_clicked(pos):
                    difficulty = "medium"
                elif buttons["hard"].is_clicked(pos):
                    difficulty = "hard"
        # Change le curseur en mode pointer si la souris est sur un bouton
        mouse_pos = pygame.mouse.get_pos()
        if any(button.is_clicked(mouse_pos) for button in buttons.values()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    return difficulty

def draw_board(board, screen, offset_x=0, offset_y=0):
    """
    Affiche le plateau de jeu.
    - offset_x: décalage horizontal pour centrer le plateau
    - offset_y: décalage vertical pour centrer le plateau
    """
    from constants import SQUARESIZE, ROW_COUNT, COLUMN_COUNT, BLUE, BLACK, RED, YELLOW, RADIUS
    screen.fill(BLACK)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (offset_x + c * SQUARESIZE, offset_y + (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            color = BLACK
            if board[r][c] == 1:
                color = RED
            elif board[r][c] == 2:
                color = YELLOW
            pygame.draw.circle(screen, color, (offset_x + c * SQUARESIZE + SQUARESIZE // 2, offset_y + (r + 1) * SQUARESIZE + SQUARESIZE // 2), RADIUS)
    pygame.display.update()

def display_end_screen(screen, font, message):
    """
    Affiche l'écran de fin de jeu avec le plateau final, un overlay semi-transparent,
    un message de victoire et deux boutons : "Rejouer" pour relancer la partie au même niveau,
    et "Menu" pour revenir au menu principal.
    Renvoie "replay" ou "menu" selon le bouton cliqué.
    """
    final_surface = screen.copy()
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
    
    button_width, button_height = 250, 80
    spacing = 40
    total_width = 2 * button_width + spacing
    start_x = (screen.get_width() - total_width) // 2
    y = screen.get_height() // 2 + 20
    
    replay_button = Button(
        rect=(start_x, y, button_width, button_height),
        text="Rejouer",
        font=font,
        bg_color=(0, 0, 255),
        text_color=(255, 255, 255),
        border_color=(255, 255, 255),
        border_width=3
    )
    
    menu_button = Button(
        rect=(start_x + button_width + spacing, y, button_width, button_height),
        text="Menu",
        font=font,
        bg_color=(0, 0, 255),
        text_color=(255, 255, 255),
        border_color=(255, 255, 255),
        border_width=3
    )
    
    screen.blit(final_surface, (0, 0))
    screen.blit(overlay, (0, 0))
    screen.blit(text_surface, text_rect)
    # Récupère la position de la souris pour l'effet de survol
    mouse_pos = pygame.mouse.get_pos()
    replay_button.draw(screen, mouse_pos)
    menu_button.draw(screen, mouse_pos)
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if replay_button.is_clicked(pos):
                    return "replay"
                elif menu_button.is_clicked(pos):
                    return "menu"
        # Change le curseur en mode pointer si la souris est sur un bouton
        mouse_pos = pygame.mouse.get_pos()
        if replay_button.is_clicked(mouse_pos) or menu_button.is_clicked(mouse_pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)