"""Module for managing the game screen using Pygame."""
import pygame

from animation.animation import *
from game.ball import BasketBall
from game.ground import Ground
from game.hoop import BasketHoop
from graphic.shapes import *
from graphic.scan_line import *
from graphic.clipping import cohen_sutherland

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
        
        # Draw minimap border to show clipping boundaries
        minimap_border = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        draw_polygon(surface, minimap_border, (255, 255, 255))

    def display_hoop_zoom(self, surface, ball: BasketBall, hoop: BasketHoop):
        """
        Viewport com zoom na região da cesta.
        Só aparece quando a bola foi arremessada.
        """
        if not ball.is_shot:
            return

        # Janela no mundo (região ao redor da cesta)
        hoop_window = (hoop.xc - 50, hoop.yc - 40, hoop.xc + 50, hoop.yc + 40)

        # Viewport no canto superior direito - formato (xmin, ymin, xmax, ymax)
        zoom_bounds = (620, 10, 790, 140)

        # Matriz de transformação
        world_to_zoom = window_viewport(hoop_window, zoom_bounds)
        sx, sy = get_scale_factors(hoop_window, zoom_bounds)

        # Limites de clipping da viewport
        vxmin, vymin = zoom_bounds[0], zoom_bounds[1]
        vxmax, vymax = zoom_bounds[2], zoom_bounds[3]

        # 1. FUNDO DA VIEWPORT
        bg_points = [(vxmin, vymin), (vxmax, vymin), (vxmax, vymax), (vxmin, vymax)]
        scanline_polygon(surface, bg_points, (135, 206, 235))  # Azul céu

        # 2. POSTE (parte visível)
        pole_top_y = hoop.yc - hoop.b_outer
        pole_points_world = [
            (hoop.xc + hoop.a_outer, pole_top_y),
            (hoop.xc + hoop.a_outer + hoop.pole_width, pole_top_y),
            (hoop.xc + hoop.a_outer + hoop.pole_width, hoop.ground_y),
            (hoop.xc + hoop.a_outer, hoop.ground_y)
        ]
        pole_points_zoom = [transform_point(p[0], p[1], world_to_zoom) for p in pole_points_world]
        pole_points_zoom = [(int(p[0]), int(p[1])) for p in pole_points_zoom]

        draw_polygon_clipping(surface, pole_points_zoom, (vxmin, vymin, vxmax, vymax), hoop.colors["border"])
        scanline_polygon_clipping(surface, pole_points_zoom, hoop.colors["pole"], vxmin, vymin, vxmax, vymax)

        # 3. TABELA (BACKBOARD)
        backboard_x = hoop.xc + hoop.a_outer - 5
        backboard_y = hoop.yc - hoop.backboard_height // 2 - 10
        backboard_points_world = [
            (backboard_x, backboard_y),
            (backboard_x + hoop.backboard_thickness, backboard_y),
            (backboard_x + hoop.backboard_thickness, backboard_y + hoop.backboard_height),
            (backboard_x, backboard_y + hoop.backboard_height)
        ]
        backboard_points_zoom = [transform_point(p[0], p[1], world_to_zoom) for p in backboard_points_world]
        backboard_points_zoom = [(int(p[0]), int(p[1])) for p in backboard_points_zoom]

        draw_polygon_clipping(surface, backboard_points_zoom, (vxmin, vymin, vxmax, vymax), hoop.colors["backboard_border"])
        scanline_polygon_clipping(surface, backboard_points_zoom, hoop.colors["backboard"], vxmin, vymin, vxmax, vymax)

        # 4. REDE (linhas com clipping)
        net_yc = hoop.yc + hoop.b_inner
        net_a = hoop.a_inner
        net_height = hoop.net_height
        spacing = 6
        max_offset = 4

        for x in range(hoop.xc - net_a, hoop.xc + net_a + 1, spacing):
            for i in range(0, net_height, spacing):
                t = i / net_height
                offset = int(max_offset * (1 - t))

                # Linha direita (\)
                x0, y0 = x + offset, net_yc + i
                x1, y1 = x, net_yc + i + spacing
                zx0, zy0 = transform_point(x0, y0, world_to_zoom)
                zx1, zy1 = transform_point(x1, y1, world_to_zoom)
                visible, cx0, cy0, cx1, cy1 = cohen_sutherland(zx0, zy0, zx1, zy1, vxmin, vymin, vxmax, vymax)
                if visible:
                    draw_line_bresenham(surface, int(cx0), int(cy0), int(cx1), int(cy1), hoop.colors["net"])

                # Linha esquerda (/)
                x0, y0 = x - offset, net_yc + i
                x1, y1 = x, net_yc + i + spacing
                zx0, zy0 = transform_point(x0, y0, world_to_zoom)
                zx1, zy1 = transform_point(x1, y1, world_to_zoom)
                visible, cx0, cy0, cx1, cy1 = cohen_sutherland(zx0, zy0, zx1, zy1, vxmin, vymin, vxmax, vymax)
                if visible:
                    draw_line_bresenham(surface, int(cx0), int(cy0), int(cx1), int(cy1), hoop.colors["net"])

        # 5. CESTA (elipses)
        hoop_zx, hoop_zy = transform_point(hoop.xc, hoop.yc, world_to_zoom)
        hoop_za_outer = int(hoop.a_outer * sx)
        hoop_zb_outer = int(hoop.b_outer * sy)
        hoop_za_inner = int(hoop.a_inner * sx)
        hoop_zb_inner = int(hoop.b_inner * sy)

        draw_ellipse_clipping(surface, int(hoop_zx), int(hoop_zy), hoop_za_outer, hoop_zb_outer, vxmin, vymin, vxmax, vymax, hoop.colors["border"])
        draw_ellipse_clipping(surface, int(hoop_zx), int(hoop_zy), hoop_za_inner, hoop_zb_inner, vxmin, vymin, vxmax, vymax, hoop.colors["border"])
        hoop_scanline(surface, int(hoop_zx), int(hoop_zy), hoop_za_outer, hoop_zb_outer, hoop_za_inner, hoop_zb_inner, hoop.colors["fill"], hoop.colors["border"])

        # 6. BOLA
        ball_zx, ball_zy = transform_point(ball.xc, ball.yc, world_to_zoom)
        ball_zr = int(ball.r * min(sx, sy))

        draw_circle_clipping(surface, int(ball_zx), int(ball_zy), ball_zr, vxmin, vymin, vxmax, vymax, ball.colors["border_and_details"])
        circle_scanline(surface, int(ball_zx), int(ball_zy), ball_zr, ball.colors["fill"], ball.colors["border_and_details"], (vxmin, vymin, vxmax, vymax))

        cos_a = math.cos(ball.angle)
        sin_a = math.sin(ball.angle)
        def rotate_around(px, py, cx, cy):
            dx, dy = px - cx, py - cy
            return dx * cos_a - dy * sin_a + cx, dx * sin_a + dy * cos_a + cy

        # Rotated horizontal line
        h1_x, h1_y = rotate_around(ball_zx - ball_zr, ball_zy, ball_zx, ball_zy)
        h2_x, h2_y = rotate_around(ball_zx + ball_zr, ball_zy, ball_zx, ball_zy)
        visible, cx0, cy0, cx1, cy1 = cohen_sutherland(h1_x, h1_y, h2_x, h2_y, vxmin, vymin, vxmax, vymax)
        if visible:
            draw_line_bresenham(surface, int(cx0), int(cy0), int(cx1), int(cy1), ball.colors["border_and_details"])

        # Rotated vertical line
        v1_x, v1_y = rotate_around(ball_zx, ball_zy - ball_zr, ball_zx, ball_zy)
        v2_x, v2_y = rotate_around(ball_zx, ball_zy + ball_zr, ball_zx, ball_zy)
        visible, cx0, cy0, cx1, cy1 = cohen_sutherland(v1_x, v1_y, v2_x, v2_y, vxmin, vymin, vxmax, vymax)
        if visible:
            draw_line_bresenham(surface, int(cx0), int(cy0), int(cx1), int(cy1), ball.colors["border_and_details"])

        r_arc = int(ball_zr * 1.6)  # Radius for the arcs

        # Rotated right arc
        arc_right_x, arc_right_y = rotate_around(ball_zx + ball_zr, ball_zy, ball_zx, ball_zy)
        draw_arc_clipping(
            surface, 
            int(arc_right_x), 
            int(arc_right_y), 
            r_arc, 
            int(ball_zx), 
            int(ball_zy), 
            ball_zr, 
            vxmin, 
            vymin, 
            vxmax, 
            vymax, 
            ball.colors["border_and_details"]
            )

        # Rotated left arc
        arc_left_x, arc_left_y = rotate_around(ball_zx - ball_zr, ball_zy, ball_zx, ball_zy)
        draw_arc_clipping(
            surface, 
            int(arc_left_x), 
            int(arc_left_y), 
            r_arc, 
            int(ball_zx), 
            int(ball_zy), 
            ball_zr, 
            vxmin, 
            vymin, 
            vxmax, 
            vymax, 
            ball.colors["border_and_details"]
            )

        # 7. BORDA DA VIEWPORT
        border = [(vxmin, vymin), (vxmax, vymin), (vxmax, vymax), (vxmin, vymax)]
        draw_polygon(surface, border, (255, 255, 255))