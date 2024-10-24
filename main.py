import pygame
import random
import math
from direction import Direction
import time

# Snake Game
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
FPS_LIMIT = 10
FAST_SPEED = FPS_LIMIT * 2 # Game set to double speed when player holds space
BLOCK_SIZE = 20
PRIORITIZE_VERTICAL_MOVEMENT = True # To self.from moving left or right while holding Vertical direction

# Colors (R,G,B)
BLACK = (0,0,0)
GREEN = (64,128,64)
GREEN2 = (0, 200, 0)
RED = (255,0,0)
WHITE = (255,255,255)


class SnakeGame:
    
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game - Python")
        self.clock = pygame.time.Clock() # Needed to set the FPS limit

        self.reset()
        
        
    def reset(self):
        
        self.direction = Direction.RIGHT
        
        self.snake = [
            [self.width // 2, self.height // 2], # Head
            [self.width // 2 - BLOCK_SIZE, self.height // 2], # 
            [self.width // 2 - (BLOCK_SIZE * 2), self.height // 2] # Tail Position
        ]
        
        self.head = None # Different movement approach
        # self.prev_tail_pos = None
        self.score = 0
        self.food = None
        self.place_food()
        
    
    def place_food(self):
        x = SCREEN_WIDTH // BLOCK_SIZE - 1 # Max horizontal Factor to use to place apple
        y = SCREEN_HEIGHT // BLOCK_SIZE - 1 # Max Vertical Factor to use to place apple
        
        # Find a valid block to place the food
        while True:
            food_pos = pygame.Vector2(random.randint(1, x) * BLOCK_SIZE, random.randint(1, y) * BLOCK_SIZE)
            self.food = [food_pos.x, food_pos.y]
            if self.food not in self.snake[0]:
                break
        
    
    def move(self):
        
        current_direction = self.direction.value
        current_head_pos = self.snake[0] # Get the current head position
        # Create the next head position
        next_head_pos = [
            current_head_pos[0] + BLOCK_SIZE * current_direction[0],
            current_head_pos[1] + BLOCK_SIZE * current_direction[1]
        ]
        
        self.head = next_head_pos # We Store the next head position
        
    def change_direction(self, new_direction):
        
        opposite_direction = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if opposite_direction[new_direction] != self.direction:
            self.direction = new_direction
            
            
    def is_collsion(self):
        
        if (self.head[0] > self.width - BLOCK_SIZE or
            self.head[0] < 0 or 
            self.head[1] > self.height - BLOCK_SIZE or 
            self.head[1] < 0):
            
            return True
        
        # Check self.head collided with its body
        # skip the first element since head is self.0]
        if self.head in self.snake[1:]:
            return True
        
        return False
    
    
    def update(self):
        
        # Move self.by inserting the next head position in front of self.list
        self.snake.insert(0, self.head)
        
        # Check if the Snake head is colliding with an apple
        # if so, we don't need to append a new segment, since we already added the next
        # head position in the front
        if self.head == self.food:
            # Update the score
            self.score += 1
            # Move the food to a new spot
            self.place_food()
        # if the next head position did not collided with food,
        # then, we remove the last element since we added
        # an extra element in front
        else:
            self.snake.pop() # Remove the last element 
            
        
    def draw(self):
        
        self.screen.fill(BLACK) # Set screen color
        
        # Iterate through self.part
        # and draw a rectangle at the part's coordinate
        
        # Draw Snake Head with a 
        pygame.draw.rect(self.screen, GREEN2, pygame.Rect(self.snake[0][0], self.snake[0][1], BLOCK_SIZE-1, BLOCK_SIZE-1))
        
        for segment in self.snake[1:]:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE-1, BLOCK_SIZE-1))
            
        # Draw the Food
        pygame.draw.rect(self.screen, RED, pygame.Rect(self.food[0], self.food[1], BLOCK_SIZE -1, BLOCK_SIZE -1))

        # Draw the Score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (0,0))
        pygame.display.flip()
        
    
    def play_next_frame(self):
        
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()            
                
                return -1, self.score

        # Handle Movement input
        keys = pygame.key.get_pressed()
        if PRIORITIZE_VERTICAL_MOVEMENT:
            # Pressing left or right while holding vertical direction does nothing
            if keys[pygame.K_w]:
                self.change_direction(Direction.UP)
            elif keys[pygame.K_s]:
                self.change_direction(Direction.DOWN)
            elif keys[pygame.K_a]:
                self.change_direction(Direction.LEFT)
            elif keys[pygame.K_d]:
                self.change_direction(Direction.RIGHT)
                    
        else:
            # Pressing up or down while holding horizontal direction does nothing
            if keys[pygame.K_a]:
                self.change_direction(Direction.LEFT)
            elif keys[pygame.K_d]:
                self.change_direction(Direction.RIGHT)
            elif keys[pygame.K_w]:
                self.change_direction(Direction.UP)
            elif keys[pygame.K_s]:
                self.change_direction(Direction.DOWN)
                
                
        # Move snake
        self.move()
        
        # Check for collisions
        game_over = False
        if self.is_collsion():
            game_over =  True
            return game_over, self.score
        
        # Update snake and food
        self.update()
        
        # Draw
        self.draw()
        
        # Set FPS Speed
        if keys[pygame.K_SPACE]:
            self.clock.tick(FAST_SPEED)
        else:
            self.clock.tick(FPS_LIMIT)
        
        return game_over, self.score
        

def main():
    
    game = SnakeGame() # Create a game instance

    # Game Loop
    while True:
        
        # Run the next game frame
        game_over, score = game.play_next_frame()

        # Exited Screen
        if game_over == -1:
            running = False
            break

        # Check game state
        if game_over:
            print(f'Final Score: {score}')
            time.sleep(2)
            game.reset()


if __name__ == "__main__":
    main()