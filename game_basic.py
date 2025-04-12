import pygame
import sys
import os  # For path handling

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
            [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.wall_rects = []
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
        # Create rectangles for walls for collision detection
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 1:
                    self.wall_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    
    def draw(self, surface):
        # Draw the background image first
        surface.blit(self.background, (0, 0))
        
        # Draw only the walls and grid lines
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if cell == 1:
                    pygame.draw.rect(surface, BROWN, rect)  # wall
                pygame.draw.rect(surface, BLACK, rect, 1)  # grid lines

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
