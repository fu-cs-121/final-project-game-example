# test.py
from core import SnakeGame

def test_initial_state():
    game = SnakeGame(width=20, height=20)
    state = game.get_state()
    
    # Check initial snake position (should be in middle)
    assert len(state['snake']) == 1, "Initial snake length should be 1"
    assert state['snake'][0] == (10, 10), "Snake should start in middle"
    
    # Check initial direction
    assert game.direction == (1, 0), "Initial direction should be right"
    
    # Check initial score
    assert state['score'] == 0, "Initial score should be 0"
    
    # Check game state
    assert not state['game_over'], "Game should start as not game over"
    print("✓ Initial state test passed")

def test_movement():
    game = SnakeGame(width=20, height=20)
    initial_head = game.snake[0]
    
    # Move right (initial direction)
    game.move()
    assert game.snake[0] == (initial_head[0] + 1, initial_head[1]), "Snake should move right"
    
    # Change direction to down and move
    game.change_direction((0, 1))  # down
    game.move()
    assert game.snake[0] == (initial_head[0] + 1, initial_head[1] + 1), "Snake should move down"
    print("✓ Movement test passed")

def test_invalid_direction_change():
    game = SnakeGame()
    
    # Try to move in opposite direction (left while going right)
    result = game.change_direction((-1, 0))
    assert not result, "Should not be able to move in opposite direction"
    assert game.direction == (1, 0), "Direction should not change"
    print("✓ Invalid direction change test passed")

def test_wall_collision():
    game = SnakeGame(width=5, height=5)
    
    # Move snake to wall (start at 2,2, moving right until hit wall)
    for _ in range(4):
        game.move()
    
    # One more move should cause collision
    assert game.move() == False, "Snake should collide with wall"
    assert game.game_over == True, "Game should be over after wall collision"
    print("✓ Wall collision test passed")

def test_snake_growth():
    game = SnakeGame()
    initial_length = len(game.snake)
    
    # Place food right in front of snake
    game.food = (game.snake[0][0] + 1, game.snake[0][1])
    
    # Move to food
    game.move()
    assert len(game.snake) == initial_length + 1, "Snake should grow after eating food"
    assert game.score == 1, "Score should increase after eating food"
    print("✓ Snake growth test passed")

def test_self_collision():
    game = SnakeGame()
    
    # Grow snake to length 5
    for _ in range(4):
        game.food = (game.snake[0][0] + 1, game.snake[0][1])
        game.move()  # Eat food and grow
    
    # Now attempt to collide with itself
    game.change_direction((0, 1))   # down
    game.move()
    game.change_direction((-1, 0))  # left
    game.move()
    game.change_direction((0, -1))  # up
    game.move()
    
    assert game.game_over == True, "Game should be over after self collision"
    print("✓ Self collision test passed")

def test_reset():
    game = SnakeGame()
    
    # Play game a bit
    game.move()
    game.move()
    game.score = 5
    
    # Reset game
    game.reset()
    state = game.get_state()
    
    assert len(state['snake']) == 1, "Snake length should reset to 1"
    assert state['score'] == 0, "Score should reset to 0"
    assert not state['game_over'], "Game should not be game over after reset"
    print("✓ Reset test passed")

if __name__ == "__main__":
    print("Running Snake Game tests...\n")
    
    try:
        test_initial_state()
        test_movement()
        test_invalid_direction_change()
        test_wall_collision()
        test_snake_growth()
        test_self_collision()
        test_reset()
        
        print("\nAll tests passed successfully! ✨")
    except AssertionError as e:
        print(f"\n❌ Test failed: {str(e)}")