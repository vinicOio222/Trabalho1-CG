"""Module for drawing a basketball hoop using Pygame."""
from graphic.scan_line import hoop_scanline, scanline_polygon
from graphic.shapes import draw_ellipse, draw_hoop_net_basic, draw_line_bresenham, draw_polygon, draw_polygon_clipping


class BasketHoop:
    """Class representing a basketball hoop."""
    def __init__(self, xc, yc, ground_y=600):
        self.a_outer = 30 # Outer ellipse semi-major axis
        self.b_outer = 8 # Outer ellipse semi-minor axis
        self.a_inner = 26  # Inner ellipse semi-major axis
        self.b_inner = 6 # Inner ellipse semi-minor axis
        self.xc = xc
        self.yc = yc
        self.ground_y = ground_y  # Y coordinate of the ground
        self.pole_width = 10  # Width of the pole
        self.net_height = 40
        self.net_spacing = 8
        self.colors = {
            "fill": (255, 0, 0),
            "border": (0, 0, 0),
            "net": (255, 255, 255),
            "pole": (0, 0, 0)  # Black color for the pole
        }

    def draw(self, surface):
        """Draw the basketball hoop on the given surface."""
        
        # Draw the pole (behind the hoop)
        # Pole goes from the top of the hoop to the ground
        pole_top_y = self.yc - self.b_outer
        pole_points = [
            (self.xc + self.a_outer, pole_top_y),  # Top right
            (self.xc + self.a_outer + self.pole_width, pole_top_y),  # Top right outer
            (self.xc + self.a_outer + self.pole_width, self.ground_y),  # Bottom right
            (self.xc + self.a_outer, self.ground_y)  # Bottom left
        ]
        
        # Draw pole outline
        draw_polygon(surface, pole_points, self.colors["border"])
        
        # Fill the pole
        scanline_polygon(surface, pole_points, self.colors["pole"])

        draw_hoop_net_basic(
            surface,
            self.xc,
            self.yc + self.b_inner,
            self.a_inner,
            self.net_height,
            self.colors["net"]
        )

        # Draw outer and inner ellipses
        draw_ellipse(
            surface,
            self.xc,
            self.yc,
            self.a_outer,
            self.b_outer,
            self.colors["border"]
        )

        draw_ellipse(
            surface,
            self.xc,
            self.yc,
            self.a_inner,
            self.b_inner,
            self.colors["border"]
        )

        # Scan-line fill the hoop shape
        hoop_scanline(
            surface, self.xc, self.yc,
            self.a_outer, self.b_outer,
            self.a_inner, self.b_inner,
            self.colors["fill"], self.colors["border"]
        )

        

    def check_score(self, ball):
        """Check if the ball passed through the hoop to score."""
        # Check if ball is in the horizontal range of the hoop
        if abs(ball.xc - self.xc) <= self.a_inner:
            # Check if ball is at the hoop level and moving downward
            if (self.yc - 5 <= ball.yc <= self.yc + 15 and 
                ball.velocity[1] > 0):
                return True
        return False
