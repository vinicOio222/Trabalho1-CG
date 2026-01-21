"""Module to manage and display the game score using Pygame."""
import pygame

class ScoreBoard:
    """Class to manage and display the game score."""
    def __init__(self, x=10, y=10, color=(255, 255, 255), font_size=24):
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.SysFont(None, font_size)
        self.score = 0

    def set_score(self, value):
        """Set the score to a specific value."""
        self.score = value

    def add_points(self, value):
        """Add points to the current score."""
        self.score += value

    def draw(self, surface):
        """Draw the score on the given surface."""
        text = f"Points: {self.score}"
        text_surface = self.font.render(text, True, self.color)
        surface.blit(text_surface, (self.x, self.y))
