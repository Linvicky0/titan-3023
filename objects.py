import pygame
from constants import *
import sys
from game import GAME_END
import random
from life_bar import LifeBar
from sprites import SpriteSheet
import os


# END GAME WHEN TIMER UP OR INVENTORY FULL

# All objects are one of these 3 categories: blank tile, collectible, or a block (can't move through it)

sprite_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()


class BaseTile(pygame.sprite.Sprite):


    def __init__(self, x, y, img = None):
        super().__init__()
        if not isinstance(self, Player):
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        else:
            size_ratio = 1/2
            player_width = TILE_SIZE * size_ratio
            player_height = TILE_SIZE * size_ratio
            self.image = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
            #Center the player within the tile
            tile_center_x = x * TILE_SIZE + TILE_SIZE / 2
            tile_center_y = y * TILE_SIZE + TILE_SIZE / 2
            self.rect = self.image.get_rect(center=(tile_center_x, tile_center_y))
          
        sprite_group.add(self) 
    
    def move(self, dx, dy):
        # Move the player while checking for collisions with map boundaries
        if 0 <= self.rect.x + dx <= SCREEN_WIDTH - self.rect.width:
            self.rect.x += dx
           
        if 0 <= self.rect.y + dy <= SCREEN_HEIGHT - self.rect.height:
            self.rect.y += dy
    

class Block(BaseTile):
    
    def __init__(self, x, y, img = None, color = BROWN):
        super().__init__(x, y)
        if not img:
            self.image.fill(color)
        else:

            self.image = pygame.transform.scale(img, (TILE_SIZE-7, TILE_SIZE-7))
            self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))


class Collectible(BaseTile):

    def __init__(self, x, y, img):
        super().__init__(x, y)
        assert(img) # collectibles should have an image
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self.award = 0
    
    def collect_item(self, player):
        object_type = type(self)
        if (object_type in player.inventory_items):
                player.inventory_items[object_type]["count"] += 1

        else:
            slot_indices = [i for i in range(len(player.inventory_slots))]
            free_slots = list(filter(lambda i: player.inventory_slots[i] == 0, slot_indices))
            player.inventory_items[object_type] = {"count": 1, "slot": free_slots[0]}
            player.inventory_slots[free_slots[0]] = {"img": self.image, "type": object_type}
            # check if inventory is full
            if len(free_slots) == 1: # this slot is now used
                GAME_END = "finished"
        
        sprite_group.remove(self)
       

class Monster(Block):
    
    def __init__(self, x, y):

        super().__init__(x, y, pygame.image.load(f"{IMG_DIR}monster.png"))
        self.speed = DEFAULT_SPEED
        self.health = 100
        monster_group.add(self)


   

class Herb(Collectible):

    def __init__(self, x, y):
        image = pygame.image.load(os.path.join(IMG_DIR, "herb.png")).convert_alpha()
        super().__init__(x, y,image)
        self.name = "herb"
        self.description_lines = [
            "Habitat: Grows along methane lake edges, thrives in darkness",
            "Appearance: Bioluminescent tendrils with soft cyan glow",
            "Effect: Restores visibility during Titan's long night",
            "Use: Craft light patches to reveal map areas or attract creatures"
        ]



class Glowvine(Collectible):
    def __init__(self, x, y):
        image = pygame.image.load(os.path.join(IMG_DIR, "herb", "Glowvine.png")).convert_alpha()
        super().__init__(x, y,image)
        self.name = "Glowvine"
        self.description_lines = [
            "Habitat: Grows along methane lake edges, thrives in darkness",
            "Appearance: Bioluminescent tendrils with soft cyan glow",
            "Effect: Restores visibility during Titan's long night",
            "Use: Craft light patches to reveal map areas or attract creatures"
        ]

   


