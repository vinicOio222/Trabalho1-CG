"""Module for the start screen with title animation and music."""
import pygame
import math
from graphic.shapes import draw_circle, draw_polygon, set_pixel
from graphic.floodfill import flood_fill


class StartScreen:
    """Class representing the start screen with animated title."""
    
    def __init__(self, width=800, height=600):
        """Initialize the start screen."""
        self.width = width
        self.height = height
        self.alpha = 0  # For fade in/out animation
        self.alpha_direction = 1  # 1 for fading in, -1 for fading out
        self.alpha_speed = 3
        self.start_pressed = False
        
        # Load and play background music
        try:
            pygame.mixer.init()
            # To add music to your game:
            # 1. Place a music file (mp3, ogg, or wav) in the project directory
            # 2. Uncomment the lines below and update the path
            pygame.mixer.music.load("menu/spacejam.mp3")  # Change to your music file path
            pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
            pygame.mixer.music.play(-1)  # Loop indefinitely (-1) or specify number of times
        except Exception as e:
            print(f"Could not load music: {e}")
            pass  # If music file not found, continue without music
    
    def draw_background(self, surface):
        """Draw the background using floodfill."""
        # Draw a border rectangle for the background
        border_color = (0, 0, 0)
        fill_color = (20, 30, 80)  # Dark blue background
        
        # Clear surface first
        surface.fill((0, 0, 0))
        
        # Draw border for the entire screen
        points = [
            (0, 0),
            (self.width, 0),
            (self.width , self.height),
            (0, self.height )
        ]
        draw_polygon(surface, points, border_color)
        
        # Fill the background
        flood_fill(surface, self.width // 2, self.height // 2, fill_color, border_color)
        
        # Draw decorative stars in the background
        self._draw_stars(surface)
    
    def _draw_stars(self, surface):
        """Draw decorative stars in the background."""
        star_positions = [
            (100, 80), (250, 120), (600, 90), (720, 150),
            (150, 450), (680, 480), (50, 300), (750, 350),
            (400, 50), (300, 500)
        ]
        
        for x, y in star_positions:
            # Draw small circles as stars
            draw_circle(surface, x, y, 2, (255, 255, 200))
    
    def draw_title(self, surface):
        """Draw the game title with animation."""
        # Main title
        font = pygame.font.SysFont('arial', 72, bold=True)
        title_text = "BASKETBALL"
        
        # Calculate color with alpha animation
        color_value = int(self.alpha)
        title_color = (color_value, color_value, 255)
        
        # Render title
        text_surface = font.render(title_text, True, title_color)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 3))
        surface.blit(text_surface, text_rect)
        
        # Subtitle
        subtitle_font = pygame.font.SysFont('arial', 36)
        subtitle_text = "ARCADE"
        subtitle_color = (color_value, 255, color_value)
        
        subtitle_surface = subtitle_font.render(subtitle_text, True, subtitle_color)
        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, self.height // 3 + 70))
        surface.blit(subtitle_surface, subtitle_rect)
        
        # Draw basketball icon near title
        self._draw_basketball_icon(surface, self.width // 2 - 180, self.height // 3, color_value)
        self._draw_basketball_icon(surface, self.width // 2 + 180, self.height // 3, color_value)
    
    def _draw_basketball_icon(self, surface, x, y, alpha):
        """Draw a small basketball icon using the shapes functions."""
        r = 25
        color = (min(255, alpha + 100), min(165, int(alpha * 0.65)), 0)  # Orange color
        
        # Draw basketball circle
        draw_circle(surface, x, y, r, color)
        
        # Fill the basketball
        if alpha > 50:  # Only fill when visible enough
            flood_fill(surface, x, y, color, color)
            
            # Draw basketball lines
            line_color = (0, 0, 0)
            # Vertical line
            points_v = [(x, y - r), (x, y + r)]
            draw_polygon(surface, points_v, line_color)
            
            # Curved lines (approximated with points)
            for angle in [60, 120, 240, 300]:
                rad = math.radians(angle)
                x1 = int(x + r * math.cos(rad))
                y1 = int(y + r * math.sin(rad))
                points = [(x, y - r), (x1, y1), (x, y + r)]
    
    def draw_instructions(self, surface):
        """Draw instructions for starting the game."""
        font = pygame.font.SysFont('arial', 32)
        
        # Make "Press SPACE to start" blink
        if self.alpha > 128:
            text = "Press SPACE to start"
            color = (255, 255, 255)
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height * 2 // 3 + 50))
            surface.blit(text_surface, text_rect)
        
        # Controls info
        controls_font = pygame.font.SysFont('arial', 20)
        controls_text = "Controls: Mouse to aim and shoot | R to reset"
        controls_surface = controls_font.render(controls_text, True, (200, 200, 200))
        controls_rect = controls_surface.get_rect(center=(self.width // 2, self.height * 2 // 3 + 100))
        surface.blit(controls_surface, controls_rect)
    
    def update_animation(self):
        """Update the fade in/out animation."""
        self.alpha += self.alpha_speed * self.alpha_direction
        
        # Reverse direction at boundaries
        if self.alpha >= 255:
            self.alpha = 255
            self.alpha_direction = -1
        elif self.alpha <= 0:
            self.alpha = 0
            self.alpha_direction = 1
    
    def draw(self, surface):
        """Draw the complete start screen."""
        self.draw_background(surface)
        self.draw_title(surface)
        self.draw_instructions(surface)
    
    def handle_event(self, event):
        """Handle events for the start screen."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.start_pressed = True
                # Stop music when starting
                try:
                    pygame.mixer.music.fadeout(1000)  # Fade out over 1 second
                except:
                    pass
                return True
        return False
    
    def is_start_pressed(self):
        """Check if the start button was pressed."""
        return self.start_pressed
