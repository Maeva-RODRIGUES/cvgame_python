import pygame
import json
from settings import BUBBLE_OFFSET_Y

class DialogueBubble:
    def __init__(self, screen, json_path, font_size=14, color=(255, 255, 255)):
        self.screen = screen
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        
        # Charger le JSON des dialogues
        with open(json_path, "r", encoding="utf-8") as f:
            self.dialogues = json.load(f)
            
         # Charger l'image de la bulle avec transparence
        self.bubble_image = pygame.image.load("assets/objects/bubble.png").convert_alpha() 
        self.bubble_width, self.bubble_height = self.bubble_image.get_size()  
        
        self.current_level = "level_1"
        self.text = []
        self.title = ""
      
        self.current_index = 0
        self.text_lines = []
        self.title = ""
        self.active = False
        self._load_dialogue()

    def _load_dialogue(self):
        """Charge le dialogue et le titre du niveau courant"""
        data = self.dialogues.get(self.current_level, {})
        self.title = data.get("title", "")
        dialogue_text = data.get("dialogue", "")
        self.text = self._split_text(dialogue_text)

    def _split_text(self, text, max_width=55):
        """Découpe le texte pour qu'il tienne dans la bulle"""
        words = text.split(" ")
        lines, current = [], ""
        for word in words:
            if len(current + word) < max_width:
                current += word + " "
            else:
                lines.append(current)
                current = word + " "
        lines.append(current)
        return lines

    def set_level(self, level_name):
        """Changer de niveau"""
        self.current_level = level_name
        self._load_dialogue()
        self.active = True
      
    def show(self):
        """Affiche la bulle"""
        self.visible = True
        self.alpha = 0
    
    def hide(self):
        """Masquer la bulle"""
        self.visible = False

    def draw(self):
        """Affiche la bulle de dialogue"""
        if not self.active:
            return  
        
        bubble_width = 100
        bubble_height = 100
        
        bubble_x = 10      
        bubble_y = 80

        # Dessiner l'image de bulle à la nouvelle position
        self.screen.blit(self.bubble_image, (bubble_x, bubble_y))  
        
        bubble_rect = pygame.Rect(35, BUBBLE_OFFSET_Y, bubble_width // 2, bubble_height - 20)
       

        # Fond semi-transparent
        surface = pygame.Surface((bubble_width, bubble_height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        self.screen.blit(surface, bubble_rect)

        # Titre du dialogue
        title_surface = self.font.render(self.title, True, (255, 223, 0))
        self.screen.blit(title_surface, (bubble_rect.x + 15, bubble_rect.y + 10))

        # Texte du dialogue
        for i, line in enumerate(self.text):
            dialogue_surface = self.font.render(line, True, self.color)
            self.screen.blit(dialogue_surface, (bubble_rect.x + 15, bubble_rect.y + 50 + i * 30))
