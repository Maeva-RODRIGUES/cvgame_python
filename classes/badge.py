import pygame
from settings import BADGE_SIZE, BADGES_PATH, NEON_PINK, NEON_BLUE, GOLD, WHITE, BLACK
from utils import load_image

class Badge:
    def __init__(self, x, y, badge_type):
        self.rect = pygame.Rect(x, y, BADGE_SIZE[0], BADGE_SIZE[1])
        self.badge_type = badge_type
        self.collected = False
        
        # Animation
        self.float_offset = 0
        self.float_direction = 1
        self.original_y = y
        
        # Sprite
        self.sprite = self.load_sprite()
    
    def load_sprite(self):
        """Charge le sprite du badge"""
        filename = f"badge_{self.badge_type}.png"
        
        try:
            sprite = load_image(BADGES_PATH + filename, BADGE_SIZE)
        except:
            # Fallback : créer un badge coloré
            sprite = self.create_fallback_sprite()
            raise
        
        return sprite
    
    def create_fallback_sprite(self):
        """Crée un sprite de fallback pour le badge"""
        sprite = pygame.Surface(BADGE_SIZE)
        sprite.fill((0, 0, 0, 0))  # Transparent
        
        # Couleurs par type de badge
        colors = {
            "rh": NEON_PINK,
            "reconversion": NEON_BLUE,
            "web": GOLD,
            "abap": (128, 255, 128),  # Vert clair
            "opensource": (255, 128, 0),  # Orange
            "ia": (128, 0, 255),  # Violet
            "objectif": (255, 255, 128)  # Jaune clair
        }
        
        color = colors.get(self.badge_type, WHITE)
        
        # Forme hexagonale
        center = (BADGE_SIZE[0] // 2, BADGE_SIZE[1] // 2)
        radius = min(BADGE_SIZE) // 2 - 2
        
        points = []
        import math
        for i in range(6):
            angle = i * math.pi / 3
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))
        
        pygame.draw.polygon(sprite, color, points)
        pygame.draw.polygon(sprite, WHITE, points, 2)
        
        # Icône au centre (lettre)
        font = pygame.font.Font(None, 20)
        letters = {
            "rh": "RH",
            "reconversion": "R",
            "web": "W",
            "abap": "A",
            "opensource": "OS",
            "ia": "IA",
            "objectif": "O"
        }
        
        letter = letters.get(self.badge_type, "?")
        text_surface = font.render(letter, True, BLACK)
        text_rect = text_surface.get_rect(center=center)
        sprite.blit(text_surface, text_rect)
        
        return sprite
    
    def update(self):
        """Met à jour l'animation du badge"""
        if not self.collected:
            # Animation de flottement
            self.float_offset += 0.1 * self.float_direction
            if abs(self.float_offset) > 5:
                self.float_direction *= -1
            
            self.rect.y = self.original_y + int(self.float_offset)
    
    def collect(self):
        """Marque le badge comme collecté"""
        self.collected = True
    
    def draw(self, screen):
        """Dessine le badge"""
        if not self.collected:
            self.update()
            
            # Effet de brillance
            glow_rect = pygame.Rect(
                self.rect.x - 5, 
                self.rect.y - 5, 
                self.rect.width + 10, 
                self.rect.height + 10
            )
            pygame.draw.rect(screen, (255, 255, 255, 50), glow_rect)
            
            # Badge
            screen.blit(self.sprite, self.rect)
            
            # Particules autour du badge
            import random
            for _ in range(3):
                particle_x = self.rect.centerx + random.randint(-20, 20)
                particle_y = self.rect.centery + random.randint(-20, 20)
                particle_size = random.randint(1, 3)
                pygame.draw.rect(screen, GOLD, (particle_x, particle_y, particle_size, particle_size))