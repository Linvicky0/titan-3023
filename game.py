import pygame
import os  
from pygame.locals import *
from objects import *
from start_page import InfoPage
from constants import HERB_DATA
import sys
import random


GAME_END = None

pygame.init()


# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Game")
clock = pygame.time.Clock()
    

class Map:

    

    def __init__(self, main_player, game):
        # assuming player starts at (0,0) - can't place block there
        # creating row 1 with 15 tiles
        game.tiles[0] = [[main_player] + [game.assign_tile(x, 0) for x in range(1, 16)]]
     
        # creating the rest (15 rows) with 16 tiles in each row
        game.tiles[1:] = [[game.assign_tile(col, row) for col in range(16)] for row in range(1, 16)]
        
        # Load background image
        try:
            self.background = pygame.image.load(f'{IMG_DIR}background/background.jpeg').convert()
            # Scale the background to fit the map size
            #self.grid = game.tiles
            #map_width = len(self.grid[0]) * TILE_SIZE
            #map_height = len(self.grid) * TILE_SIZE
            #self.background = pygame.transform.scale(self.background, (map_width, map_height)).convert()
            #self.background = pygame.transform.scale(self.background, (map_width, map_height))
        except pygame.error as e:
            print(f"Could not load background image: {e}")
            # Create a fallback background surface
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(GREEN)
        
   

    def draw(self, surface):
        # Draw the background image first
        surface.blit(self.background, (0, 0))
        # print(len(sprite_group))
        sprite_group.draw(screen)
        

    def draw_popup(self, surface, title, description_lines, font):
        popup_rect = pygame.Rect(80, 400, 640, 160)
        pygame.draw.rect(surface, (255, 255, 255), popup_rect)
        pygame.draw.rect(surface, (0, 0, 0), popup_rect, 3)

        title_surf = font.render(title, True, (0, 100, 0))
        text_rect = title_surf.get_rect(center=(80 + 640 // 2, 400 + 160 // 2))
        surface.blit(title_surf, (popup_rect.x + 20, popup_rect.y + 10))

        for i, line in enumerate(description_lines):
            line_surf = font.render(line, True, (50, 50, 50))
            surface.blit(line_surf, (popup_rect.x + 20, popup_rect.y + 50 + i * 25))

    def check_collision(self, player, dx, dy):

        player.move(dx, dy)
        collided_blocks = pygame.sprite.spritecollide(player, sprite_group, False)

        for block in collided_blocks:

            if (isinstance(block, Mysterious)):
                block.reveal(player)

            elif (isinstance(block, Block) and block != player):
                # print("Undoing a move", type(block), self.tiles[0][0], block.rect)
                player.move(-1 * dx, -1 * dy) # undo the move if this is a block collision

            elif (isinstance(block, Collectible)): # object is a collectible
                block.collect_item(player)
                

# Game class
class Game:
    def __init__(self, num_tiles = 16):
        self.player = Player(0, 0)
        self.tiles = [[0] * num_tiles] * num_tiles
        print(len(sprite_group)) # 1 player = 1 sprite
        self.map = Map(self.player, self)
        print(len(sprite_group)) # 16*16 = 256 sprites
        self.running = True
        self.monsters = pygame.sprite.Group()
        self.monsters.add(Monster(5, 5))  # Place monster at (5,5)
        sprite_group.add(*self.monsters) 
        self.show_info_page = False
        self.info_page = InfoPage()
    
    def assign_tile(self, row, col):
        if row == 0 or col == 0 or col == len(self.tiles) or row == len(self.tiles):
            return BaseTile(col, row)
        # do not block user (always a path to go)
        if (isinstance(self.tiles[row][col-1], Block) and isinstance(self.tiles[row - 1][col + 1], Block)):
            return BaseTile(col, row)
        
        return random.choice(ITEMS)(col, row)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    self.show_info_page = not self.show_info_page
                elif event.key == pygame.K_ESCAPE and self.show_info_page:
                    self.show_info_page = False
                elif self.show_info_page:
                    if event.key == pygame.K_UP:
                        self.info_page.scroll(-30)
                    elif event.key == pygame.K_DOWN:
                        self.info_page.scroll(30)
                
        # Handle player movement with keys
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.player.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.player.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.player.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.player.speed
            
        self.map.check_collision(self.player, dx, dy)
    
    def update(self):
        for monster in self.monsters:
            monster.update(self.tiles)
        if pygame.sprite.spritecollideany(self.player, self.monsters):
            self.player.life_bar.take_damage(1)
        pass
        
    def render(self):
        if self.show_info_page:
            self.info_page.draw(screen)
            pygame.display.flip()
            return
        if (not GAME_END):
            # screen.fill(BLACK)
            if self.player.popup_text:
                now = pygame.time.get_ticks()
                if now - self.player.popup_timer < self.player.popup_duration:
                    font = pygame.font.SysFont(None, 24)
                    self.map.draw_popup(screen, *self.player.popup_text, font)
                else:
                    self.player.popup_text = None
            self.map.draw(screen)
            self.player.life_bar.draw(screen)
            pygame.display.flip()

        else:
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 55)
            text = "Timer Up!\n\n"
            if (GAME_END == "finished"):
                text = "Congrats on finishing!\n\n"
            
            score = 0
            for item_class, info in self.player.inventory_slots().items():
                score += info["count"] * item_class.reward
            
            text += f"Score: {score}"
            display_text = font.render(text, True, (255, 255, 255))
            screen.blit(display_text, (250, 250))
            pygame.display.flip()

        
    def run(self):
        self.show_start_screen()
        while self.running:
            self.process_events()
            self.update()
            self.render()
            clock.tick(60)  # 60 FPS
    

    def show_start_screen(self):
        background = pygame.image.load(os.path.join(IMG_DIR, "background", "start_background2.png")).convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        font = pygame.font.SysFont(None, 36)
        title_font = pygame.font.SysFont(None, 64)

        while True:
            screen.blit(background, (0, 0))

            # Game title
            title_text = title_font.render("🌌 Titan Exploration 🌌", True, (255, 255, 255))
            screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))

            # Instructions
            start_text = font.render("Press SPACE to start", True, (255, 255, 255))
            info_text = font.render("Press I for Information • Press Q to Quit", True, (200, 200, 200))

            screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT - 120))
            screen.blit(info_text, (SCREEN_WIDTH//2 - info_text.get_width()//2, SCREEN_HEIGHT - 80))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return  # exit start screen and begin game
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_i:
                        self.show_info_page = True
                        return  # open game, info page will trigger right away

    

# Main function
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()