import pygame
import os  
from pygame.locals import *
from objects import *
from start_page import InfoPage
from constants import *
import sys
import random
import time  # Add this import for timing
from rain import RainPatch  # Import the RainPatch class


pygame.init()

text_font = pygame.font.SysFont("Arial", 30)

def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Game")
clock = pygame.time.Clock()

# Create a group for rain patches
rain_group = pygame.sprite.Group()


def check_monster_collision(monster, dx, dy):
    # Move the monster
    monster.move(dx, dy)

    # Check for collisions with the sprite group
    collided_sprites = pygame.sprite.spritecollide(monster, sprite_group, False)


    if any(isinstance(sprite, Block) for sprite in collided_sprites):
        # Undo the movement
        monster.move(-dx, -dy)
        # Choose a new random direction
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        new_direction = random.choice(directions)
        new_dx = new_direction[0] * DEFAULT_SPEED
        new_dy = new_direction[1] * DEFAULT_SPEED
        # Attempt to move in the new direction
        check_collision(monster, new_dx, new_dy)

def check_collision(creature, dx, dy):

    creature.move(dx, dy)
    collided_blocks = pygame.sprite.spritecollide(creature, sprite_group, False)

    for block in collided_blocks:

        if (isinstance(block, Mysterious) and isinstance(creature, Player)):
            block.reveal(creature)
        
        if (isinstance(block, Block) and block != creature):
            creature.move(-1 * dx, -1 * dy) # undo the move if this is a block collision
        elif (isinstance(block, Collectible) and isinstance(creature, Player)): # object is a collectible
            block.collect_item(creature)
    
    # Check if player is in rain
    if isinstance(creature, Player):
        rain_hits = pygame.sprite.spritecollide(creature, rain_group, False)
        # player slows down when in rain, resumes normal speed otherwise 
        if rain_hits:
            creature.life_bar.update(0.1) 
            creature.speed = 2 
        else:
            creature.speed = 3


        if isinstance(block, Player) and isinstance(creature, Monster):
                block.life_bar.update(1)

        if isinstance(creature, Player) and isinstance(block, Monster):
                creature.life_bar.update(1)  



class Map:

    def __init__(self, main_player, game):
        # assuming player starts at (0,0) - can't place block there
        # creating row 1 with 15 tiles
        game.tiles[0] = [[main_player] + [game.assign_tile(x, 0) for x in range(1, 16)]]
     
        # creating the rest (15 rows) with 16 tiles in each row
        game.tiles[1:] = [[game.assign_tile(col, row) for col in range(16)] for row in range(1, 16)]
        
        # Load background image
        try:
            # Scale the background to fit the map size
            self.background = pygame.image.load(f'{BACKGROUND_DIR}background.jpeg').convert()
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
           
        except pygame.error as e:
            print(f"Could not load background image: {e}")
            # Create a fallback background surface
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(GREEN)
        
   

