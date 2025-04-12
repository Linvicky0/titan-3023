import pygame
from pygame.locals import *
from objects import *
import sys
import os  
import random
import time  # Add this import for timing
from rain import RainPatch  # Import the RainPatch class
from text import draw_text, text_font # to print text to the screen



GAME_END = None

pygame.init()


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

    # Define the types to check for
    collision_types = (Block, Herb, Bacteria)

    # Check if any collided sprite is an instance of the specified types
    if any(isinstance(sprite, collision_types) for sprite in collided_sprites):
        # Undo the movement
        monster.move(-dx, -dy)

        # Choose a new random direction
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        new_direction = random.choice(directions)
        new_dx = new_direction[0] * DEFAULT_SPEED*2
        new_dy = new_direction[1] * DEFAULT_SPEED*2

        # Attempt to move in the new direction
        monster.move(new_dx, new_dy)

def check_collision(creature, dx, dy):

    creature.move(dx, dy)
    collided_blocks = pygame.sprite.spritecollide(creature, sprite_group, False)

    for block in collided_blocks:

        if (isinstance(block, Mysterious)):
            block.reveal(creature)
        
        elif (isinstance(block, Block) and block != creature):
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
            self.background = pygame.image.load(f'{IMG_DIR}background.jpeg').convert()
            # Scale the background to fit the map size
            # map_width = len(self.grid[0]) * TILE_SIZE
            # map_height = len(self.grid) * TILE_SIZE
            # self.background = pygame.transform.scale(self.background, (map_width, map_height))
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
        # print(len(sprite_group)) # 1 player = 1 sprite
        self.map = Map(self.player, self)
        # print(len(sprite_group)) # 16 * 16 = 256 sprites
        self.running = True
        self.last_rain_time = time.time()
        self.rain_interval = random.randint(15, 30)  # Random interval between rain events
        self.start_time = time.time()
        self.max_duration = 60  # sec

    def draw_inventory(self, player):
       # generate boxes for inventory
        num_slots = len(player.inventory_slots)
        start_index = (len(self.tiles) // 2) - (num_slots // 2)
        slot_size = TILE_SIZE + 20
        y_pos = SCREEN_HEIGHT - slot_size
        cur_box_x = start_index * TILE_SIZE
        for box in range(num_slots):
                
            tile_surface = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)
            tile_surface.fill((*BLUE, 50))
            tile_pos = (cur_box_x, y_pos)


            slot = player.inventory_slots[box]

            if slot:
                tile_surface = pygame.Surface((slot_size, slot_size), pygame.SRCALPHA)

                tile_surface.blit(slot["img"], (0, 0))
                font = pygame.font.SysFont(None, 24)
                count_text = f"{player.inventory_items[slot['type']]['count']}"
                text_surface = font.render(count_text, True, BLACK)  
                text_rect = text_surface.get_rect(center=(cur_box_x + slot_size // 2, y_pos + slot_size // 2))

                tile_surface.blit(text_surface, text_rect)
            
            screen.blit(tile_surface, tile_pos)
            tile_rect = pygame.Rect(tile_pos, (slot_size, slot_size))
            pygame.draw.rect(screen, (0, 0, 0), tile_rect, width=3)
            cur_box_x += slot_size
            

    def draw(self, screen):
        # Draw the background image first, then inventory, then sprites
        screen.blit(self.map.background, (0, 0))
        self.draw_inventory(self.player)
        sprite_group.draw(screen)
        rain_group.draw(screen)

    
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

    # Timer check
        if time.time() - self.start_time > self.max_duration:
         global GAME_END
         GAME_END = "timeout"
         self.running = False

    # Game over due to health loss
        if self.player.life_bar.current_life <= 0:
         screen.fill((255, 255, 255)) 
         draw_text("Game over", text_font, (0, 0, 0), 220, 150)
         pygame.display.update()
         time.sleep(5)
         self.running = False 
        
                
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
            x = random.choice([-1*(DEFAULT_SPEED*2), DEFAULT_SPEED*4])
            y = random.choice([-1*(DEFAULT_SPEED*2), DEFAULT_SPEED*4])
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
            x = random.randint(0, SCREEN_WIDTH - TILE_SIZE*3)
            y = random.randint(0, SCREEN_HEIGHT - TILE_SIZE*3)
            
            # Larger patches (3x3 tiles instead of 2x2)
            patch_width = TILE_SIZE * 3
            patch_height = TILE_SIZE * 3
            
            # Create a temporary rect to check for overlaps
            temp_rect = pygame.Rect(x, y, patch_width, patch_height)
            
            # Check if this position would overlap with existing rain patches
            if not RainPatch.check_overlap(temp_rect, rain_group.sprites()):
                # No overlap, create the rain patch
                rain_patch = RainPatch(x, y, patch_width, patch_height)
                rain_group.add(rain_patch)
                patches_created += 1       


    def render(self):
        if not GAME_END:
            self.draw(screen)
            self.player.life_bar.draw(screen)

        # Show remaining time
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

        else:
            screen.fill(BLACK)
            font = pygame.font.SysFont(None, 55)
        text = ''
        # ✅ Always define `text` first
        if GAME_END == "finished":
             text = "Timer Up!"

            #text = "Congrats on finishing!"
        
        score = 0
        for item_class, info in self.player.inventory_items.items():
            if hasattr(item_class, 'reward'):  # Ensure item class has a reward attribute
                count = info.get("count", 0)  # Access the count correctly
                score += count * item_class.reward  # C

        # Draw result text
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (250, 200))

        # Draw score
     #
        pygame.display.flip()

        
    def run(self):
        while self.running:
            self.process_events()
            self.update_monsters()
            self.update_rain()  # Update rain patches
            self.render()
            clock.tick(60)  # 60 FPS

    

# Main function
def main():
    game = Game()
    game.run()
    pygame.quit()
    pygame.time.Clock().tick(60)
    sys.exit()

if __name__ == "__main__":
    main()