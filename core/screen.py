"""Module for managing the game screen using Pygame."""
import pygame

from animation.animation import *
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
        pygame.display.set_caption("Basketball Arcade")

    def clear(self, color=(128,128,128)): # dark gray
        """Clear the screen with the given color."""
        self.canvas.fill(color)

    def update(self): # noqa
        """Update the display."""
        pygame.display.flip()

    def display_minimap(self, surface, ball, hoop:BasketHoop, ):

        world_to_minimap = windown_viewport(world_bounds, minimap_bounds)
        
        # Obter fatores de escala
        sx, sy = get_scale_factors(world_bounds, minimap_bounds)

        # Transformar posição da bola (coordenadas - usa transform_point)
        ball_mini_x, ball_mini_y = transform_point(ball.xc, ball.yc, world_to_minimap)
        ball_mini_r = int(ball.r * min(sx, sy))  # Raio escalonado
        
        # Transformar posição do aro (coordenadas - usa transform_point)
        hoop_mini_x, hoop_mini_y = transform_point(hoop.xc, hoop.yc, world_to_minimap)
        
        # Transformar dimensões do aro (usa transform_dimension, não transform_point!)
        hoop_mini_a_outer, hoop_mini_b_outer = transform_dimension(hoop.a_outer, hoop.b_outer, sx, sy)
        hoop_mini_a_inner, hoop_mini_b_inner = transform_dimension(hoop.a_inner, hoop.b_inner, sx, sy)
        
        # Desenhar no minimapa (versões simplificadas)
        # Bola no minimapa
        draw_circle(
            surface, 
            int(ball_mini_x), 
            int(ball_mini_y), 
            max(1, ball_mini_r),  # Usa raio escalonado, mínimo 1 pixel
            (255, 165, 0)
            )
        circle_scanline(
            surface, 
            int(ball_mini_x), 
            int(ball_mini_y), 
            max(1, ball_mini_r), 
            (255, 165, 0), 
            (0, 0, 0)
            )
        # Bola no minimapa
        draw_ellipse(
            surface, 
            int(hoop_mini_x), 
            int(hoop_mini_y), 
            int(hoop_mini_a_outer),
            int(hoop_mini_b_outer),
            (255, 0, 0)
            )
        
        draw_ellipse(
            surface, 
            int(hoop_mini_x), 
            int(hoop_mini_y), 
            int(hoop_mini_a_inner),
            int(hoop_mini_b_inner),
            (255, 0, 0)
            )
        
        hoop_scanline(
            surface, 
            int(hoop_mini_x), 
            int(hoop_mini_y), 
            int(hoop_mini_a_outer),
            int(hoop_mini_b_outer), 
            int(hoop_mini_a_inner), 
            int(hoop_mini_b_inner), 
            (255, 0, 0), (0, 0, 0)
            )
        
        # Mostrar área visível atual no minimapa (opcional)
        viewport_corners = [
            (0, 0),
            (WIDTH, 0),
            (WIDTH, HEIGHT),
            (0, HEIGHT)
        ]

        minimap_corners = [transform_point(x, y, world_to_minimap) for x, y in viewport_corners]
        if len(minimap_corners) >= 2:
            draw_polygon(surface, minimap_corners, (0, 0, 0))
    
