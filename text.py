# use to print text to the screen 

import pygame 

pygame.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# default font -- create your own using this format ("Font_Name", size)
text_font = pygame.font.SysFont("Arial", 60)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))