# Game class
class Game:
    def __init__(self, num_tiles = 16):
        self.player = Player(0, 0)

        self.tiles = [[0] * num_tiles] * num_tiles
        self.map = Map(self.player, self)
        self.last_rain_time = time.time()
        self.rain_interval = random.randint(15, 30)  # Random interval between rain events
        self.show_info_page = False
        self.info_page = InfoPage()
        self.GAME_END = False
        background = pygame.image.load(f"{BACKGROUND_DIR}start_background.png").convert()
        self.start_background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.start_time = time.time()
        self.max_duration = 60

    def draw_inventory(self, player):
       # generate boxes for inventory
        num_slots = len(player.inventory_slots)//2
        start_index = (len(self.tiles) // 2) - (num_slots // 2)
        slot_size = TILE_SIZE + 20
        y_pos = SCREEN_HEIGHT - slot_size
        cur_box_x = start_index * TILE_SIZE
        for box in range(num_slots):
                
            tile_surface = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)
            tile_surface.fill((*BLUE, 100))
            tile_pos = (cur_box_x, y_pos)


            slot = player.inventory_slots[box]

            if slot:
                tile_surface = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)

                tile_surface.blit(slot["img"], (0, 0))
                  # Create text surface first
                font = pygame.font.SysFont(None, 32)
                count_text = f"{player.inventory_items[slot['type']]['count']}"
                text_surface = font.render(count_text, True, WHITE)
                
                # Calculate text position relative to tile_surface
                text_x = (slot_size - text_surface.get_width()) - 4
                text_y = (slot_size - text_surface.get_height()) - 4
                
                # Blit text directly onto tile_surface at calculated position
                tile_surface.blit(text_surface, (text_x, text_y))

            
            screen.blit(tile_surface, tile_pos)
            tile_rect = pygame.Rect(tile_pos, (slot_size, slot_size))
            pygame.draw.rect(screen, (0, 0, 0), tile_rect, width=3)
            cur_box_x += slot_size


    
    def assign_tile(self, row, col):
        if row == 0 or col == 0 or col == len(self.tiles) or row == len(self.tiles):
            return BaseTile(col, row)
        # do not block user (always a path to go)
        if (isinstance(self.tiles[row][col-1], Block) and isinstance(self.tiles[row - 1][col + 1], Block)):
            return BaseTile(col, row)
        
        generic_type = random.choice(MYSTERIOUS_CHOICES + [Mysterious])
        if generic_type == Herb:
            return random.choice(HERB_CHOICES)(col, row)

        return generic_type(col, row)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_END = "Quit Game Pressed"
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
        
        # Game Over event: prints message to screen and exits 
        if self.player.life_bar.current_life <= 0:
            screen.fill((255, 255, 255)) 
            draw_text(f"Game over, score: {self.player.score}", text_font, BLACK, SCREEN_WIDTH/3, SCREEN_HEIGHT/2)
            pygame.display.update()
            self.GAME_END = "Oops" 
        elif time.time() - self.start_time > self.max_duration:
            self.GAME_END = "Finished"
                
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

        if dx == 0 and dy == 0:
             self.player.moving = False
             self.player.current_frame = 0
             self.player.update_sprite()
        else:
            check_collision(self.player, dx, dy)
    
    def update_monsters(self):        
        D = [(-1, 0), (0, 1), (0, -1), (1, 0)]
        for monster in monster_group:
            x = random.choice([-1*(DEFAULT_SPEED*2), DEFAULT_SPEED])
            y = random.choice([-1*(DEFAULT_SPEED*2), DEFAULT_SPEED])
            check_monster_collision(monster, x, y) 


    def update_rain(self):
        # Update existing rain patches
        rain_group.update()
        
        # Check if it's time to create new rain
        current_time = time.time()
        if current_time - self.last_rain_time > self.rain_interval:
            self.create_rain_patches()
            self.last_rain_time = current_time
            self.rain_interval = random.randint(15, 30)  # Set next rain interval
    
    
    def create_rain_patches(self):
        # Create 1-2 rain patches at random locations (reduced from 2-4)
        num_patches = random.randint(1, 2)
        attempts = 0
        patches_created = 0
        
        while patches_created < num_patches and attempts < 20:  # Limit attempts to prevent infinite loop
            attempts += 1
            
            # Generate random position
            x = random.randint(0, SCREEN_WIDTH - TILE_SIZE*5)
            y = random.randint(0, SCREEN_HEIGHT - TILE_SIZE*5)
            
            # Create larger patches (5x5 tiles)
            patch_width = TILE_SIZE * (4 + random.randint(1, 3))  # 4-6 tiles wide
            patch_height = TILE_SIZE * (4 + random.randint(1, 3))  # 4-6 tiles high
            
            # Create a temporary rect to check for overlaps
            temp_rect = pygame.Rect(x, y, patch_width, patch_height)
            
            # Check if this position would overlap with existing rain patches
            if not RainPatch.check_overlap(temp_rect, rain_group.sprites()):
                # No overlap, create the rain patch
                rain_patch = RainPatch(x, y, patch_width, patch_height)
                rain_group.add(rain_patch)
                patches_created += 1       


    def render(self):


        if self.show_info_page:
            self.info_page.draw(screen)
        else:
            # Draw the background image first, then inventory, then sprites
            screen.blit(self.map.background, (0, 0))
            self.draw_inventory(self.player)
            sprite_group.draw(screen)
            rain_group.draw(screen)
            self.player.life_bar.draw(screen)

            # Display time bar
            remaining_time = max(0, int(self.max_duration - (time.time() - self.start_time)))
            font = pygame.font.SysFont(None, 36)
            timer_text = font.render(f"Time Left: {remaining_time}", True, BLACK)
            timer_rect = timer_text.get_rect()
            timer_rect.bottomleft = (200, 10) 

        # Optional: white background for timer box
            timer_bg = pygame.Surface((timer_text.get_width() + 10, timer_text.get_height() + 6))
            timer_bg.fill(WHITE)
            screen.blit(timer_bg, (250, 8))
            screen.blit(timer_text, (250, 8))

            pygame.display.flip()
        
        pygame.display.flip()

        
    def run(self):
        self.show_start_screen()
        while not self.GAME_END:
            self.process_events()
            self.update_monsters()
            self.update_rain()  # Update rain patches
            self.render()
            clock.tick(60)  # 60 FPS
        
        screen.blit(self.start_background, (0, 0))
        self.GAME_END += f"\nScore: {self.player.score}"

        draw_text(self.GAME_END, text_font, BLACK, SCREEN_WIDTH/3, SCREEN_HEIGHT/2)

        pygame.display.update()

        time.sleep(5)
    

    def show_start_screen(self):
        

        font = pygame.font.SysFont(None, 36)
        title_font = pygame.font.SysFont(None, 64)

        while True:
            screen.blit(self.start_background, (0, 0))

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