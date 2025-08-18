import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PURPLE_BG,
    FPS,
    GAME_TITLE
)
from classes.platform import Platform
from classes.player import Player

pygame.init()

# Configuration 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()

# Objets du jeu
platform = Platform(y_pos=380) 
player = Player(x=100, y=300)

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- LOGIQUE DU JEU -----
    keys = pygame.key.get_pressed()
    player.update(keys)

    # ----- AFFICHAGE -----
    screen.fill(PURPLE_BG)          # fond
    platform.draw(screen)           # sol
    player.draw(screen)             # personnage

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
