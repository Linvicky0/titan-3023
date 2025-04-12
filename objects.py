import pygame
from constants import *
import sys
from game import GAME_END
import random
from life_bar import LifeBar


# END GAME WHEN TIMER UP OR INVENTORY FULL

# All objects are one of these 3 categories: blank tile, collectible, or a block (can't move through it)

sprite_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()

class BaseTile(pygame.sprite.Sprite):


    def __init__(self, x, y, img = None):
        super().__init__()
        self.rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        sprite_group.add(self)
    
    def move(self, dx, dy):
        # Move the player while checking for collisions with map boundaries
        if 0 <= self.rect.x + dx <= SCREEN_WIDTH - self.rect.width:
            self.rect.x += dx
           
        if 0 <= self.rect.y + dy <= SCREEN_HEIGHT - self.rect.height:
            self.rect.y += dy
    

class Block(BaseTile):
    
    def __init__(self, x, y, img = None):
        super().__init__(x, y)
        if not img:
            self.image.fill(BROWN)
        else:
            self.image = pygame.transform.scale(img, (TILE_SIZE - 5, TILE_SIZE - 5))
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
            player.inventory_slots[free_slots[0]] = True
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
        super().__init__(x, y, pygame.image.load(f"{IMG_DIR}herb.png"))     
        self.reward = 5

class Bacteria(Collectible):

    def __init__(self, x, y):
        super().__init__(x, y, pygame.image.load(f"{IMG_DIR}bacteria.png"))
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
        super().__init__(x, y, pygame.image.load(f"{IMG_DIR}person.png"))
        self.speed = DEFAULT_SPEED
        self.inventory_items = {} # map object type to their slot and count
        self.inventory_slots = [0] * int(len(ITEMS)/2) # 0 means slot is unused
        self.life_bar = LifeBar(max_life=100, x=10, y=10, width=200, height=20)
        
   
            

ITEMS = [BaseTile, Block, Herb, Bacteria, Mysterious]

        
 
    
    
        
    
