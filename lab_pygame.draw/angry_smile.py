import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

screen.fill(WHITE)

#face
circle(screen, YELLOW, (200, 175), 120)
circle(screen, BLACK, (200, 175), 120, 2)

#left eye
circle(screen, RED, (155, 155), 23)
circle(screen, BLACK, (155, 155), 23, 1)
circle(screen, BLACK, (155, 155), 10)

#left eyebrow
line(screen, BLACK, (80, 70), (180, 115), 20)

#right eye
circle(screen, RED, (250, 155), 17)
circle(screen, BLACK, (250, 155), 17, 1)
circle(screen, BLACK, (250, 155), 10)

#right eyebrow
line(screen, BLACK, (320, 70), (225, 115), 20)

#mouth
rect(screen, BLACK, (150, 240, 105, 20))


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()