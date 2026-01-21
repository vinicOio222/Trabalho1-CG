"""BasketBall class representing a basketball with drawing and movement capabilities."""

from graphic.scan_line import circle_scanline
from graphic.shapes import draw_circle, draw_line, draw_arc


class BasketBall:
    """Class representing a basketball."""
    def __init__(self, xc, yc):
        self.xc = xc
        self.yc = yc
        self.velocity = [0, 0]
        self.r = 15
        self.colors = {
            "fill": (255, 165, 0),
            "border_and_details": (0, 0, 0)
        }

    def draw(self, surface):
        """Draw the basketball on the given surface."""
        # Draw the outer circle and cross details
        draw_circle(surface, self.xc, self.yc, self.r, self.colors["border_and_details"])
        draw_line(surface, self.xc - self.r, self.yc, self.xc + self.r, self.yc, self.colors["border_and_details"])
        draw_line(surface, self.xc, self.yc - self.r, self.xc, self.yc + self.r,self.colors["border_and_details"])

        r_arc = int(self.r * 1.6) # Radius for the arcs

        # Draw the arcs for basketball details
        # Right arc
        draw_arc(
            surface,
            self.xc + self.r,
            self.yc,
            r_arc,
            self.xc,
            self.yc,
            self.r,
            self.colors["border_and_details"]
        )
        # Left arc
        draw_arc(
            surface,
            self.xc - self.r,
            self.yc,
            r_arc,
            self.xc,
            self.yc,
            self.r,
            self.colors["border_and_details"]
        )

        # Fill the circle using scan-line algorithm
        circle_scanline(
            surface,
            self.xc,
            self.yc,
            self.r,
            self.colors["fill"],
            self.colors["border_and_details"]
        )

    def shot(self, vx, vy):
        """Set the initial velocity of the basketball."""
        self.velocity = [vx, vy]

    def update(self, gravity=0.5):
        """Update the position of the basketball based on its velocity and gravity."""
        self.velocity[1] += gravity
        self.xc += self.velocity[0]
        self.yc += self.velocity[1]
