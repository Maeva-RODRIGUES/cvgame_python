# Dimensions fenêtre
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Couleurs (RGB)
PURPLE_BG = (43, 14, 63)  ##2B0E3F
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = (245, 235, 255)
DARK_PURPLE = (30, 0, 56)      # #1E0038
NEON_PINK = (255, 31, 143)     # #FF1F8F
NEON_BLUE = (0, 245, 255)      # #00F5FF
GOLD = (255, 217, 61)          # #FFD93D


# Titre du jeu
GAME_TITLE = "Hack Ton Job - CV Game"

# Départ de chaque niveau (coordonnées monde)
PLAYER_START_X = 50
SIGN_X = 130
SIGN_HEIGHT = 90

# Son joué au ramassage d'un badge (relatif à assets/)
BADGE_SOUND = "sounds/badge.wav"

# Physique du joueur (en pixels par frame)
PLAYER_SPEED = 5
PLAYER_JUMP_STRENGTH = 13   # vitesse verticale au moment du saut
GRAVITY = 0.6               # hauteur max d'un saut = v² / (2 × g) ≈ 141 px

# Taux de rafraîchissement (FPS)
FPS = 60

# Marges ou padding éventuels
PADDING = 20

# Sol : la tuile (platform.png recadrée) fait 77 px de haut et touche le bas de l'écran
GROUND_HEIGHT = 77
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT

BUBBLE_OFFSET_Y = 220

# Types de badges
BADGE_TYPES = [
    "rh",
    "reconversion",
    "web",
    "abap",
    "fullstack",
    "data",
    "objectif"
]

# Tailles des sprites
PLAYER_SIZE = (64, 110)  # garde le ratio du sprite recadré (523 x 900)
BADGE_SIZE = (32, 32)
PLATFORM_HEIGHT = 20

# Style des plateformes (maquette : bloc coloré, liseré néon sur le dessus)
PLATFORM_COLOR = (88, 40, 190)
PLATFORM_EDGE_COLOR = NEON_BLUE
PLATFORM_EDGE_HEIGHT = 4
PLATFORM_TILE_WIDTH = 40

# Chemins des assets
ASSETS_PATH = "assets/"
PLAYER_PATH = ASSETS_PATH + "player/"
BADGES_PATH = "badges/"  # relatif à assets/ (load_image ajoute déjà assets/)
#BACKGROUNDS_PATH = ASSETS_PATH + "backgrounds/"
#UI_PATH = ASSETS_PATH + "ui/"