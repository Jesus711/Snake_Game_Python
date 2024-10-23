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
PRIORITIZE_VERTICAL_MOVEMENT = True # To allow holding Vertical Direction and press Horizontal

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Python")
clock = pygame.time.Clock() # Needed to set the FPS limit

class Snake:
    
    def __init__(self, start_pos, cell_size=20):
        
        self.body = [
            [start_pos.x, start_pos.y], # Headw
            [start_pos.x - cell_size, start_pos.y], # 
            [start_pos.x - cell_size * 2, start_pos.y] # Tail Position
        ]

        self.direction = Direction.RIGHT
        self.prev_tail_pos = None
        self.cell_size = cell_size
        self.is_alive = False
        
    
    def move(self):
    
        if self.is_alive:
            return
    
        current_direction = self.direction.value
        current_head_pos = self.body[0] # Get the current head position
        # Create the next head position
        next_head_pos = [
            current_head_pos[0] + self.cell_size * current_direction[0],
            current_head_pos[1] + self.cell_size * current_direction[1]
        ]
        
        # Store the last position the tail segment was located
        self.prev_tail_pos = self.body[-1]
        # Create the snake's body
        # head = next head pos
        # rest of the body = previous segment coordinates excluding the last element
        self.body = [next_head_pos] + self.body[:-1]
        
        
    def change_direction(self, new_direction):
        
        opposite_direction = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if opposite_direction[new_direction] != self.direction:
            self.direction = new_direction
        
        
    def draw_snake(self):
        
        for segment in self.body:
            pygame.draw.rect(screen, "green", pygame.Rect(segment[0], segment[1], self.cell_size - 1, self.cell_size - 1))
            
        return self.body[0]
        
        
    def grow(self):
        
        if self.prev_tail_pos:
            self.body.append(self.prev_tail_pos)
            
            
    def detect_wall_collision(self, screen_width, screen_height):
        
        head_pos = self.body[0]
        if head_pos[0] < -5 or head_pos[0] > screen_width + 5 or head_pos[1] < -5 or head_pos[1] > screen_height + 5:
            return True
        
        return False
    
    def detect_body_collision(self):
        
        return self.body[0] in self.body[1:]
    
    
    def detect_apple_collision(self, apple_pos):
        
        head_pos = self.body[0]
        head = pygame.Rect(head_pos[0], head_pos[1], self.cell_size, self.cell_size)
        
        return head.colliderect(apple_pos)
    
    
    
        

def main():
    
    cell_size = 20 # Sets the size of each block of the snake and Apple
    x = SCREEN_WIDTH // cell_size - 1 # Max horizontal Factor to use to place apple
    y = SCREEN_HEIGHT // cell_size - 1 # Max Vertical Factor to use to place apple
    
    FAST_SPEED = FPS_LIMIT * 2 # Game set to double speed when player holds space
    
    # Starting Position of player, Center of Screen
    player_pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    # Get random start for apple
    apple_pos = pygame.Vector2(random.randint(1, x) * cell_size, random.randint(1, y) * cell_size)
    
    snake = Snake(player_pos, cell_size)
    
    running = True # Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:            
                running = False

        keys = pygame.key.get_pressed()
        
        if PRIORITIZE_VERTICAL_MOVEMENT:
            # Pressing left or right while holding vertical direction does nothing
            if keys[pygame.K_w]:
                snake.change_direction(Direction.UP)
            elif keys[pygame.K_s]:
                snake.change_direction(Direction.DOWN)
            elif keys[pygame.K_a]:
                snake.change_direction(Direction.LEFT)
            elif keys[pygame.K_d]:
                snake.change_direction(Direction.RIGHT)
                    
        else:
            # Pressing up or down while holding horizontal direction does nothing
            if keys[pygame.K_a]:
                snake.change_direction(Direction.LEFT)
            elif keys[pygame.K_d]:
                snake.change_direction(Direction.RIGHT)
            elif keys[pygame.K_w]:
                snake.change_direction(Direction.UP)
            elif keys[pygame.K_s]:
                snake.change_direction(Direction.DOWN)

        
        snake.move()

        # Border Collision Detectiona
        if snake.detect_wall_collision(SCREEN_WIDTH, SCREEN_HEIGHT):
            running = False
            
        if snake.detect_body_collision():
            running = False
        
        # Draw an apple
        apple = pygame.draw.rect(screen, "red", pygame.Rect(apple_pos.x, apple_pos.y, cell_size - 1, cell_size - 1))
        # Draw the snake
        snake.draw_snake()
        
        if snake.detect_apple_collision(apple):
            snake.grow()
            apple_pos = pygame.Vector2(random.randint(1, x) * cell_size, random.randint(1, y) * cell_size)
            while True:
                if [apple_pos.x, apple_pos.y] in snake.body:
                    apple_pos = pygame.Vector2(random.randint(1, x) * cell_size, random.randint(1, y) * cell_size)
                else:
                    break
            
            apple.x = apple_pos.x
            apple.y = apple_pos.y
            

        

        pygame.display.flip() # Displays the work on the screen
        
        # Set FPS limit
        if keys[pygame.K_SPACE]:
            clock.tick(FAST_SPEED)
        else:
            clock.tick(FPS_LIMIT)
        screen.fill((0,0,0)) # Set the color of the screen

        
    pygame.quit()


if __name__ == "__main__":
    main()