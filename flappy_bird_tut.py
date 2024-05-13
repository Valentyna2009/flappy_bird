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

# define font
font = pygame.font.SysFont("Bauhaus 93", 60)

# defimne the color
white = (255, 255, 255)

# position of ground and speed the image
ground_scroll = 0
ground_speed = 3
flying = False
game_over = False
pipe_gap = 165
# частота появления этих труб в милисекундах
pipe_frequency = 2000
last_pipe = pygame.time.get_ticks() - pipe_frequency
# счётчик очков и распознования, пролетела ли птичка колону, что бы засчитать бал
score = 0
pass_pipe = False 

bg = pygame.image.load('flappy_bird2/bg3.png')
ground = pygame.image.load('flappy_bird2/ground2.png')

def print_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


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
                flap_cooldown = 10
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
        if self.rect.right < 0:
            self.kill()

# обьединение обьектов в группы
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(int(SCREEN_WIDTH / 8), int(SCREEN_HEIGHT / 2))

bird_group.add(flappy)


running = True

while running:

    clock.tick(fps)
    # background
    screen.blit(bg, (0, 0))

    # draw a pipe on the screen
    pipe_group.draw(screen)
    # draw a bird on the screen
    bird_group.draw(screen)
    bird_group.update()

    # draw a pipe on the screen
    pipe_group.draw(screen)

    # draw and scroll the ground
    screen.blit(ground, (ground_scroll, SCREEN_HEIGHT - ground.get_height()))

    # check the score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
        and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
        and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                
    print_text(str(score), font, white, int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 16))

# если она ударяется об колону или вверх экрана, то это конец игры
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # check if bird touch the groud
    if flappy.rect.bottom >= SCREEN_HEIGHT - ground.get_height(): 
        game_over = True
        flying = False

    if game_over == False and flying == True:

        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height , 1)
            # add the pipe on the screen
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        pipe_group.update()

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