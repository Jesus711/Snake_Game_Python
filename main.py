import pygame
import random
import math

# Snake Game
pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1000
FPS_LIMIT = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Python")
clock = pygame.time.Clock() # Needed to set the FPS limit


def main():
    # Starting Position of player, Center of Screen
    player_pos = pygame.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    dt = 0 # Delta Time in seconds since the last frame, used for framerate
    direction = [1, 0] # x, y direction
    
    apple_placed = False
    apple_pos = pygame.Vector2(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT-100))
    pygame.draw.circle(screen, "blue", apple_pos, 20)
    
    
    running = True # Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill((255,255,255)) # Set the color of the screen
        
        
        # Draw a red circle at the center of the display with a radius of 20
        player_head = pygame.draw.circle(screen, "red", player_pos, 20)
        # Draw an apple
        apple = pygame.draw.circle(screen, "orange", apple_pos, 20)
        

        
        if direction[0] == 1 or direction[0] == -1:
            player_pos.x += math.floor(200 * dt * direction[0])
            
        elif direction[1] == 1 or direction[1] == -1:
            player_pos.y += math.floor(200 * dt * direction[1])
            
        # Border Collision Detection
        if player_pos.x <= 0 or player_pos.x >= SCREEN_WIDTH or player_pos.y <= 0 or player_pos.y >= SCREEN_HEIGHT:
            running = False
            
        if player_head.colliderect(apple):
            apple_pos = pygame.Vector2(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT-100))
            apple.x = apple_pos.x
            apple.y = apple_pos.y
            
        
        keys = pygame.key.get_pressed()
        #print(player_pos)
        
        # If vertical movement, prevent opposite direction
        if keys[pygame.K_w] or keys[pygame.K_s]:
            if direction[1] == 1 or direction[1] == -1:
                # do nothing
                # if use continue it causes a time skip
                pass
            elif keys[pygame.K_w]:
                direction[1] = -1
                direction[0] = 0
            elif keys[pygame.K_s]:
                direction[1] = 1
                direction[0] = 0

        # if horizontal movement, prevent opposite direction
        if keys[pygame.K_a] or keys[pygame.K_d]:
            if direction[0] == 1 or direction[0] == -1:
                # do nothing
                # if use continue it causes a time skip
                pass
            elif keys[pygame.K_a]:
                direction[1] = 0
                direction[0] = -1
            elif keys[pygame.K_d]:
                direction[1] = 0
                direction[0] = 1
        
        pygame.display.flip() # Displays the work on the screen
        
        # Set FPS limit
        dt = clock.tick(FPS_LIMIT) / 1000
        
    pygame.quit()


if __name__ == "__main__":
    main()