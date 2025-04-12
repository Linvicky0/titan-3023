import pygame 

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Game Timer Example")

# Set up the font
font = pygame.font.SysFont('Consolas', 30)

# Total duration of the timer in seconds
total_time = 60  # 60-second countdown

# Record the start time in milliseconds
start_ticks = pygame.time.get_ticks()