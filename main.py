"""Main module for the basket ball game application."""
import pygame
from core.screen import Screen
from game.ball import BasketBall
from game.hoop import BasketHoop
from game.score_board import ScoreBoard


def main():
    """Main function to run the basket ball game application."""
    screen = Screen()
    canvas = screen.canvas
    clock = pygame.time.Clock()

    # Initialize game objects
    ball = BasketBall(100, 500)
    hoop = BasketHoop(650, 200)
    score_board = ScoreBoard()
    
    # Game state variables
    scored = False
    game_over = False
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle mouse events for slingshot
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    ball.start_drag(mouse_x, mouse_y)
            
            elif event.type == pygame.MOUSEMOTION and not game_over:
                if ball.is_dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    ball.update_drag(mouse_x, mouse_y)
            
            elif event.type == pygame.MOUSEBUTTONUP and not game_over:
                if event.button == 1 and ball.is_dragging:
                    ball.release_drag()
                    scored = False
            
            # Reset game with R key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    ball.reset()
                    score_board.set_score(0)
                    score_board.lives = 5
                    scored = False
                    game_over = False

        # Update ball physics
        if ball.is_shot:
            ball.update(gravity=0.5)
            
            # Check if ball scored
            if not scored and hoop.check_score(ball):
                score_board.add_points(1)
                scored = True
                ball.reset()
            
            # Check if ball is out of bounds
            elif ball.is_out_of_bounds(800, 600):
                if not scored:
                    score_board.lose_life()
                    if score_board.is_game_over():
                        game_over = True
                ball.reset()
                scored = False

        # Draw everything
        screen.clear()
        hoop.draw(canvas)
        ball.draw(canvas)
        score_board.draw(canvas)
        
        # Draw slingshot line and info when dragging
        if ball.is_dragging:
            import math
            
            # Calculate distance and angle
            dx = ball.initial_x - ball.xc
            dy = ball.initial_y - ball.yc
            distance = math.sqrt(dx**2 + dy**2)
            angle_rad = math.atan2(-dy, dx)
            angle_deg = math.degrees(angle_rad)
            
            # Draw main line (thicker)
            pygame.draw.line(canvas, (255, 255, 255), 
                           (ball.initial_x, ball.initial_y), 
                           (ball.xc, ball.yc), 4)
            
            # Draw arrow head
            if distance > 5:
                arrow_length = 15
                arrow_angle = 25  # degrees
                
                # Calculate arrow head points
                angle1 = angle_rad + math.radians(180 - arrow_angle)
                angle2 = angle_rad + math.radians(180 + arrow_angle)
                
                point1_x = ball.xc + arrow_length * math.cos(angle1)
                point1_y = ball.yc - arrow_length * math.sin(angle1)
                point2_x = ball.xc + arrow_length * math.cos(angle2)
                point2_y = ball.yc - arrow_length * math.sin(angle2)
                
                # Draw arrow head
                pygame.draw.line(canvas, (255, 255, 255), (ball.xc, ball.yc), (int(point1_x), int(point1_y)), 4)
                pygame.draw.line(canvas, (255, 255, 255), (ball.xc, ball.yc), (int(point2_x), int(point2_y)), 4)
            
            # Draw projected trajectory (dotted line)
            vx = dx * 0.3
            vy = dy * 0.3
            gravity = 0.5
            sim_x, sim_y = ball.initial_x, ball.initial_y
            
            for i in range(0, 100, 5):
                sim_x += vx
                sim_y += vy
                vy += gravity
                
                if 0 <= sim_x < 800 and 0 <= sim_y < 600:
                    pygame.draw.circle(canvas, (100, 255, 100), (int(sim_x), int(sim_y)), 2)
                else:
                    break
            
            # Display drag info
            font = pygame.font.SysFont(None, 20)
            info_text = f"Distância: {distance:.1f}  Ângulo: {angle_deg:.1f}°"
            text_surface = font.render(info_text, True, (255, 255, 0))
            canvas.blit(text_surface, (ball.initial_x - 80, ball.initial_y - 40))
        
        # Display game over message
        if game_over:
            font = pygame.font.SysFont(None, 48)
            text = font.render("GAME OVER! Press R to restart", True, (255, 0, 0))
            text_rect = text.get_rect(center=(400, 300))
            canvas.blit(text, text_rect)
        
        screen.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
