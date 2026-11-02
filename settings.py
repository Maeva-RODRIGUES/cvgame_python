from pathlib import Path

# Chemins absolus calculés depuis ce fichier : le jeu se lance depuis n'importe quel dossier
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"
LEVELS_PATH = DATA_DIR / "levels.json"
END_SCREEN_PATH = DATA_DIR / "end_screen.json"

# Dimensions fenêtre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Couleurs (RGB)
PURPLE_BG = (43, 14, 63)  ##2B0E3F
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = (245, 235, 255)
DARK_PURPLE = (30, 0, 56)  # #1E0038
NEON_PINK = (255, 31, 143)  # #FF1F8F
NEON_BLUE = (0, 245, 255)  # #00F5FF
GOLD = (255, 217, 61)  # #FFD93D


# Titre du jeu
GAME_TITLE = "Hack Ton Job - CV Game"
GAME_SUBTITLE = "AIDE MAËVA À DÉCROCHER SON CDI"

# Départ de chaque niveau (coordonnées monde)
PLAYER_START_X = 50
SIGN_X = 130
SIGN_HEIGHT = 90

# Sons
BADGE_SOUND = ASSETS_DIR / "sounds" / "badge.wav"  # ramassage d'un badge
BUBBLE_SOUND = ASSETS_DIR / "sounds" / "pop.wav"  # ouverture de la bulle
# Joué une fois à l'arrivée sur l'écran de fin (Pixabay, Content License)
END_SOUND = ASSETS_DIR / "sounds" / "item-collected-1-367087.mp3"

# Physique du joueur (en pixels par frame)
PLAYER_SPEED = 5
PLAYER_JUMP_STRENGTH = 13  # vitesse verticale au moment du saut
GRAVITY = 0.6  # hauteur max d'un saut = v² / (2 × g) ≈ 141 px

# Taux de rafraîchissement (FPS)
FPS = 60

# Marges ou padding éventuels
PADDING = 20

# Sol : la tuile (platform.png recadrée) fait 77 px de haut et touche le bas de l'écran
GROUND_HEIGHT = 77
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT

# Bulle de dialogue (bubble.png recadrée : 452 x 312, queue comprise)
BUBBLE_POS = (30, 70)  # coin haut gauche à l'écran, sous le titre
BUBBLE_FRAME = (6, 6, 440, 228)  # intérieur du cadre, relatif à l'image recadrée
BUBBLE_PADDING = 16
BUBBLE_LINE_HEIGHT = 28
BUBBLE_CHAR_DELAY_MS = 40  # vitesse de la machine à écrire

# Types de badges
BADGE_TYPES = ["rh", "reconversion", "web", "backend", "fullstack", "data", "objectif"]

# Dernier badge : remplacé par le drapeau final
FINAL_BADGE = "objectif"
FLAG_HEIGHT = 96

# Tailles des sprites
PLAYER_SIZE = (64, 110)  # garde le ratio du sprite recadré (523 x 900)
BADGE_SIZE = (32, 32)
PLATFORM_HEIGHT = 20

# Style des plateformes (maquette : bloc coloré, liseré néon sur le dessus)
PLATFORM_COLOR = (88, 40, 190)
PLATFORM_EDGE_COLOR = NEON_BLUE
PLATFORM_EDGE_HEIGHT = 4
PLATFORM_TILE_WIDTH = 40

# Dossier des badges, relatif à assets/ (load_image part de ASSETS_DIR)
BADGES_PATH = "badges/"
