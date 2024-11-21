import pygame
import sys
from core import SnakeGame

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game settings
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE
FPS = 8

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def draw_game(screen, game_state):
    """Draw the current game state"""
    # Clear screen
    screen.fill(BLACK)
    
    # Draw snake
    for segment in game_state['snake']:
        x, y = segment
        pygame.draw.rect(screen, GREEN, 
                        (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2))
    
    # Draw food
    food_x, food_y = game_state['food']
    pygame.draw.rect(screen, RED, 
                    (food_x * CELL_SIZE, food_y * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2))
    
    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {game_state["score"]}', True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw game over message
    if game_state['game_over']:
        font = pygame.font.Font(None, 48)
        game_over_text = font.render('Game Over! Press R to Restart', True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(game_over_text, text_rect)
    
    # Update display
    pygame.display.flip()

def main():
    # Create game instance
    game = SnakeGame(width=GRID_WIDTH, height=GRID_HEIGHT)
    
    # Direction mappings: keyboard to (x, y) direction
    direction_map = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0)
    }
    
    # Game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # Change direction based on arrow keys
                if event.key in direction_map:
                    game.change_direction(direction_map[event.key])
                
                # Restart game if 'R' is pressed
                if event.key == pygame.K_r and game.game_over:
                    game.reset()
        
        # Update game state
        if not game.game_over:
            game.move()
        
        # Draw current state
        draw_game(screen, game.get_state())
        
        # Control game speed
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()