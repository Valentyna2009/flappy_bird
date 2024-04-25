import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# position of ground and speed the image
ground_scroll = 0
ground_speed = 3


bg = pygame.image.load('bg3.png')
ground = pygame.image.load('ground2.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bird.png')
        self.DEFAULT_SIZE = (55, 60)
        self.image = pygame.transform.scale(self.image, self.DEFAULT_SIZE)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    #def update(self):

        # animation
        # self.counter += 1
        # flap_cooldown = 0
        # if self.counter > flap_cooldown:
        #     self.counter = 0
        #     flap_cooldown += 1
        # self.image = self.birds[self.index]


bird_group = pygame.sprite.Group()

flappy = Bird(int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT / 2))

bird_group.add(flappy)

running = True

while running:

    clock.tick(fps)
    # background
    screen.blit(bg, (0, 0))

    # draw a bird on the screen
    bird_group.draw(screen)

    # draw and scroll the ground
    screen.blit(ground, (ground_scroll, SCREEN_HEIGHT - ground.get_height()))
    ground_scroll -= ground_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
pygame.quit()