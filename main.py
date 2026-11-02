import os

import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PURPLE_BG,
    FPS,
    GAME_TITLE,
    TEXT_COLOR,
    GROUND_Y,
    PLAYER_START_X,
    SIGN_X,
    BADGE_SOUND,
)
from classes.ground import Ground
from classes.sign import Sign
from classes.player import Player
from classes.dialogue_bubble import DialogueBubble
from classes.level import LevelManager
from utils import DATA_DIR

pygame.init()
pygame.mixer.init()

# Configuration 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Objets du jeu
ground = Ground(GROUND_Y)
sign = Sign(SIGN_X, GROUND_Y)
player = Player(x=50, y=0)  
levels = LevelManager("data/levels.json")
bubble = DialogueBubble(screen, levels.levels, font_size=24, color=TEXT_COLOR)

# Position de départ du joueur : les pieds sur le sol
player.place(PLAYER_START_X, GROUND_Y)

# Son du badge
badge_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, BADGE_SOUND))

# Texte du jeu
pygame.font.init()
font = pygame.font.Font(None, 48)  
title_text = font.render("AIDE MAËVA À MONTER EN COMPÉTENCES", True, TEXT_COLOR)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))  

# Caméra : décalage horizontal entre le monde et l'écran
camera_x = 0

# On initialise le premier dialogue
bubble.set_level(levels.current_level)

# Vrai entre le ramassage du badge et la fermeture de la bulle
level_complete = False


def start_next_level():
    """Passe au niveau suivant : joueur au départ, caméra à 0, nouveau dialogue."""
    if levels.next_level():
        player.place(PLAYER_START_X, GROUND_Y)
        bubble.set_level(levels.current_level)
        return 0
    # Dernier niveau terminé : l'écran de fin arrive en 2.4
    return camera_x

# Boucle principale
running = True
while running:
    # ----- 1. ÉVÉNEMENTS -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Espace : afficher la bulle, accélérer le texte ou la fermer
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not bubble.visible:
                bubble.toggle()
            else:
                bubble.skip_or_hide()
                # Bulle du badge fermée : on enchaîne sur le niveau suivant
                if level_complete and not bubble.visible:
                    level_complete = False
                    camera_x = start_next_level()

    # ----- 2. LOGIQUE (coordonnées monde) -----
    keys = pygame.key.get_pressed()
    # Le joueur est figé pendant que la bulle du badge est ouverte
    if not level_complete:
        player.update(keys, GROUND_Y, levels.platforms, levels.width)

    # La caméra centre le joueur, bornée entre le début et la fin du niveau
    camera_x = player.rect.centerx - SCREEN_WIDTH // 2
    camera_x = max(0, min(camera_x, levels.width - SCREEN_WIDTH))

    # Badges : animation, puis ramassage (une seule fois grâce à `collected`)
    for badge in levels.badges:
        badge.update()
    for badge in levels.badges:
        if not badge.collected and player.rect.colliderect(badge.rect):
            badge.collect()
            badge_sound.play()
            # Bulle du niveau terminé ; le passage au suivant se fait à sa fermeture
            level_complete = True
            if not bubble.visible:
                bubble.toggle()

    # ----- 3. AFFICHAGE (coordonnées écran = monde - camera_x) -----
    screen.fill(PURPLE_BG)

    # Décor avant le joueur : sol infini puis plateformes du niveau
    ground.draw(screen, camera_x)
    sign.draw(screen, camera_x)
    for platform in levels.platforms:
        platform.draw(screen, camera_x)
    for badge in levels.badges:
        badge.draw(screen, camera_x)

    player.draw(screen, camera_x)
    bubble.draw()
    screen.blit(title_text, title_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
