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

# Background Properties
bg = pygame.image.load("369_background_new.png").convert()
bg = pygame.transform.scale(bg, (WIDTH,HEIGHT))
bg_x1 = 0
bg_x2 = WIDTH
scroll_speed = 5

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 30

# Dinosaur properties
# dino = pygame.image.load('dinosaur.png').convert()
dino_width, dino_height = 40, 50
dino_x, dino_y = 50, HEIGHT - dino_height - 20
dino_vel_y = 0
gravity = 1.0
is_jumping = False

# Obstacle properties
# obstacle = pygame.image.load('obstacle.png').convert()
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

def draw_background():
    global bg_x1, bg_x2

    # Move backgrounds to the left
    bg_x1 -= scroll_speed
    bg_x2 -= scroll_speed

    # Reset positions when they move out of view
    if bg_x1 <= -WIDTH:
        bg_x1 = WIDTH
    if bg_x2 <= -WIDTH:
        bg_x2 = WIDTH

    # Draw the backgrounds
    screen.blit(bg, (bg_x1, 0))
    screen.blit(bg, (bg_x2, 0))


# Main game loop
running = True 
speed = True
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

    # Speed up obstacle as game progresses further (10% obstacle speed boost every 5 pts)
    if speed and score % 5 == 0 and score != 0:
        obstacle_speed *= 1.1
        speed = False
    elif score %5 != 0:
        speed = True

    # Collision detection
    if (dino_x < obstacle_x + obstacle_width and
        dino_x + dino_width > obstacle_x and
        dino_y < obstacle_y + obstacle_height and
        dino_y + dino_height > obstacle_y):
        print("Game Over!")
        running = False

    # Drawing everything
    draw_background()
    draw_dinosaur(dino_x, dino_y)
    draw_obstacle(obstacle_x, obstacle_y)
    draw_score(score)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
