import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# position of ground and speed the image
ground_scroll = 0
ground_speed = 4
flying = False
game_over = False

bg = pygame.image.load('bg3.png')
ground = pygame.image.load('ground2.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False


    def update(self):

        if flying == True:
            # apply gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < SCREEN_HEIGHT - ground.get_height():
                self.rect.y += int(self.vel)



        if game_over == False:

            # jump wegen Space Taste
            result = False
            for value in pygame.key.get_pressed():
                result = result or value
            if result == True and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if result == False:
                self.clicked = False

            # handle the animation
            flap_cooldown = 5
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
            if self.index >= len(self.images):
                self.index = 0

            # rotate the brid
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            # point the bird at the ground
            self.image = pygame.transform.rotate(self.images[self.index], -90)



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
    bird_group.update()

    # draw and scroll the ground
    screen.blit(ground, (ground_scroll, SCREEN_HEIGHT - ground.get_height()))
    ground_scroll -= ground_speed
    if abs(ground_scroll) > 35:
        ground_scroll = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()
pygame.quit()