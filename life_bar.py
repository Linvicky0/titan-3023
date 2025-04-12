import pygame
import sys
import os  # You can remove this unless you're loading assets

# Initialize Pygame
pygame.init()

# Define colors
RED = (255, 0, 0)
GRAY = (169, 169, 169)
BLACK = (0, 0, 0)

class LifeBar:
    def __init__(self, max_life, x, y, width, height):
        self.max_life = max_life
        self.current_life = max_life
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, surface):
        """Draw the life bar on the screen."""
        # Draw background (gray)
        pygame.draw.rect(surface, GRAY, (self.x, self.y, self.width, self.height))

        # Draw foreground (red)
        life_percentage = self.current_life / self.max_life
        life_width = self.width * life_percentage
        pygame.draw.rect(surface, RED, (self.x, self.y, life_width, self.height))

        # Optional: border
        pygame.draw.rect(surface, BLACK, (self.x, self.y, self.width, self.height), 2)

    def update(self, amount):
        if (amount < 0):
            self.current_life = max(0, self.current_life - amount)
        else:
            self.current_life = min(self.max_life, self.current_life - amount)

   
    def die(self):
        return self.current_life == 0