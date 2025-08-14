import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PURPLE_BG,
    FPS,
    GAME_TITLE
)
from classes.platform import Platform

pygame.init()

# Configuration de la fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)
clock = pygame.time.Clock()
platform = Platform(y_pos=200) 


# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # BG
    screen.fill(PURPLE_BG)
    
    #------Eléments du jeu ici------
   
    platform.draw(screen)
    
    
    
    
    
    
    
    #-------------------------------

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Limite les FPS
    clock.tick(FPS)


pygame.quit()
