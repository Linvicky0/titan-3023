import pygame
import random
import time

class RainDrop:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.length = random.randint(5, 15)  # Length of raindrop
        self.thickness = random.randint(1, 3)  # Thickness of raindrop

class RainPatch(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # Create a randomly shaped patch by varying width and height slightly
        random_width = width + random.randint(-width//4, width//4)
        random_height = height + random.randint(-height//4, height//4)
        
        # Ensure minimum size
        self.width = max(random_width, width//2)
        self.height = max(random_height, height//2)
        
        # Create the surface with the random dimensions
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Initialize with completely transparent surface
        self.image.fill((0, 0, 0, 0))
        
        # Draw an irregular shape for the rain patch
        self.draw_irregular_shape()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.creation_time = time.time()
        self.duration = 30  # Duration in seconds
        
        # Create raindrops for animation
        self.raindrops = []
        # Slightly fewer drops but larger in size
        self.create_raindrops(int(60 * (self.width * self.height) / (width * height)))
    
    def draw_irregular_shape(self):
        """Draw an irregular shape for the rain patch base - nearly transparent"""
        # Create a barely visible base shape
        base_color = (170, 255, 0, 10)  # Acid green with very high transparency (only 10/255 alpha)
        
        # Draw multiple overlapping circles to create an irregular shape
        num_circles = random.randint(5, 10)
        for _ in range(num_circles):
            center_x = random.randint(0, self.width)
            center_y = random.randint(0, self.height)
            radius = random.randint(self.width//3, self.width//2)
            pygame.draw.circle(self.image, base_color, (center_x, center_y), radius)
    
    def create_raindrops(self, count):
        for _ in range(count):
            # Distribute drops across the entire area
            x = random.randint(-20, self.width + 20)
            y = random.randint(-20, self.height + 20)
            # Slower speed for raindrops
            speed = random.uniform(3, 9)  # Slightly faster for larger drops
            self.raindrops.append(RainDrop(x, y, speed))
    
    def update(self):
        # Check if the rain patch should disappear
        if time.time() - self.creation_time > self.duration:
            self.kill()
            return
        
        # Clear the image completely (fully transparent)
        self.image.fill((0, 0, 0, 0))
        
        # Redraw the irregular base shape
        self.draw_irregular_shape()
        
        # Update and draw raindrops
        for drop in self.raindrops:
            # Move the raindrop diagonally (slower movement)
            drop.x += drop.speed * 0.5
            drop.y += drop.speed * 0.7
            
            # Draw the raindrop as a diagonal line
            start_pos = (int(drop.x), int(drop.y))
            # Adjust end position calculation for larger drops
            end_pos = (int(drop.x - drop.length * 0.5), int(drop.y - drop.length * 0.7))
            
            # Acid green color for methane rain
            # Base color: bright acid green (170, 255, 0)
            # Add slight variation for visual interest
            r = random.randint(150, 190)
            g = random.randint(230, 255)
            b = random.randint(0, 30)
            alpha = random.randint(200, 230)
            
            acid_green = (r, g, b, alpha)
            pygame.draw.line(self.image, acid_green, start_pos, end_pos, drop.thickness)
            
            # If raindrop goes out of bounds, reset it to maintain coverage
            if drop.x > self.width + 20 or drop.y > self.height + 20:
                # Reset to random position at top or left edge
                if random.choice([True, False]):
                    # Reset at top
                    drop.x = random.randint(-20, self.width + 20)
                    drop.y = -drop.length
                else:
                    # Reset at left
                    drop.x = -drop.length
                    drop.y = random.randint(-20, self.height)
    
    @staticmethod
    def check_overlap(new_rect, existing_patches):
        """Check if a new rain patch would overlap with existing ones"""
        for patch in existing_patches:
            if new_rect.colliderect(patch.rect):
                return True
        return False 