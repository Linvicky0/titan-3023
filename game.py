import pygame
from pygame.locals import *
from objects import *
import sys, os, random
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

def check_collision(creature, dx, dy):

    creature.move(dx, dy)
    collided_blocks = pygame.sprite.spritecollide(creature, sprite_group, False)

    for block in collided_blocks:

        if (isinstance(block, Mysterious)):
            block.reveal(creature)
        
        elif (isinstance(block, Block) and block != creature):
            creature.move(-1 * dx, -1 * dy) # undo the move if this is a block collision
        elif isinstance(block, Player) and isinstance(creature, Monster):
                block.life_bar.update(1)

        elif isinstance(creature, Player) and isinstance(block, Monster):
                creature.life_bar.update(1)  

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
        
   
        
    def draw(self, surface):
        # Draw the background image first
        surface.blit(self.background, (0, 0))
        # print(len(sprite_group))
        sprite_group.draw(screen)
        # Draw rain patches
        rain_group.draw(screen)
                

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
        
        # Game Over event: prints message to screen and exits 
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
        
        # If not moving, reset animation
        if dx == 0 and dy == 0:
            self.player.moving = False
            self.player.current_frame = 0
            self.player.update_sprite()
        
        check_collision(self.player, dx, dy)
    
    def update_monsters(self):
        for monster in monster_group:
            check_collision(monster, monster.rect.x + DEFAULT_SPEED, monster.rect.y + DEFAULT_SPEED)        

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
        if (not GAME_END):
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
    sys.exit()

if __name__ == "__main__":
    main()