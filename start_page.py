import pygame
from constants import HERB_DATA

class InfoPage:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 32)
        self.scroll_offset = 0

        # Load and scale images
        self.herb_entries = []
        for herb in HERB_DATA:
            image = pygame.image.load(herb["image"]).convert_alpha()
            image = pygame.transform.scale(image, (64, 64))
            self.herb_entries.append({
                "name": herb["name"],
                "image": image,
                "description": herb["description"]
            })

    def draw(self, surface):
        surface.fill((10, 10, 10))
        y = 20 - self.scroll_offset

        for entry in self.herb_entries:
            # Herb image
            surface.blit(entry["image"], (40, y))
            # Name
            name_surf = self.title_font.render(entry["name"], True, (180, 255, 180))
            surface.blit(name_surf, (120, y))

            y += 30
            # Description lines
            for line in entry["description"]:
                line_surf = self.font.render(line, True, (200, 200, 200))
                surface.blit(line_surf, (120, y))
                y += 25
            y += 30  # spacing between herbs

        # Exit instruction
        exit_text = self.font.render("Press ESC to return", True, (160, 160, 160))
        surface.blit(exit_text, (20, 560))

    def scroll(self, dy):
        self.scroll_offset += dy
        self.scroll_offset = max(0, self.scroll_offset)
