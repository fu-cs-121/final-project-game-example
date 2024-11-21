import pygame
import sys
import math
from core import SnakeGame
from pygame import gfxdraw
import random

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
DARK_GREEN = (34, 139, 34)
BLUE = (50, 50, 255)
GRAY = (128, 128, 128)

# Game settings
CELL_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE + 60  # Extra space for score
FPS = 60  # Higher FPS for smoother animations
MOVE_DELAY = 100  # Milliseconds between snake movements
PARTICLE_LIFETIME = 30  # Frames

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        return self.lifetime > 0

    def draw(self, screen):
        alpha = int((self.lifetime / PARTICLE_LIFETIME) * 255)
        color = (*self.color, alpha)
        gfxdraw.filled_circle(screen, int(self.x), int(self.y), 2, color)

class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []
        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 74)
        self.last_move_time = 0
        self.food_animation = 0
        self.screen_shake = 0
        
        # Create gradient background surface
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            color = (
                max(0, min(255, 20 + (y * 30 // SCREEN_HEIGHT))),
                max(0, min(255, 40 + (y * 20 // SCREEN_HEIGHT))),
                max(0, min(255, 20 + (y * 40 // SCREEN_HEIGHT)))
            )
            pygame.draw.line(self.background, color, (0, y), (SCREEN_WIDTH, y))

    def add_particles(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def draw_rounded_rect(self, surface, color, rect, radius):
        """Draw a rectangle with rounded corners"""
        pygame.draw.rect(surface, color, rect.inflate(-radius * 2, 0))
        pygame.draw.rect(surface, color, rect.inflate(0, -radius * 2))
        
        # Draw the corners
        for corner in [(rect.topleft, rect.topright),
                      (rect.bottomleft, rect.bottomright)]:
            for point in corner:
                pygame.draw.circle(surface, color, point, radius)

    def draw_snake_segment(self, x, y, prev_segment=None, next_segment=None):
        """Draw a snake segment with smooth corners"""
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE - 2, CELL_SIZE - 2)
        self.draw_rounded_rect(self.screen, GREEN, rect, CELL_SIZE // 4)

        # Add gradient effect
        highlight = pygame.Surface((CELL_SIZE - 2, CELL_SIZE - 2), pygame.SRCALPHA)
        pygame.draw.ellipse(highlight, (255, 255, 255, 64), 
                          (0, 0, CELL_SIZE - 2, (CELL_SIZE - 2) // 2))
        self.screen.blit(highlight, (x * CELL_SIZE, y * CELL_SIZE))

    def draw_food(self, x, y):
        """Draw food with pulsing animation"""
        self.food_animation = (self.food_animation + 0.1) % (2 * math.pi)
        size_multiplier = 1 + math.sin(self.food_animation) * 0.2
        
        center_x = x * CELL_SIZE + CELL_SIZE // 2
        center_y = y * CELL_SIZE + CELL_SIZE // 2
        radius = int((CELL_SIZE // 2 - 2) * size_multiplier)
        
        # Draw main circle
        pygame.draw.circle(self.screen, RED, (center_x, center_y), radius)
        
        # Draw highlight
        highlight_pos = (center_x - radius // 3, center_y - radius // 3)
        pygame.draw.circle(self.screen, (255, 255, 255, 128), highlight_pos, radius // 3)

    def draw_game(self, game_state):
        """Draw the current game state"""
        # Apply screen shake
        shake_offset_x = random.randint(-self.screen_shake, self.screen_shake)
        shake_offset_y = random.randint(-self.screen_shake, self.screen_shake)
        self.screen_shake = max(0, self.screen_shake - 1)

        # Draw background
        self.screen.blit(self.background, (shake_offset_x, shake_offset_y))
        
        # Update and draw particles
        self.particles = [p for p in self.particles if p.update()]
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw snake
        for segment in game_state['snake']:
            self.draw_snake_segment(*segment)
        
        # Draw food
        self.draw_food(*game_state['food'])
        
        # Draw score
        score_text = self.font.render(f'Score: {game_state["score"]}', True, WHITE)
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        
        # Draw game over message
        if game_state['game_over']:
            self.draw_game_over()
        
        pygame.display.flip()

    def draw_game_over(self):
        """Draw game over screen with animation"""
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # Draw "Game Over" text with shadow
        game_over_text = self.title_font.render('Game Over!', True, WHITE)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 40))
        
        # Draw shadow
        shadow_text = self.title_font.render('Game Over!', True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH/2 + 2, SCREEN_HEIGHT/2 - 38))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(game_over_text, text_rect)
        
        # Draw "Press R to Restart" with pulsing animation
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
        restart_color = (255, 255, 255, int(128 + 127 * pulse))
        restart_text = self.font.render('Press R to Restart', True, restart_color)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40))
        self.screen.blit(restart_text, restart_rect)

    def draw_start_menu(self):
        """Draw the start menu"""
        self.screen.blit(self.background, (0, 0))
        
        # Draw title
        title_text = self.title_font.render('SNAKE', True, GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        
        # Draw shadow
        shadow_text = self.title_font.render('SNAKE', True, DARK_GREEN)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH/2 + 2, SCREEN_HEIGHT/3 + 2))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Draw "Press SPACE to Start" with pulsing animation
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
        start_color = (255, 255, 255, int(128 + 127 * pulse))
        start_text = self.font.render('Press SPACE to Start', True, start_color)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 2/3))
        self.screen.blit(start_text, start_rect)
        
        # Draw controls help
        controls_text = self.font.render('Use Arrow Keys or WASD to move', True, GRAY)
        controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 3/4))
        self.screen.blit(controls_text, controls_rect)
        
        pygame.display.flip()

def main():
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Enhanced Snake Game")
    clock = pygame.time.Clock()
    
    # Create game instance and renderer
    game = SnakeGame(width=GRID_WIDTH, height=GRID_HEIGHT)
    renderer = GameRenderer(screen)
    
    # Direction mappings: keyboard to (x, y) direction
    direction_map = {
        pygame.K_UP: (0, -1),
        pygame.K_DOWN: (0, 1),
        pygame.K_LEFT: (-1, 0),
        pygame.K_RIGHT: (1, 0),
        pygame.K_w: (0, -1),
        pygame.K_s: (0, 1),
        pygame.K_a: (-1, 0),
        pygame.K_d: (1, 0)
    }
    
    # Game states
    in_start_menu = True
    running = True
    last_move_time = 0
    last_score = 0
    
    # Game loop
    while running:
        current_time = pygame.time.get_ticks()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if in_start_menu and event.key == pygame.K_SPACE:
                    in_start_menu = False
                elif event.key in direction_map:
                    game.change_direction(direction_map[event.key])
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()
                    last_score = 0
        
        if in_start_menu:
            renderer.draw_start_menu()
            continue
        
        # Update game state
        if not game.game_over and current_time - last_move_time >= MOVE_DELAY:
            game.move()
            last_move_time = current_time
            
            # Check if score increased (food collected)
            game_state = game.get_state()
            if game_state['score'] > last_score:
                food_x, food_y = game_state['food']
                renderer.add_particles(
                    food_x * CELL_SIZE + CELL_SIZE // 2,
                    food_y * CELL_SIZE + CELL_SIZE // 2,
                    RED
                )
                renderer.screen_shake = 5
                last_score = game_state['score']
        
        # Draw current state
        renderer.draw_game(game.get_state())
        
        # Control game speed
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()