import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 850
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# position of ground and speed the image
ground_scroll = 0
ground_speed = 3
flying = False
game_over = False
pipe_gap = 160
# частота появления этих труб в милисекундах
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency

bg = pygame.image.load('flappy_bird2/bg3.png')
ground = pygame.image.load('flappy_bird2/ground2.png')

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"flappy_bird2/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False


    def update(self):

            if flying == True:
                # gravity
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


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("flappy_bird2/img/pipe1.png")
        self.rect = self.image.get_rect()
        # postion 1 is from the top and -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
           self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        self.rect.x -= ground_speed

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

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

    # draw a pipe on the screen
    pipe_group.draw(screen)
    pipe_group.update()

    # draw and scroll the ground
    screen.blit(ground, (ground_scroll, SCREEN_HEIGHT - ground.get_height()))


    # check if bird touch the groud
    if flappy.rect.bottom >= SCREEN_HEIGHT - ground.get_height():
        game_over = True
        flying = False

    if game_over == False and flying == True:

        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2), -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2), 1)
            # add the pipe on the screen
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

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