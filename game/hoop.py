"""Module for drawing a basketball hoop using Pygame."""
from graphic.scan_line import hoop_scanline
from graphic.shapes import draw_ellipse


class BasketHoop:
    """Class representing a basketball hoop."""
    def __init__(self, xc, yc):
        self.a_outer = 30 # Outer ellipse semi-major axis
        self.b_outer = 8 # Outer ellipse semi-minor axis
        self.a_inner = 26  # Inner ellipse semi-major axis
        self.b_inner = 6 # Inner ellipse semi-minor axis
        self.xc = xc
        self.yc = yc
        self.colors = [(255, 0, 0), (0, 0, 0)]  # Red hoop with black outline

    def draw(self, surface):
        """Draw the basketball hoop on the given surface."""

        # Draw outer and inner ellipses
        draw_ellipse(
            surface,
            self.xc,
            self.yc,
            self.a_outer,
            self.b_outer,
            self.colors[1]
        )

        draw_ellipse(
            surface,
            self.xc,
            self.yc,
            self.a_inner,
            self.b_inner,
            self.colors[1]
        )

        # Scan-line fill the hoop shape
        hoop_scanline(
            surface, self.xc, self.yc,
            self.a_outer, self.b_outer,
            self.a_inner, self.b_inner,
            self.colors[0], self.colors[1]
        )
