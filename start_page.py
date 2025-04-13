import pygame
from constants import *

class InfoPage:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 32)
        self.scroll_offset = 0

    def draw(self, surface):
        surface.fill((10, 10, 10))
        y = 20 - self.scroll_offset
        for herb_name, herb_info in HERB_DATA.items():
            # Herb image
            image = pygame.image.load(herb_info["image"]).convert_alpha()
            image = pygame.transform.scale(image, (96, 96))
            surface.blit(image, (10, y))
            # Name
            name_surf = self.title_font.render(herb_name, True, LIGHT_GREEN)
            surface.blit(name_surf, (120, y))

            y += 30
            # Description lines
            for line in herb_info["description"]:
                line_surf = self.font.render(line, True, WHITE)
                surface.blit(line_surf, (120, y))
                y += 25
            y += 30  # spacing between herbs

        # Exit instruction
        y_pos = SCREEN_HEIGHT - TILE_SIZE
        x_pos = SCREEN_WIDTH - (5*TILE_SIZE)
        exit_text = self.font.render("Press ESC to return", True, GRAY)
        surface.blit(exit_text, (x_pos, y_pos))

    def scroll(self, dy):
        self.scroll_offset += dy
        self.scroll_offset = max(0, self.scroll_offset)
