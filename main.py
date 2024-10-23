import pygame
import random
import math
from direction import Direction
import time

# Snake Game
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
FPS_LIMIT = 60
SNAKE_SPEED = 0.075

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Python")
clock = pygame.time.Clock() # Needed to set the FPS limit

class Snake:
    
    def __init__(self, start_pos, cell_size=20):
        
        self.body = [
            [start_pos.x, start_pos.y], # Head
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
        
    # TODO: BUG found in movement: if player holds W or UP, player is allowed to move the opposite h direction
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
            pygame.draw.rect(screen, "red", pygame.Rect(segment[0], segment[1], self.cell_size - 1, self.cell_size - 1))
            
        return self.body[0]
        
        
    def increase_snake(self):
        
        if self.prev_tail_pos:
            self.body.append(self.prev_tail_pos)
            
            
    def detect_wall_collision(self, screen_width, screen_height):
        
        head_pos = self.body[0]
        if head_pos[0] <= 0 or head_pos[0] >= screen_width or head_pos[1] <= 0 or head_pos[1] >= screen_height:
            return True
        
        return False
    
    def detect_body_collision(self):
        
        pass
    
    
    def detect_apple_collision(self, apple_pos):
        
        head_pos = self.body[0]
        head = pygame.Rect(head_pos[0], head_pos[1], self.cell_size, self.cell_size)
        
        return head.colliderect(apple_pos)
    
    
    
        

def main():
    
    # Starting Position of player, Center of Screen
    player_pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    apple_pos = pygame.Vector2(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT-100))

    last_move_time = 0
    snake = Snake(player_pos, cell_size=20)
    
    running = True # Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        current_time = time.time()
        
        # Draw the snake
        snake.draw_snake()
        
        # Draw an apple
        apple = pygame.draw.circle(screen, "orange", apple_pos, 12)
        
        if current_time - last_move_time >= SNAKE_SPEED:
            snake.move()
            last_move_time = current_time
            
        # Border Collision Detectiona
        if snake.detect_wall_collision(SCREEN_WIDTH, SCREEN_HEIGHT):
            running = False
        
        
        if snake.detect_apple_collision(apple):
            snake.increase_snake()
            apple_pos = pygame.Vector2(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT-100))
            apple.x = apple_pos.x
            apple.y = apple_pos.y
            
            
        keys = pygame.key.get_pressed()
        #print(player_pos)
        if keys[pygame.K_w]:
            snake.change_direction(Direction.UP)
        
        if keys[pygame.K_s]:
            snake.change_direction(Direction.DOWN)

        if keys[pygame.K_a]:
            snake.change_direction(Direction.LEFT)
            
        if keys[pygame.K_d]:
            snake.change_direction(Direction.RIGHT)
        
        pygame.display.flip() # Displays the work on the screen
        
        # Set FPS limit
        clock.tick(FPS_LIMIT) / 1000
        screen.fill((255,255,255)) # Set the color of the screen

        
    pygame.quit()


if __name__ == "__main__":
    main()