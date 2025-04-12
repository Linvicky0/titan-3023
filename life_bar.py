import pygame
import sys
import os  # You can remove this unless you're loading assets
from constants import *

# Initialize Pygame
pygame.init()



class LifeBar:
    def __init__(self, max_life, x, y, width, height):
        self.max_life = max_life
        self.current_life = max_life
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 24)


    def draw(self, surface):
        """Draw the life bar on the screen."""
        # Draw background (gray)
        pygame.draw.rect(surface, GRAY, (self.x, self.y, self.width, self.height))

        # Draw foreground (red)
        life_percentage = self.current_life / self.max_life
        life_width = self.width * life_percentage
        pygame.draw.rect(surface, GREEN, (self.x, self.y, life_width, self.height))

        # Optional: border
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)
        life_text = f"{self.current_life}%"
        text_surface = self.font.render(life_text, True, BLACK)  # Render text
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect) 

    def update(self, amount):
        if (amount < 0):
            self.current_life = max(0, self.current_life - amount)
        else:
            self.current_life = min(self.max_life, self.current_life - amount)

   
    def die(self):
        return self.current_life == 0