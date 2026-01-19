"""Main module for the basket ball game application."""
import pygame
from core.screen import Screen
from graphic.shapes import line_dda


def main():
    """Main function to run the basket ball game application."""
    screen = Screen()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.clear((0, 0, 0))
        # Example of setting a pixel in the center of the screen
        line_dda(screen.screen, 100, 100, 700, 500, (255, 0, 0))
        screen.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
    
