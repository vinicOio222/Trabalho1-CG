"""Module for managing the game screen using Pygame."""
import pygame

WIDTH, HEIGHT = 800, 600

class Screen:
    """Class representing the game screen."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Basketball Arcade")

    def clear(self, color=(0, 0, 0)):
        """Clear the screen with the given color."""
        self.screen.fill(color)

    def update(self): # noqa
        """Update the display."""
        pygame.display.flip()
