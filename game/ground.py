from graphic.shapes import draw_polygon
from graphic.scan_line import scanline_polygon

class Ground:
    """
    Represents the ground as a polygon rendered using
    Bresenham line drawing and scanline filling.
    """

    def __init__(self, ground_y, width, height):
        """
        Initialize the ground polygon.

        Args:
            ground_y (int): Y coordinate where the ground starts.
            width (int): Screen width.
            height (int): Screen height.
        """
        self.points = [
            (0, ground_y),
            (width, ground_y),
            (width, height),
            (0, height)
        ]
        self.colors = {
            "border": (0, 0, 0),  # Dark Green
            "fill": (80, 160, 80)     # Light Green
        }

    def draw(self, surface):
        """
        Draw the ground polygon outline and fill it using scanline.
        """
        # Draw polygon outline
        draw_polygon(surface, self.points, self.colors["border"])

        # Fill polygon interior
        scanline_polygon(surface, self.points, self.colors["fill"])
