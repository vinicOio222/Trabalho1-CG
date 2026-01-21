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

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit event  
                running = False

        screen.clear()
        ball = BasketBall(100, 500)
        ball.draw(canvas)
        hoop = BasketHoop(650, 200)
        hoop.draw(canvas)
        score_board = ScoreBoard()
        score_board.draw(canvas)
        screen.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
    
