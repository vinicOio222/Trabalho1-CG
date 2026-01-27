"""BasketBall class representing a basketball with drawing and movement capabilities."""

from graphic.scan_line import circle_scanline
from graphic.shapes import draw_circle, draw_line_bresenham, draw_arc

import math

class BasketBall:
    """Class representing a basketball."""
    def __init__(self, xc, yc):
        self.initial_x = xc
        self.initial_y = yc
        self.xc = xc
        self.yc = yc
        self.velocity = [0, 0]
        self.r = 15
        self.is_shot = False
        self.is_dragging = False
        self.drag_start = None
        self.angle = 0  # Ângulo atual em radianos
        self.angular_velocity = 0  # Velocidade angular
        self.colors = {
            "fill": (255, 165, 0),
            "border_and_details": (0, 0, 0)
        }

    def _rotate_point(self, x, y):
        """Rotaciona um ponto (x, y) ao redor do centro da bola."""
        dx = x - self.xc
        dy = y - self.yc
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)
        x_new = dx * cos_a - dy * sin_a + self.xc
        y_new = dx * sin_a + dy * cos_a + self.yc
        return x_new, y_new
    
    def draw(self, surface):
        """Draw the basketball on the given surface."""
        # Convert coordinates to integers for drawing
        xc = int(self.xc)
        yc = int(self.yc)
        
        # Draw the outer circle and cross details
        draw_circle(surface, xc, yc, self.r, self.colors["border_and_details"])
        # Linha horizontal rotacionada
        h1_x, h1_y = self._rotate_point(xc - self.r, yc)
        h2_x, h2_y = self._rotate_point(xc + self.r, yc)
        draw_line_bresenham(surface, int(h1_x), int(h1_y), int(h2_x), int(h2_y), self.colors["border_and_details"])
        # Linha vertical rotacionada
        v1_x, v1_y = self._rotate_point(xc, yc - self.r)
        v2_x, v2_y = self._rotate_point(xc, yc + self.r)
        draw_line_bresenham(surface, int(v1_x), int(v1_y), int(v2_x), int(v2_y), self.colors["border_and_details"])

        r_arc = int(self.r * 1.6) # Radius for the arcs

        # Right arc rotacionado
        arc_right_x, arc_right_y = self._rotate_point(xc + self.r, yc)
        draw_arc(
            surface,
            int(arc_right_x),
            int(arc_right_y),
            r_arc,
            xc,
            yc,
            self.r,
            self.colors["border_and_details"]
        )
        # Left arc rotacionado
        arc_left_x, arc_left_y = self._rotate_point(xc - self.r, yc)
        draw_arc(
            surface,
            int(arc_left_x),
            int(arc_left_y),
            r_arc,
            xc,
            yc,
            self.r,
            self.colors["border_and_details"]
        )

        # Fill the circle using scan-line algorithm
        circle_scanline(
            surface,
            xc,
            yc,
            self.r,
            self.colors["fill"],
            self.colors["border_and_details"]
        )

    def shot(self, vx, vy):
        """Set the initial velocity of the basketball."""
        self.velocity = [vx, vy]
        self.is_shot = True

    # Translation
    def update(self, gravity=0.5):
        """Update the position of the basketball based on its velocity and gravity."""
        if self.is_shot:
            self.velocity[1] += gravity
            self.xc += self.velocity[0]
            self.yc += self.velocity[1]
            self.angle += self.angular_velocity

    def reset(self):
        """Reset the ball to its initial position."""
        self.xc = self.initial_x
        self.yc = self.initial_y
        self.velocity = [0, 0]
        self.is_shot = False
        self.is_dragging = False
        self.drag_start = None
        self.angle = 0  # Reseta ângulo
        self.angular_velocity = 0

    def is_out_of_bounds(self, width, height):
        """Check if the ball is out of bounds."""
        return (self.xc < -50 or self.xc > width + 50 or 
                self.yc < -50 or self.yc > height + 50)

    def start_drag(self, mouse_x, mouse_y):
        """Start dragging the ball for slingshot."""
        # Check if mouse is near the ball
        dx = mouse_x - self.xc
        dy = mouse_y - self.yc
        distance = (dx**2 + dy**2)**0.5
        if distance <= self.r * 2 and not self.is_shot:
            self.is_dragging = True
            self.drag_start = (self.xc, self.yc)
            return True
        return False

    def update_drag(self, mouse_x, mouse_y):
        """Update drag position."""
        if self.is_dragging:
            # Limit drag distance
            dx = self.initial_x - mouse_x
            dy = self.initial_y - mouse_y
            distance = (dx**2 + dy**2)**0.5
            max_distance = 100
            if distance > max_distance:
                ratio = max_distance / distance
                dx *= ratio
                dy *= ratio
            self.xc = self.initial_x - dx
            self.yc = self.initial_y - dy

    def release_drag(self):
        """Release the slingshot and shoot the ball."""
        if self.is_dragging:
            # Calculate velocity based on drag distance
            vx = (self.initial_x - self.xc) * 0.3
            vy = (self.initial_y - self.yc) * 0.3
            self.angular_velocity = vx * 0.01
            self.shot(vx, vy)
            self.is_dragging = False
            self.drag_start = None
