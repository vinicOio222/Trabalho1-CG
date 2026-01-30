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
        
        # Backboard properties
        self.backboard_width = 70
        self.backboard_height = 60
        self.backboard_thickness = 3
        
        self.colors = {
            "fill": (255, 0, 0),
            "border": (0, 0, 0),
            "net": (255, 255, 255),
            "pole": (0, 0, 0),  # Black color for the pole
            "backboard": (255, 255, 255),  # White backboard
            "backboard_border": (255, 0, 0)  # Red border
        }

    def draw(self, surface):
        """Draw the basketball hoop on the given surface."""
        
        # Draw the backboard (behind everything)
        backboard_x = self.xc + self.a_outer - 5
        backboard_y = self.yc - self.backboard_height // 2 - 10  # Moved up by 10 pixels
        
        backboard_points = [
            (backboard_x, backboard_y),
            (backboard_x + self.backboard_thickness, backboard_y),
            (backboard_x + self.backboard_thickness, backboard_y + self.backboard_height),
            (backboard_x, backboard_y + self.backboard_height)
        ]
        
        # Draw backboard border
        draw_polygon(surface, backboard_points, self.colors["backboard_border"])
        
        # Fill the backboard
        scanline_polygon(surface, backboard_points, self.colors["backboard"])
        
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

    def check_backboard_collision(self, ball):
        """
        Check and handle collision between ball and backboard.
        
        Args:
            ball: The basketball object to check collision with.
            
        Returns:
            bool: True if collision occurred, False otherwise.
        """
        backboard_x = self.xc + self.a_outer - 5
        backboard_y = self.yc - self.backboard_height // 2 - 10  # Same offset as in draw method
        backboard_right = backboard_x + self.backboard_thickness
        backboard_bottom = backboard_y + self.backboard_height
        
        # Check if ball is colliding with the backboard (front face)
        if (backboard_x - ball.r <= ball.xc <= backboard_right + ball.r and
            backboard_y - ball.r <= ball.yc <= backboard_bottom + ball.r):
            
            # Ball is approaching from the left (front of backboard)
            if ball.velocity[0] > 0 and ball.xc < backboard_x + ball.r:
                ball.xc = backboard_x - ball.r
                ball.velocity[0] = -ball.velocity[0] * 0.7  # Bounce back with some energy loss
                return True
                
        return False

    def check_pole_collision(self, ball):
        """
        Check and handle collision between ball and pole.
        
        Args:
            ball: The basketball object to check collision with.
            
        Returns:
            bool: True if collision occurred, False otherwise.
        """
        pole_top_y = self.yc - self.b_outer
        pole_left = self.xc + self.a_outer
        pole_right = pole_left + self.pole_width
        
        # Check if ball is colliding with the pole
        if (pole_left - ball.r <= ball.xc <= pole_right + ball.r and
            pole_top_y - ball.r <= ball.yc <= self.ground_y):
            
            # Determine which side of the pole the ball hit
            ball_center_x = ball.xc
            pole_center_x = (pole_left + pole_right) / 2
            
            # Ball is approaching from the left
            if ball.velocity[0] > 0 and ball_center_x < pole_center_x:
                ball.xc = pole_left - ball.r
                ball.velocity[0] = -ball.velocity[0] * 0.6  # Bounce back
                return True
            
            # Ball is approaching from the right
            elif ball.velocity[0] < 0 and ball_center_x > pole_center_x:
                ball.xc = pole_right + ball.r
                ball.velocity[0] = -ball.velocity[0] * 0.6  # Bounce back
                return True
                
        return False
