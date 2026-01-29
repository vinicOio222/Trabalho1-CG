"""Module for managing the game screen using Pygame."""
import pygame

from animation.animation import *
from game.ball import BasketBall
from game.ground import Ground
from game.hoop import BasketHoop
from graphic.shapes import *
from graphic.scan_line import *

WIDTH, HEIGHT = 800, 600
world_bounds = (0, 0, WIDTH, HEIGHT)
minimap_bounds = (10, 10, 160, 120)

class Screen:
    """Class representing the game screen."""

    def __init__(self):
        pygame.init()
        self.canvas = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.render_sky()
        pygame.display.set_caption("Basketball Arcade")

    def render_sky(self, top_color=(30, 80, 180), bottom_color=(180, 220, 255)): # noqa
        """Clear the screen with the given color."""
        scanline_gradient_sky(
            self.background,
            top_color,
            bottom_color
        )

    def clear(self): # noqa
        """Clear the screen with a sky gradient."""
        self.canvas.blit(self.background, (0, 0))

    def update(self): # noqa
        """Update the display."""
        pygame.display.flip()

    def display_minimap(self, surface, ball:BasketBall, hoop:BasketHoop, ground: Ground): # noqa
        """
        Render a minimap showing the ball and hoop positions.

        Args:
            surface: The pygame surface to draw the minimap on.
            ball (BasketBall): The basketball object to display.
            hoop (BasketHoop): The basketball hoop object to display.
        """
        world_to_minimap = window_viewport(world_bounds, minimap_bounds)

        # Get scale factors
        sx, sy = get_scale_factors(world_bounds, minimap_bounds)

        # Transform ball position (coordinates - uses transform_point)
        ball_mini_x, ball_mini_y = transform_point(ball.xc, ball.yc, world_to_minimap)
        ball_mini_r = int(ball.r * min(sx, sy))  # Scaled radius

        # Transform hoop position (coordinates - uses transform_point)
        hoop_mini_x, hoop_mini_y = transform_point(hoop.xc, hoop.yc, world_to_minimap)

        # Transform hoop dimensions (uses transform_dimension, not transform_point!)
        hoop_mini_a_outer, hoop_mini_b_outer = transform_dimension(hoop.a_outer, hoop.b_outer, sx, sy)
        hoop_mini_a_inner, hoop_mini_b_inner = transform_dimension(hoop.a_inner, hoop.b_inner, sx, sy)
        # Transform ground points

        ground_mini_start = transform_point(ground.points[0][0], ground.points[0][1], world_to_minimap)
        ground_mini_end = transform_point(ground.points[1][0], ground.points[1][1], world_to_minimap)

        # Draw on minimap (simplified versions)
        # Ground on minimap
        draw_polygon(
            surface,
            [
                (int(ground_mini_start[0]), int(ground_mini_start[1])),
                (int(ground_mini_end[0]), int(ground_mini_end[1])),
                (int(ground_mini_end[0]), minimap_bounds[3]),
                (int(ground_mini_start[0]), minimap_bounds[3])
            ],
            ground.colors["fill"]
        )
        scanline_polygon(
            surface,
            [
                (int(ground_mini_start[0]), int(ground_mini_start[1])),
                (int(ground_mini_end[0]), int(ground_mini_end[1])),
                (int(ground_mini_end[0]), minimap_bounds[3]),
                (int(ground_mini_start[0]), minimap_bounds[3])
            ],
            ground.colors["fill"],
        )

        # Ball on minimap
        draw_circle(
            surface,
            int(ball_mini_x),
            int(ball_mini_y),
            max(1, ball_mini_r),  # Use scaled radius, minimum 1 pixel
            ball.colors["fill"]
        )
        circle_scanline(
            surface,
            int(ball_mini_x),
            int(ball_mini_y),
            max(1, ball_mini_r),
            ball.colors["fill"],
            ball.colors["border_and_details"]
        )

        # Hoop on minimap (outer ellipse)
        draw_ellipse(
            surface,
            int(hoop_mini_x),
            int(hoop_mini_y),
            int(hoop_mini_a_outer),
            int(hoop_mini_b_outer),
            hoop.colors["fill"]
        )

        # Hoop on minimap (inner ellipse)
        draw_ellipse(
            surface,
            int(hoop_mini_x),
            int(hoop_mini_y),
            int(hoop_mini_a_inner),
            int(hoop_mini_b_inner),
            hoop.colors["fill"]
        )

        # Hoop scanline rendering
        hoop_scanline(
            surface,
            int(hoop_mini_x),
            int(hoop_mini_y),
            int(hoop_mini_a_outer),
            int(hoop_mini_b_outer),
            int(hoop_mini_a_inner),
            int(hoop_mini_b_inner),
            hoop.colors["fill"],
            hoop.colors["border"]
        )

        # Show current visible area on minimap (optional)
        viewport_corners = [
            (0, 0),
            (WIDTH, 0),
            (WIDTH, HEIGHT),
            (0, HEIGHT)
        ]

        minimap_corners = [transform_point(x, y, world_to_minimap) for x, y in viewport_corners]
        if len(minimap_corners) >= 2:
            draw_polygon(surface, minimap_corners, (0, 0, 0))