# core.py
import random

class SnakeGame:
    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        self.reset()
        
    def reset(self):
        """Reset the game to initial state"""
        # Start snake in middle of board
        start_x = self.width // 2
        start_y = self.height // 2
        self.snake = [(start_x, start_y)]
        
        # Direction is stored as (x, y) coordinates
        # right = (1, 0), left = (-1, 0), up = (0, -1), down = (0, 1)
        self.direction = (1, 0)  # start moving right
        
        self.score = 0
        self.food = self.place_food()
        self.game_over = False
        
    def place_food(self):
        """Place food in a random empty cell"""
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def change_direction(self, new_direction):
        """Change snake direction if valid"""
        # Dictionary of opposite directions
        opposites = {
            (1, 0): (-1, 0),   # right vs left
            (-1, 0): (1, 0),   # left vs right
            (0, 1): (0, -1),   # down vs up
            (0, -1): (0, 1)    # up vs down
        }
        
        # Can't reverse direction
        if opposites[new_direction] != self.direction:
            self.direction = new_direction
            return True
        return False
        
    def move(self):
        """Move the snake one step in current direction"""
        if self.game_over:
            return False
            
        # Calculate new head position
        dx, dy = self.direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)
        
        # Check for wall collision
        x, y = new_head
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            self.game_over = True
            return False
            
        # Check for snake collision (excluding tail)
        if new_head in self.snake[:-1]:
            self.game_over = True
            return False
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food was eaten
        if new_head == self.food:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()  # Remove tail if no food eaten
            
        return True
        
    def get_state(self):
        """Get current game state"""
        return {
            'snake': self.snake,
            'food': self.food,
            'score': self.score,
            'game_over': self.game_over,
            'board_size': (self.width, self.height)
        }