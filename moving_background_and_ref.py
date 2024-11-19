import pygame, sys
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('ref_running.png'))
        self.sprites.append(pygame.image.load('ref_running_again.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        # self.sprites.append(pygame.Surface((50, 50)))
        # self.sprites[0].fill((255, 0, 0))  # Red block
        # self.sprites.append(pygame.Surface((50, 50)))
        # self.sprites[1].fill((0, 255, 0))  # Green block
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.animation_speed = 10  # Higher values = slower animation
        self.counter = 0
        
    def update(self):
        self.counter += 1
        if self.counter >= self.animation_speed:
            self.counter = 0  # Reset counter
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

        
     
pygame.init()
clock = pygame.time.Clock()

# background
FrameHeight = 325
FrameWidth = 550
screen = pygame.display.set_mode((FrameWidth, FrameHeight)) 
bg = pygame.image.load("369_background_new.png").convert() 

scroll = 0

tiles = math.ceil(FrameWidth / bg.get_width()) + 1

# character
moving_sprites = pygame.sprite.Group()
player = Player(100, 200)
moving_sprites.add(player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    i = 0
    while(i < tiles): 
        screen.blit(bg, (bg.get_width()*i 
                         + scroll, 0)) 
        i += 1
    # FRAME FOR SCROLLING 
    scroll -= 6
  
    # RESET THE SCROLL FRAME 
    if abs(scroll) > bg.get_width(): 
        scroll = 0
    # CLOSINF THE FRAME OF SCROLLING 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            quit() 
    moving_sprites.update()
    moving_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(30)
    pygame.display.update()
