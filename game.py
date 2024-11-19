import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Google Dinosaur Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 30

# Dinosaur properties
dino_width, dino_height = 40, 50
dino_x, dino_y = 50, HEIGHT - dino_height - 20
dino_vel_y = 0
gravity = 1.0
is_jumping = False

# Obstacle properties
obstacle_width, obstacle_height = 20, 40
obstacle_x = WIDTH
obstacle_y = HEIGHT - obstacle_height - 20
obstacle_speed = 10

# Score
score = 0
font = pygame.font.Font(None, 36)

def draw_dinosaur(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, dino_width, dino_height))

def draw_obstacle(x, y):
    pygame.draw.rect(screen, GRAY, (x, y, obstacle_width, obstacle_height))

def draw_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dinosaur jump mechanics
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not is_jumping:
        dino_vel_y = -15
        is_jumping = True

    dino_y += dino_vel_y
    dino_vel_y += gravity
    if dino_y >= HEIGHT - dino_height - 20:
        dino_y = HEIGHT - dino_height - 20
        is_jumping = False

    # Obstacle movement
    obstacle_x -= obstacle_speed
    if obstacle_x < -obstacle_width:
        obstacle_x = WIDTH
        score += 1

    # Collision detection
    if (dino_x < obstacle_x + obstacle_width and
        dino_x + dino_width > obstacle_x and
        dino_y < obstacle_y + obstacle_height and
        dino_y + dino_height > obstacle_y):
        print("Game Over!")
        running = False

    # Drawing everything
    draw_dinosaur(dino_x, dino_y)
    draw_obstacle(obstacle_x, obstacle_y)
    draw_score(score)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
