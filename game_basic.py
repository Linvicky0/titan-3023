import pygame
import sys
import os  # For path handling
from life_bar import LifeBar
# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 50
PLAYER_SPEED = 5

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Map Explorer")
clock = pygame.time.Clock()

# Player class
class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 32, 32)
        self.color = BLUE
        self.speed = PLAYER_SPEED
      
        
    def move(self, dx, dy):
        # Move the player while checking for collisions with map boundaries
        if 0 <= self.rect.x + dx <= SCREEN_WIDTH - self.rect.width:
            self.rect.x += dx
        if 0 <= self.rect.y + dy <= SCREEN_HEIGHT - self.rect.height:
            self.rect.y += dy
            
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Simple map class
class Map:
    def __init__(self):
        # Simple grid-based map: 0 = grass, 1 = wall
        self.grid = [
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 2, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 2, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
        ]
        self.wall_rects = []
        self.clickable_rects = []
        self._create_wall_rects()
        
        # Load background image
        try:
            # Replace 'background.png' with your image file path
            self.background = pygame.image.load('background.jpeg').convert()
            # Scale the background to fit the map size
            map_width = len(self.grid[0]) * TILE_SIZE
            map_height = len(self.grid) * TILE_SIZE
            self.background = pygame.transform.scale(self.background, (map_width, map_height))
        except pygame.error as e:
            print(f"Could not load background image: {e}")
            # Create a fallback background surface
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(GREEN)
        
    def _create_wall_rects(self):
     for y, row in enumerate(self.grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if cell == 1:  # Real walls
                self.wall_rects.append(rect) 
            elif cell == 2:  # Fake walls (clickable)
                self.wall_rects.append(rect)
                self.clickable_rects.append(rect)

    def remove_fake_wall(self, pos):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 2:  # Check if the cell is a fake wall
                    rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if rect.collidepoint(pos):  # If clicked on a fake wall
                        self.grid[y][x] = 0  # Clear the fake wall (set to empty space)
                        self.clickable_rects = [r for r in self.clickable_rects if r != rect]  # Remove from clickable list
                        break
                    
    def draw(self, surface):
    # Draw the background image first
        surface.blit(self.background, (0, 0))

    # Draw real walls
        for rect in self.wall_rects:
            pygame.draw.rect(surface, BROWN, rect)
            pygame.draw.rect(surface, BLACK, rect, 2)  # Optional border

    # Draw clickable objects (fake walls)
        for rect in self.clickable_rects:
            pygame.draw.rect(surface, BROWN, rect)  # Make them look like real walls
            pygame.draw.rect(surface, BLACK, rect, 2)  # Optional border
        
        # # Draw only the walls and grid lines
        # for y, row in enumerate(self.grid):
        #     for x, cell in enumerate(row):
        #         rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        #         if cell == 1:
        #             pygame.draw.rect(surface, BROWN, rect)  # wall
        #         pygame.draw.rect(surface, BLACK, rect, 1)  # grid lines
    # def _create_clickable_rects(self):
    #     # Create rectangles for clickable objects (not real walls)
    #     for y, row in enumerate(self.grid):
    #         for x, cell in enumerate(row):
    #             if cell == 2:  # Clickable objects
    #                 rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    #                 self.clickable_rects.append(rect)
                    
    # def _create_wall_rects(self):
    #     # Create rectangles for real walls for collision detection
    #     for y, row in enumerate(self.grid):
    #         for x, cell in enumerate(row):
    #             if cell == 1:  # Real walls
    #                 rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    #                 self.wall_rects.append(rect)
                
    def check_collision(self, player_rect):
        for wall in self.wall_rects:
            if player_rect.colliderect(wall):
                return True
        return False

# Game class
class Game:
    def __init__(self):
        self.player = Player()
        self.map = Map()
        self.running = True
        self.life_bar = LifeBar(max_life=100, x=10, y=10, width=200, height=20)
        
    # def process_events(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             self.running = False
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             pos = pygame.mouse.get_pos()
    #             for rect in self.map.clickable_rects:
    #                 if rect.collidepoint(pos):
    #                     self.map.clickable_rects.remove(rect)
    #                     break  # Only remove one per click
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.map.remove_fake_wall(pos)  # Remove clicked fake wall and reveal background


                
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
            
        # Check if movement would cause collision with wall
        temp_rect = self.player.rect.copy()
        temp_rect.x += dx
        temp_rect.y += dy
        
        if not self.map.check_collision(temp_rect):
            self.player.move(dx, dy)
    
    def update(self):
        pass
        
    def render(self):
        screen.fill(BLACK)
        self.map.draw(screen)
        self.player.draw(screen)
        self.life_bar.draw(screen)
        pygame.display.flip()
        
    def run(self):
        while self.running:
            self.process_events()
            self.update()
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
