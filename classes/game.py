import os
from enum import Enum, auto

import pygame
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    PURPLE_BG,
    FPS,
    GAME_TITLE,
    GAME_SUBTITLE,
    TEXT_COLOR,
    GOLD,
    WHITE,
    DARK_PURPLE,
    NEON_BLUE,
    NEON_PINK,
    GROUND_Y,
    PLAYER_START_X,
    SIGN_X,
    BADGE_SOUND,
    END_SOUND,
)
from classes.ground import Ground
from classes.sign import Sign
from classes.player import Player
from classes.dialogue_bubble import DialogueBubble
from classes.level import LevelManager
from classes.hud import Hud
from classes.end_screen import EndScreen
from utils import DATA_DIR

LEVELS_PATH = "data/levels.json"
END_SCREEN_PATH = "data/end_screen.json"


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

        self.big_font = pygame.font.Font(None, 96)
        self.title_font = pygame.font.Font(None, 48)
        self.text_font = pygame.font.Font(None, 32)
        self.title_text = self.title_font.render(GAME_SUBTITLE, True, TEXT_COLOR)
        self.badge_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, BADGE_SOUND))
        self.end_sound = pygame.mixer.Sound(os.path.join(DATA_DIR, END_SOUND))

        self.ground = Ground(GROUND_Y)
        self.sign = Sign(SIGN_X, GROUND_Y)
        self.player = Player(x=PLAYER_START_X, y=0)
        self.hud = Hud()
        self.end_screen = EndScreen(END_SCREEN_PATH, self.hud.sprites)

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
        self.collected = []  # types des badges ramassés, dans l'ordre
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
            self.end_sound.play()

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
        else:
            self._handle_end_event(event)

    def _handle_title_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.new_game()
            self.state = State.PLAYING

    def _handle_end_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_SPACE:  # rejouer
            self.end_sound.stop()  # coupe le son de fin s'il joue encore
            self.new_game()
            self.state = State.PLAYING
        elif event.key == pygame.K_ESCAPE:  # quitter
            self.running = False

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
                self.collected.append(badge.badge_type)
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
        # Décor : le sol, le panneau et Maëva au départ
        self.ground.draw(self.screen, 0)
        self.sign.draw(self.screen, 0)
        self.player.draw(self.screen, 0)

        # Titre, puis sous-titre dans un cadre néon (comme la maquette)
        self._draw_centered(self.big_font.render(GAME_TITLE, True, WHITE), 120)
        box = pygame.Rect(0, 0, self.title_text.get_width() + 60, 64)
        box.center = (SCREEN_WIDTH // 2, 215)
        pygame.draw.rect(self.screen, DARK_PURPLE, box)
        pygame.draw.rect(self.screen, NEON_PINK, box, 3)
        self._draw_centered(self.title_text, box.centery)

        # Contrôles : une ligne par action, touches dessinées à gauche
        controls = [
            (["left", "right"], "Se déplacer"),
            (["up"], "Sauter"),
            (["Espace"], "Ouvrir, accélérer ou fermer la bulle"),
        ]
        y = 310
        for keys, action in controls:
            x = SCREEN_WIDTH // 2 - 220
            for key in keys:
                x = self._draw_key(key, x, y) + 10
            label = self.text_font.render(action, True, TEXT_COLOR)
            self.screen.blit(label, label.get_rect(midleft=(SCREEN_WIDTH // 2 - 60, y + 22)))
            y += 64

        # Invitation à jouer, qui clignote
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            start = self.text_font.render("Appuie sur Espace pour commencer", True, GOLD)
            self._draw_centered(start, 530)

    def _draw_key(self, key, x, y):
        """Dessine une touche de clavier en (x, y) et renvoie son bord droit.

        La police par défaut n'a pas les caractères flèches : on les trace en triangles.
        """
        label = None if key in ("left", "right", "up") else self.text_font.render(key, True, WHITE)
        width = 44 if label is None else label.get_width() + 30
        rect = pygame.Rect(x, y, width, 44)
        pygame.draw.rect(self.screen, DARK_PURPLE, rect, border_radius=6)
        pygame.draw.rect(self.screen, NEON_BLUE, rect, 2, border_radius=6)
        cx, cy = rect.center
        arrows = {
            "left": [(cx - 9, cy), (cx + 7, cy - 9), (cx + 7, cy + 9)],
            "right": [(cx + 9, cy), (cx - 7, cy - 9), (cx - 7, cy + 9)],
            "up": [(cx, cy - 9), (cx - 9, cy + 7), (cx + 9, cy + 7)],
        }
        if label is None:
            pygame.draw.polygon(self.screen, WHITE, arrows[key])
        else:
            self.screen.blit(label, label.get_rect(center=rect.center))
        return rect.right

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
        self.hud.draw(self.screen, self.levels.number, self.levels.count,
                      self.levels.title, self.collected)

    def _draw_end(self):
        self.end_screen.draw(self.screen, self.collected)
