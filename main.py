import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PURPLE_BG,
    FPS,
    GAME_TITLE,
    TEXT_COLOR,
    PLAYER_OFFSET_Y
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
player = Player(x=50, y=0)  

# Ajuste la position Y du joueur APRÈS création
player.rect.bottom = platform.rect.top + PLAYER_OFFSET_Y

# Texte du jeu
pygame.font.init()
font = pygame.font.Font(None, 48)  
title_text = font.render("AIDE MAËVA À MONTER EN COMPÉTENCES", True, TEXT_COLOR)
title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))  

# Scroll
scroll_x = 0

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ----- LOGIQUE DU JEU -----
    keys = pygame.key.get_pressed()
    
    
    # Effet parallaxe : on décale le sol au lieu de déplacer l'écran
    if keys[pygame.K_LEFT]:
        scroll_x += player.speed  
    elif keys[pygame.K_RIGHT]:
        scroll_x -= player.speed  


    # ----- AFFICHAGE -----
    screen.fill(PURPLE_BG)          # fond
    platform.draw(screen)           # sol
    player.draw(screen)             # personnage
    
    
    # Dessiner le sol avec répétition pour l'effet infini 
    platform_width = platform.image.get_width()
    for i in range(-1, SCREEN_WIDTH // platform_width + 2):
        x_pos = i * platform_width + (scroll_x % platform_width)
        screen.blit(platform.image, (x_pos, platform.rect.y))
    
     # Texte
    screen.blit(title_text, title_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