class Bacteria(Collectible):

    def __init__(self, x, y):

        # print("Bacteria created")
        image = pygame.image.load(os.path.join(IMG_DIR, "bacteria.png")).convert_alpha()
        super().__init__(x, y,image)
        self.name = "bactria"
        self.description_lines = [
            "Habitat: Grows along methane lake edges, thrives in darkness",
            "Appearance: Bioluminescent tendrils with soft cyan glow",
            "Effect: Restores visibility during Titan's long night",
            "Use: Craft light patches to reveal map areas or attract creatures"
        ]
        self.reward = 10

   
        

class Mysterious(Block):

    def reveal(self, player):
        # Create a creature object on the fly after user touched this block
        object_type = random.choice(ITEMS[0:-1] + [Monster]) # excluding Mysterious
        new_obj = object_type(self.rect.x/TILE_SIZE, self.rect.y/TILE_SIZE)
        # replace old sprite with new one
        sprite_group.add(new_obj)
        sprite_group.remove(self)

        if (isinstance(object_type, Monster)):
            player.life_bar.update(5)

        elif (isinstance(object_type, Collectible)): # put it to backpack
            new_obj.collect_item(player)

                    

class Player(Block):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = DEFAULT_SPEED
        self.life_bar = LifeBar(max_life=100, x=10, y=10, width=200, height=20)
        self.inventory_items = {} # map object type to their slot and count
        self.inventory_slots = [0] * int(len(ITEMS)/2) # 0 means slot is unused        
        self.load_sprites()
         # Animation variables
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 100  # milliseconds per frame
        self.direction = 'down'  # default direction
        self.moving = False

        self.popup_text = None
        self.popup_timer = 0
        self.popup_duration = 5000  # milliseconds = 3 seconds

        
        # Update the image with the first sprite
        self.update_sprite()
    

    def load_sprites(self):
         # Path to the sprite sheet
         sprite_path = os.path.join(IMG_DIR, 'space_man.png')
         
         # Create sprite sheet object
         sprite_sheet = SpriteSheet(sprite_path)
         
         # Calculate exact dimensions
         sprite_width = 1700 // 5  # = 340
         sprite_height = 1500 // 3  # ≈ 500
         
         # Load animations for each direction
         self.sprites = {
             'down': sprite_sheet.load_strip((0, 0, sprite_width, sprite_height), 5, None),
             'up': sprite_sheet.load_strip((0, sprite_height, sprite_width, sprite_height), 5, None),
             'left': sprite_sheet.load_strip((0, sprite_height*2, sprite_width, sprite_height), 5, None)
         }
         
         # For right-facing animations, flip the left-facing sprites
         self.sprites['right'] = []
         for img in self.sprites['left']:
             self.sprites['right'].append(pygame.transform.flip(img, True, False))
 
     
    def update_sprite(self):
         if self.sprites:
             # Get the current animation frame
             try:
                 self.image = self.sprites[self.direction][self.current_frame]
                 # Scale the image if needed
                 self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
             except (KeyError, IndexError):
                 # Fallback if sprite loading fails
                 self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
                 self.image.fill(BLUE)
         else:
             # Fallback to original colored rectangle
             self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
             self.image.fill(BLUE)
        
    
    def move(self, dx, dy):
         # Update direction based on movement
         if dx > 0:
             self.direction = 'right'
         elif dx < 0:
             self.direction = 'left'
         elif dy > 0:
             self.direction = 'down'
         elif dy < 0:
             self.direction = 'up'
         
         # Set moving flag
         self.moving = dx != 0 or dy != 0
         
         # Update animation
         current_time = pygame.time.get_ticks()
         if self.moving and current_time - self.animation_timer > self.animation_speed:
             self.animation_timer = current_time
             self.current_frame = (self.current_frame + 1) % len(self.sprites[self.direction])
             self.update_sprite()
         
         # Call the original move method
         super().move(dx, dy)
 
    


ITEMS = [BaseTile, Block, Herb, Glowvine, Bacteria, Mysterious]


        
 
    
    
        
    
