import os
from enum import Enum, auto

import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PURPLE_BG,
    FPS,
    GAME_TITLE,
    TEXT_COLOR,
    GOLD,
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

LEVELS_PATH = "data/levels.json"


class State(Enum):
    TITLE = auto()    # écran titre
    PLAYING = auto()  # partie en cours
    END = auto()      # partie terminée


class Game:
    """Le jeu : fenêtre, objets, et une boucle événements -> logique -> affichage par état."""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        self.title_text = self.title_font.render("AIDE MAËVA À MONTER EN COMPÉTENCES", True, TEXT_COLOR)
        self.badge_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, BADGE_SOUND))

        self.ground = Ground(GROUND_Y)
        self.sign = Sign(SIGN_X, GROUND_Y)
        self.player = Player(x=PLAYER_START_X, y=0)

        self.state = State.TITLE
        self.running = True
        self.new_game()

    # ----- Mise en place -----

    def new_game(self):
        """Prépare une partie depuis le niveau 1 (aussi utilisé pour rejouer)."""
        self.levels = LevelManager(LEVELS_PATH)
        self.bubble = DialogueBubble(self.screen, self.levels.levels, font_size=24, color=TEXT_COLOR)
        self.bubble.set_level(self.levels.current_level)
        self.player.place(PLAYER_START_X, GROUND_Y)
        self.camera_x = 0
        # Vrai entre le ramassage du badge et la fermeture de la bulle
        self.level_complete = False

    def start_next_level(self):
        """Niveau suivant : joueur au départ, caméra à 0, nouveau dialogue. Sinon fin de partie."""
        if self.levels.next_level():
            self.player.place(PLAYER_START_X, GROUND_Y)
            self.bubble.set_level(self.levels.current_level)
            self.camera_x = 0
        else:
            self.state = State.END

    # ----- Boucle principale -----

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

    # ----- 1. Événements -----

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return
        if self.state == State.TITLE:
            self._handle_title_event(event)
        elif self.state == State.PLAYING:
            self._handle_playing_event(event)

    def _handle_title_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.new_game()
            self.state = State.PLAYING

    def _handle_playing_event(self, event):
        # Espace : afficher la bulle, accélérer le texte ou la fermer
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not self.bubble.visible:
                self.bubble.toggle()
            else:
                self.bubble.skip_or_hide()
                # Bulle du badge fermée : on enchaîne sur le niveau suivant
                if self.level_complete and not self.bubble.visible:
                    self.level_complete = False
                    self.start_next_level()

    # ----- 2. Logique (coordonnées monde) -----

    def update(self):
        if self.state == State.PLAYING:
            self._update_playing()

    def _update_playing(self):
        keys = pygame.key.get_pressed()
        # Le joueur est figé pendant que la bulle du badge est ouverte
        if not self.level_complete:
            self.player.update(keys, GROUND_Y, self.levels.platforms, self.levels.width)

        # La caméra centre le joueur, bornée entre le début et la fin du niveau
        camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_x = max(0, min(camera_x, self.levels.width - SCREEN_WIDTH))

        # Badges : animation, puis ramassage (une seule fois grâce à `collected`)
        for badge in self.levels.badges:
            badge.update()
        for badge in self.levels.badges:
            if not badge.collected and self.player.rect.colliderect(badge.rect):
                badge.collect()
                self.badge_sound.play()
                # Bulle du niveau terminé ; le passage au suivant se fait à sa fermeture
                self.level_complete = True
                self.bubble.set_level(self.levels.current_level)  # relance la machine à écrire
                if not self.bubble.visible:
                    self.bubble.toggle()

    # ----- 3. Affichage (coordonnées écran = monde - camera_x) -----

    def draw(self):
        self.screen.fill(PURPLE_BG)
        if self.state == State.TITLE:
            self._draw_title()
        elif self.state == State.PLAYING:
            self._draw_playing()
        else:
            self._draw_end()

    def _draw_centered(self, surface, y):
        self.screen.blit(surface, surface.get_rect(center=(SCREEN_WIDTH // 2, y)))

    def _draw_title(self):
        # Version minimale : l'écran titre complet arrive en 2.2
        self._draw_centered(self.title_text, SCREEN_HEIGHT // 2 - 40)
        start = self.text_font.render("Appuie sur Espace pour commencer", True, GOLD)
        self._draw_centered(start, SCREEN_HEIGHT // 2 + 30)

    def _draw_playing(self):
        # Décor avant le joueur : sol infini, panneau, plateformes, badge
        cam = self.camera_x
        self.ground.draw(self.screen, cam)
        self.sign.draw(self.screen, cam)
        for platform in self.levels.platforms:
            platform.draw(self.screen, cam)
        for badge in self.levels.badges:
            badge.draw(self.screen, cam)

        self.player.draw(self.screen, cam)
        self.bubble.draw()
        self._draw_centered(self.title_text, 40)

    def _draw_end(self):
        # Version minimale : l'écran de fin complet arrive en 2.4
        self._draw_centered(self.text_font.render("Fin de la partie", True, GOLD), SCREEN_HEIGHT // 2)
