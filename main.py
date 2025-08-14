import pygame

# --- Initialisation de Pygame ---
pygame.init()

# --- Configuration de la fenêtre ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hack Ton Job - CV Game")

# --- Couleur de fond (branding violet pastel) ---
BACKGROUND_COLOR = (43, 14, 63)  # #2B0E3F en RGB

# --- Configuration du framerate ---
clock = pygame.time.Clock()
FPS = 60

# --- Boucle principale ---
running = True
while running:
    # --- Gestion des événements ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Dessin de l'écran ---
    screen.fill(BACKGROUND_COLOR)

    # --- Rendu du jeu (à compléter avec tes sprites/classes plus tard) ---

    # --- Mise à jour de l'affichage ---
    pygame.display.flip()

    # --- Limitation du framerate ---
    clock.tick(FPS)

# --- Fermeture propre de Pygame ---
pygame.quit()
