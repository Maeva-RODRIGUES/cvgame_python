import pygame
from settings import (
    BUBBLE_SOUND,
    BUBBLE_POS,
    BUBBLE_FRAME,
    BUBBLE_PADDING,
    BUBBLE_LINE_HEIGHT,
    BUBBLE_CHAR_DELAY_MS,
    DARK_PURPLE,
    GOLD,
)
from utils import load_image, wrap_text

HINT_TEXT = "Espace pour continuer"


class DialogueBubble:
    """Bulle de dialogue du niveau : titre + texte affiché en machine à écrire."""

    def __init__(self, screen, levels, font_size=14, color=(255, 255, 255)):
        self.screen = screen
        self.levels = levels
        self.font = pygame.font.Font(None, font_size)
        self.hint_font = pygame.font.Font(None, 20)
        self.color = color

        self.image = self._load_image()
        frame = pygame.Rect(BUBBLE_FRAME)
        # Zone où le texte doit tenir : intérieur du cadre moins la marge
        self.text_area = frame.move(BUBBLE_POS).inflate(-2 * BUBBLE_PADDING, -2 * BUBBLE_PADDING)

        self.bubble_sound = pygame.mixer.Sound(BUBBLE_SOUND)

        self.current_level = "level_1"
        self.title = ""
        self.text = []
        self.visible = False

        # Effet machine à écrire
        self.typing_index = 0
        self.finished_typing = False
        self.last_update_time = 0

        self._load_dialogue()

    @staticmethod
    def _load_image():
        """Image recadrée sur sa zone visible, intérieur du cadre rempli pour la lisibilité."""
        image, _ = load_image("objects/bubble.png")
        image = image.convert_alpha()
        visible = image.subsurface(image.get_bounding_rect(min_alpha=16)).copy()
        visible.fill(DARK_PURPLE, pygame.Rect(BUBBLE_FRAME))
        return visible

    def _load_dialogue(self):
        """Charge le titre et le dialogue du niveau courant."""
        data = self.levels.get(self.current_level, {})
        self.title = data.get("title", "")
        self.text = wrap_text(data.get("dialogue", ""), self.font, self.text_area.width)

    def _total_chars(self):
        return sum(len(line) for line in self.text)

    def set_level(self, level_name):
        """Change de niveau et relance l'effet machine à écrire."""
        self.current_level = level_name
        self._load_dialogue()
        self.typing_index = 0
        self.finished_typing = False
        self.last_update_time = pygame.time.get_ticks()

    def toggle(self):
        """Afficher ou masquer la bulle."""
        self.visible = not self.visible
        self.bubble_sound.play()

    def skip_or_hide(self):
        """Affiche tout le texte d'un coup, ou masque la bulle s'il est déjà affiché."""
        if not self.visible:
            return
        if not self.finished_typing:
            self.typing_index = self._total_chars()
            self.finished_typing = True
        else:
            self.visible = False

    def _update_typing(self):
        now = pygame.time.get_ticks()
        if self.finished_typing or now - self.last_update_time < BUBBLE_CHAR_DELAY_MS:
            return
        self.typing_index += 1
        self.last_update_time = now
        if self.typing_index >= self._total_chars():
            self.finished_typing = True

    def draw(self):
        if not self.visible:
            return
        self._update_typing()

        self.screen.blit(self.image, BUBBLE_POS)
        x, y = self.text_area.topleft

        # Titre
        self.screen.blit(self.font.render(self.title, True, GOLD), (x, y))

        # Texte, lettre par lettre
        remaining = self.typing_index
        for i, line in enumerate(self.text):
            if remaining <= 0:
                break
            shown = line[:remaining]
            remaining -= len(line)
            surface = self.font.render(shown, True, self.color)
            self.screen.blit(surface, (x, y + (i + 1.5) * BUBBLE_LINE_HEIGHT))

        # Indication clignotante une fois le texte entièrement affiché
        if self.finished_typing and (pygame.time.get_ticks() // 500) % 2 == 0:
            hint = self.hint_font.render(HINT_TEXT, True, GOLD)
            self.screen.blit(hint, hint.get_rect(bottomright=self.text_area.bottomright))
