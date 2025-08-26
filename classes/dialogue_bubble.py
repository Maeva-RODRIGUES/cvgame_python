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
        
        # Son pour l'apparition de la bulle <= ajout 20h05
        self.bubble_sound = pygame.mixer.Sound("assets/sounds/pop.wav")  

        self.current_level = "level_1"
        self.text = []
        self.title = ""
        self.visible = False
        self.current_index = 0
        self.text_lines = []
        self.active = False
        self.scale = 0
        
        # variables effet machine à écrire
        self.typing_index = 0
        self.typing_speed = 2          # Plus le chiffre est grand → plus c’est lent
        self.last_update_time = 0
        self.finished_typing = False

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
        
        
    def toggle(self):  
        """Afficher ou masquer la bulle"""
        self.visible = not self.visible
        self.bubble_sound.play() 
        
    def skip_or_hide(self): 
        """Affiche le texte instantanément ou masque la bulle"""
        if not self.visible:
            return
        if not self.finished_typing:
            # Afficher tout le texte
            self.typing_index = sum(len(line) for line in self.text)
            self.finished_typing = True
        else:
            # Masquer la bulle si tout est affiché
            self.visible = False
      
    def draw(self):
        """Affiche la bulle de dialogue"""
        if not self.visible:
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
        
        # logique effet machine à écrire
        now = pygame.time.get_ticks()
        if not self.finished_typing and now - self.last_update_time > 30 * self.typing_speed:
            self.typing_index += 1
            self.last_update_time = now
            total_length = sum(len(line) for line in self.text)
            if self.typing_index >= total_length:
                self.finished_typing = True


        # Texte du dialogue : affichage progressif lettre par lettre
        char_count = 0
        for i, line in enumerate(self.text):
            visible_text = ""
            for char in line:
                if char_count < self.typing_index:
                    visible_text += char
                    char_count += 1
                else:
                    break
            dialogue_surface = self.font.render(visible_text, True, self.color)
            self.screen.blit(dialogue_surface, (bubble_rect.x + 15, bubble_rect.y + 50 + i * 30))
