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
BLUE = (0, 30, 209)

# Background Properties
bg = pygame.image.load("369_background_new.png").convert()
bg = pygame.transform.scale(bg, (WIDTH,HEIGHT))
bg_x1 = 0
bg_x2 = WIDTH
scroll_speed = 10

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 30

# Dinosaur properties
player_img1 = pygame.image.load('ref_running.png')
player_img1 = pygame.transform.scale(player_img1, (100, 100))
player_img2 = pygame.image.load('ref_running_again.png')
player_img2 = pygame.transform.scale(player_img2, (100,100))
ground_y = HEIGHT - 30
jump_power = -20
gravity = 1.0

class Dinosaur:
    def __init__(self):
        self.sprites = [player_img1, player_img2]
        self.x = 50
        self.velocity = 0
        self.is_jumping = False
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.y = ground_y - self.image.get_height()
        self.counter = 0
        self.animation_speed = 10

    def jump(self):
        if not self.is_jumping:
            self.velocity = jump_power
            self.is_jumping = True

    def fall(self):
        if self.is_jumping:
            self.velocity = - jump_power
            self.is_jumping = False

    def move(self):
        self.velocity += gravity
        self.y += self.velocity
        if self.y >= ground_y - self.image.get_height():
            self.y = ground_y - self.image.get_height()
            self.is_jumping = False

    def draw(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0  # Reset counter
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
        screen.blit(self.image, (self.x, self.y))

# Obstacle properties
obstacle_speed = 10
obstacle_imgs = []
obstacle_img1 = pygame.image.load('pylon_cropped_40height.png')
obstacle_img1 = pygame.transform.scale(obstacle_img1, (40,80))
obstacle_imgs.append(obstacle_img1)
obstacle_img2 = pygame.image.load('waterbottle_cropped_50pixelwidth.png')
obstacle_img2 = pygame.transform.scale(obstacle_img2, (40,50))
obstacle_img2 = pygame.transform.rotate(obstacle_img2, 130)
obstacle_imgs.append(obstacle_img2)

class Obstacle:
    def __init__(self,obstacle_img):
        self.image = obstacle_img
        self.x = WIDTH
        self.y = ground_y - self.image.get_height()
        self.speed = obstacle_speed
        self.reset = False

    def move(self):
        self.x -= self.speed

    def set_x(self):
        self.x = WIDTH + random.randint(50, 100)  # Randomize obstacle spacing

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def set_height(self, height):
        self.y = height



def draw_score(score):
    text = font.render(f"Score: {score}", True, BLUE)
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


# Object creation for player and obstacles
dinosaur = Dinosaur()
obstacles = [Obstacle(i) for i in obstacle_imgs]
obstacles[1].set_height(random.randint(200,300))


# Score
score = 0
font = pygame.font.Font(None, 36)
running = True 
# Obstacle Speed settings
speed_update = True
max_speed = 30

def select_obstacle():
    current_obstacle = random.choice(obstacles)
    if current_obstacle == obstacles[1]:
        current_obstacle.set_height(random.randint(200,300))
    return current_obstacle

def reset_obstacle(obstacle):
    if obstacle.x < -obstacle.image.get_width():
        obstacle.set_x()
        obstacle = select_obstacle()
    return obstacle

current_obstacle = select_obstacle()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dinosaur jump mechanics
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        dinosaur.jump()
    dinosaur.move()

    # Obstacle movement
    current_obstacle.move()
    current_obstacle = reset_obstacle(current_obstacle)
    # Speed up obstacle as game progresses further (10% obstacle speed boost every 5 pts)
    if current_obstacle.speed < max_speed:
        for obstacle in obstacles:
            if speed_update and score % 200 == 0 and score != 0:
                obstacle.speed *= 1.1
        scroll_speed = current_obstacle.speed
        speed_update = False
        if score % 200 != 0:
            speed_update = True

    # Collision detection
    dino_rect = pygame.Rect(dinosaur.x, dinosaur.y, dinosaur.image.get_width(), dinosaur.image.get_height())
    for obstacle in obstacles:
        obs_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.image.get_width(), obstacle.image.get_height())
        if dino_rect.colliderect(obs_rect):
            print('Game Over!')
            running = False

    # Drawing everything
    draw_background()
    dinosaur.draw()
    current_obstacle.draw()
    score += 1
    draw_score(score)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
