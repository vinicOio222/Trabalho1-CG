"""BasketBall class representing a basketball with drawing and movement capabilities."""

from graphic.scan_line import circle_scanline
from graphic.shapes import draw_circle, draw_line, draw_arc


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
        self.colors = {
            "fill": (255, 165, 0),
            "border_and_details": (0, 0, 0)
        }

    def draw(self, surface):
        """Draw the basketball on the given surface."""
        # Convert coordinates to integers for drawing
        xc = int(self.xc)
        yc = int(self.yc)
        
        # Draw the outer circle and cross details
        draw_circle(surface, xc, yc, self.r, self.colors["border_and_details"])
        draw_line(surface, xc - self.r, yc, xc + self.r, yc, self.colors["border_and_details"])
        draw_line(surface, xc, yc - self.r, xc, yc + self.r,self.colors["border_and_details"])

        r_arc = int(self.r * 1.6) # Radius for the arcs

        # Draw the arcs for basketball details
        # Right arc
        draw_arc(
            surface,
            xc + self.r,
            yc,
            r_arc,
            xc,
            yc,
            self.r,
            self.colors["border_and_details"]
        )
        # Left arc
        draw_arc(
            surface,
            xc - self.r,
            yc,
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

    def update(self, gravity=0.5):
        """Update the position of the basketball based on its velocity and gravity."""
        if self.is_shot:
            self.velocity[1] += gravity
            self.xc += self.velocity[0]
            self.yc += self.velocity[1]

    def reset(self):
        """Reset the ball to its initial position."""
        self.xc = self.initial_x
        self.yc = self.initial_y
        self.velocity = [0, 0]
        self.is_shot = False
        self.is_dragging = False
        self.drag_start = None

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
            self.shot(vx, vy)
            self.is_dragging = False
            self.drag_start = None
