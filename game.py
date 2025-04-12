import pygame
from pygame.locals import *
from objects import *
import sys
import os  
import random


GAME_END = None

pygame.init()


# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Start Game")
clock = pygame.time.Clock()

def check_collision(creature, dx, dy):

    creature.move(dx, dy)

    collided_blocks = pygame.sprite.spritecollide(creature, sprite_group, False)

    for block in collided_blocks:

        if (isinstance(block, Mysterious)):
            block.reveal(creature)
        
        elif (isinstance(block, Block) and block != creature):
            creature.move(-1 * dx, -1 * dy) # undo the move if this is a block collision
        elif isinstance(block, Player) and isinstance(creature, Monster):
                block.life_bar.take_damage(1)

        elif isinstance(creature, Player) and isinstance(block, Monster):
                creature.life_bar.take_damage(1)  
                
        elif (isinstance(block, Collectible) and isinstance(creature, Player)): # object is a collectible
            block.collect_item(creature)

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
                

# Game class
class Game:
    def __init__(self, num_tiles = 16):
        self.player = Player(0, 0)
        self.tiles = [[0] * num_tiles] * num_tiles
        print(len(sprite_group)) # 1 player = 1 sprite
        self.map = Map(self.player, self)
        print(len(sprite_group)) # 16 * 16 = 256 sprites
        self.running = True
        
    
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
            
        check_collision(self.player, dx, dy)
    
    def update_monsters(self):
        for monster in monster_group:
            check_collision(monster, monster.rect.x + DEFAULT_SPEED, monster.rect.y + DEFAULT_SPEED)        
        

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