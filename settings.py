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

# Vitesse de base du joueur
PLAYER_SPEED = 5

# Taux de rafraîchissement (FPS)
FPS = 60

# Marges ou padding éventuels
PADDING = 20

# Offset pour aligner le joueur sur la plateforme
PLAYER_OFFSET_Y = 300

# Types de badges
BADGE_TYPES = [
    "rh",
    "reconversion", 
    "web",
    "abap",
    "opensource",
    "ia",
    "objectif"
]

# Tailles des sprites
PLAYER_SIZE = (64, 64)
BADGE_SIZE = (32, 32)
PLATFORM_HEIGHT = 20

# Chemins des assets
ASSETS_PATH = "assets/"
PLAYER_PATH = ASSETS_PATH + "player/"
BADGES_PATH = ASSETS_PATH + "badges/"
#BACKGROUNDS_PATH = ASSETS_PATH + "backgrounds/"
#UI_PATH = ASSETS_PATH + "ui/"