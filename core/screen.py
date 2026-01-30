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

        # Get minimap clipping window coordinates
        xmin, ymin, xmax, ymax = minimap_bounds[0], minimap_bounds[1], minimap_bounds[0] + minimap_bounds[2] - 1, minimap_bounds[1] + minimap_bounds[3] - 1

        # Draw on minimap (simplified versions)
        # Ground on minimap (uses polygon clipping)
        draw_polygon_clipping(
            surface,
            [
                (int(ground_mini_start[0]), int(ground_mini_start[1])),
                (int(ground_mini_end[0]), int(ground_mini_end[1])),
                (int(ground_mini_end[0]), ymax),
                (int(ground_mini_start[0]), ymax)
            ],
            (xmin, ymin, xmax, ymax),
            ground.colors["fill"]
        )
        scanline_polygon_clipping(
            surface,
            [
                (int(ground_mini_start[0]), int(ground_mini_start[1])),
                (int(ground_mini_end[0]), int(ground_mini_end[1])),
                (int(ground_mini_end[0]), ymax),
                (int(ground_mini_start[0]), ymax)
            ],
            ground.colors["fill"],
            xmin, ymin, xmax, ymax
        )

        # Ball on minimap (uses circle clipping)
        draw_circle_clipping(
            surface,
            int(ball_mini_x),
            int(ball_mini_y),
            max(1, ball_mini_r),  # Use scaled radius, minimum 1 pixel
            xmin, ymin, xmax, ymax,
            ball.colors["fill"]
        )
        circle_scanline(
            surface,
            int(ball_mini_x),
            int(ball_mini_y),
            max(1, ball_mini_r),
            ball.colors["fill"],
            ball.colors["border_and_details"],
            (xmin, ymin, xmax, ymax)
        )
    
        # Pole on minimap (draw behind the hoop)
        pole_top_y = hoop.yc - hoop.b_outer
        pole_mini_top_x, pole_mini_top_y = transform_point(hoop.xc + hoop.a_outer, pole_top_y, world_to_minimap)
        pole_mini_top_outer_x, pole_mini_top_outer_y = transform_point(hoop.xc + hoop.a_outer + hoop.pole_width, pole_top_y, world_to_minimap)
        pole_mini_bottom_x, pole_mini_bottom_y = transform_point(hoop.xc + hoop.a_outer, hoop.ground_y, world_to_minimap)
        pole_mini_bottom_outer_x, pole_mini_bottom_outer_y = transform_point(hoop.xc + hoop.a_outer + hoop.pole_width, hoop.ground_y, world_to_minimap)
        
        pole_mini_points = [
            (int(pole_mini_top_x), int(pole_mini_top_y)),
            (int(pole_mini_top_outer_x), int(pole_mini_top_outer_y)),
            (int(pole_mini_bottom_outer_x), int(pole_mini_bottom_outer_y)),
            (int(pole_mini_bottom_x), int(pole_mini_bottom_y))
        ]
        
        draw_polygon_clipping(surface, pole_mini_points, (xmin, ymin, xmax, ymax), hoop.colors["border"])
        scanline_polygon_clipping(surface, pole_mini_points, hoop.colors["pole"], xmin, ymin, xmax, ymax)

        # Backboard on minimap (draw behind the hoop)
        backboard_x = hoop.xc + hoop.a_outer - 5
        backboard_y = hoop.yc - hoop.backboard_height // 2 - 10  # Same offset as in draw method
        
        backboard_mini_top_left = transform_point(backboard_x, backboard_y, world_to_minimap)
        backboard_mini_top_right = transform_point(backboard_x + hoop.backboard_thickness, backboard_y, world_to_minimap)
        backboard_mini_bottom_left = transform_point(backboard_x, backboard_y + hoop.backboard_height, world_to_minimap)
        backboard_mini_bottom_right = transform_point(backboard_x + hoop.backboard_thickness, backboard_y + hoop.backboard_height, world_to_minimap)
        
        backboard_mini_points = [
            (int(backboard_mini_top_left[0]), int(backboard_mini_top_left[1])),
            (int(backboard_mini_top_right[0]), int(backboard_mini_top_right[1])),
            (int(backboard_mini_bottom_right[0]), int(backboard_mini_bottom_right[1])),
            (int(backboard_mini_bottom_left[0]), int(backboard_mini_bottom_left[1]))
        ]
        
        draw_polygon_clipping(surface, backboard_mini_points, (xmin, ymin, xmax, ymax), hoop.colors["backboard_border"])
        scanline_polygon_clipping(surface, backboard_mini_points, hoop.colors["backboard"], xmin, ymin, xmax, ymax)

        # Hoop on minimap (outer ellipse - uses ellipse clipping)
        draw_ellipse_clipping(
            surface,
            int(hoop_mini_x),
            int(hoop_mini_y),
            int(hoop_mini_a_outer),
            int(hoop_mini_b_outer),
            xmin, ymin, xmax, ymax,
            hoop.colors["fill"]
        )

        # Hoop on minimap (inner ellipse - uses ellipse clipping)
        draw_ellipse_clipping(
            surface,
            int(hoop_mini_x),
            int(hoop_mini_y),
            int(hoop_mini_a_inner),
            int(hoop_mini_b_inner),
            xmin, ymin, xmax, ymax,
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
            (WIDTH-1, 0),
            (WIDTH-1, HEIGHT-1),
            (0, HEIGHT-1)
        ]
        
        # Draw minimap border to show clipping boundaries
        minimap_border = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        draw_polygon(surface, minimap_border, (255, 255, 255))