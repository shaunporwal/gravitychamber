





import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Initialize pixel array with 300 black pixels randomly placed
pixels = [BLACK] * 1000
for i in range(300):
    index = random.randint(0, 999)
    pixels[index] = WHITE

# Main game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move black pixels to random adjacent white pixel spots
    for i in range(1000):
        if pixels[i] == BLACK:
            adjacent_indices = [j for j in range(i-1, i+2) if j >= 0 and j < 1000 and pixels[j] == WHITE]
            if adjacent_indices:
                new_index = random.choice(adjacent_indices)
                pixels[new_index] = BLACK
                pixels[i] = WHITE

    # Draw pixels on window
    for i in range(1000):
        pygame.draw.rect(window, pixels[i], (i, 0, 1, 1))

    # Update window
    pygame.display.update()

# Quit Pygame
pygame.quit()
