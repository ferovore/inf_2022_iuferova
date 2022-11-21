# image 11_1

import pygame
from pygame.draw import *
import math

pygame.init()

FPS = 30
scr_width, scr_height = 550, 750
screen = pygame.display.set_mode((scr_width, scr_height))

GRAY = (210, 210, 210)
BLACK = (0, 0, 0)
FISH = (150, 180, 170)
CORALL = (230, 127, 80)
WHITE = (255, 255, 255)
DARK_BROWN = (75, 60, 45)
BROWN = (94, 75, 56)
LIGHT_BROWN = (118, 94, 70)
SKIN = (202, 185, 166)
GRAY_BROWN = (235, 230, 225)

#фон
screen.fill(WHITE)
rect(screen, GRAY, (0, 0, scr_width, 350))

def needle(x=150, y=400, width=250):

    circle(screen, GRAY, (x, y), width/2, draw_top_left=True, draw_top_right=True)
    circle(screen, BLACK, (x, y), width/2, 2, draw_top_left=True, draw_top_right=True)

    delta_y = width/7
    for i in range(4):
        delta_x = (width**2 / 4 - i**2 * delta_y**2) ** 0.5
        line(screen, BLACK, (x - delta_x, y - i*delta_y), (x + delta_x, y - i*delta_y))

    delta = width / 5
    for i in range(2):
        for j in range(3 - i):
            line(screen, BLACK, (x + delta*j, y - 2*i*delta_y), (x + delta*j, y - (2*i + 1)*delta_y))
            line(screen, BLACK, (x - delta*j, y - 2*i*delta_y), (x - delta*j, y - (2*i + 1)*delta_y))
    for j in range(2):
        line(screen, BLACK, (x + (j + 0.5)*delta, y - delta_y), (x + (j + 0.5)*delta, y - 2*delta_y))
        line(screen, BLACK, (x - (j + 0.5)*delta, y - delta_y), (x - (j + 0.5)*delta, y - 2*delta_y))

def rotated_ellipse(surface, color, rect, angle, width=0):    #angle — в градусах!
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    surface.blit(rotated_surf, rotated_surf.get_rect(center = target_rect.center))

def cat(x=160, y=580, body_size=130): # x, y = координаты "центра кота"

    ellipse(screen, GRAY, (x - body_size/2, y - body_size/8, body_size, body_size/4))

    rotated_ellipse(screen, GRAY, (x - 0.85*body_size, y + body_size/20, body_size/2, body_size/12), 20)
    rotated_ellipse(screen, GRAY, (x - 0.7*body_size, y + body_size/8, body_size/2, body_size/12), 30)
    rotated_ellipse(screen, GRAY, (x + 0.35*body_size, y + body_size/10, 1.1*body_size/2, 1.1*body_size/12), -30)
    rotated_ellipse(screen, GRAY, (x + 0.2*body_size, y + body_size/6, 1.1*body_size/2, 1.1*body_size/12), -40)

    rotated_ellipse(screen, GRAY, (x + 0.28*body_size, y - 0.28*body_size, 0.75*body_size, body_size/7), 33)

    head_x = body_size/3
    head_y = body_size/4

    # дописать: рыба и зубы кота

    #head
    ellipse(screen, GRAY, (x - 0.5*body_size, y - 0.3*body_size, head_x, head_y))
    ellipse(screen, GRAY, (x - 0.5*body_size, y - 0.3*body_size, head_x, head_y))

    eye_x = body_size/3/5
    eye_y = body_size/4/5
    #left eye
    ellipse(screen, WHITE, (x - 0.5*body_size + 0.8*eye_x, y - 0.3*body_size + eye_y, eye_x, eye_y))
    ellipse(screen, BLACK, (x - 0.5*body_size + 0.8*1.5*eye_x, y - 0.3*body_size + 1.25*eye_y, 0.5*eye_x, 0.5*eye_x))
    #right eye
    ellipse(screen, WHITE, (x - 0.5*body_size + 0.7*3*eye_x, y - 0.3*body_size + 1.5*eye_y, eye_x, eye_y))
    ellipse(screen, BLACK, (x - 0.5*body_size + 0.72*3.5*eye_x, y - 0.3*body_size + 1.75*eye_y, 0.5*eye_x, 0.5*eye_x))
    #nose
    polygon(screen, BLACK, [(x - 0.5*body_size + 1.25*eye_x, y - 0.17*body_size), 
                            (x - 0.5*body_size + 1.4*eye_x, y - 0.17*body_size), 
                            (x - 0.5*body_size + 1.3*eye_x, y - 0.17*body_size + 0.4*eye_y)])
    #ears
    polygon(screen, GRAY, [(x - 0.5*body_size + 0.4*head_x, y - 0.3*body_size + 0.1*head_y),
                           (x - 0.5*body_size + 0.5*head_x, y - 0.3*body_size - 0.3*head_y),
                           (x - 0.5*body_size + 0.6*head_x, y - 0.3*body_size + 0.15*head_y)])
    polygon(screen, GRAY, [(x - 0.5*body_size + 0.7*head_x, y - 0.3*body_size + 0.18*head_y),
                           (x - 0.5*body_size + 0.9*head_x, y - 0.3*body_size + 0.3*head_y),
                           (x - 0.5*body_size + head_x, y - 0.3*body_size - 0.1*head_y)])


def man(x=350, y=400, width=170, reflect=False): # x, y = координаты центра
    unit_x = width / 10
    unit_y = 1.3 * width / 14
    x += 5 * unit_x
    y += 7 * unit_y
    
    orient = -1 if reflect else 1

    ellipse(screen, GRAY_BROWN, (x + unit_x * orient * (-1.8), y + unit_y * (-6.3), unit_x * orient * 6, unit_y * 4))

    #body
    ellipse(screen, BROWN, (x + unit_x * orient * (-2.7), y + unit_y * (-3.3), unit_x * orient * 7.3, unit_y * 16.2))
    rect(screen, WHITE, (x + unit_x * orient * (-2.7), y + unit_y * (-3.3 + 8.1), unit_x * orient * 7.3, unit_y * 8.1))

    #head
    ellipse(screen, LIGHT_BROWN, (x + unit_x * orient * (-1.1), y + unit_y * (-6), unit_x * orient * (4.5), unit_y * 3.4))
    ellipse(screen, SKIN, (x + unit_x * orient * (-0.5), y + unit_y * (-5.4), unit_x * orient * (3.5), unit_y * 2.4))

    #legs
    ellipse(screen, BROWN, (x + unit_x * orient * (-1.3), y + unit_y * (4.1), unit_x * orient * 1.5, unit_y * 2.8))
    ellipse(screen, BROWN, (x + unit_x * orient * (-2.3), y + unit_y * (5.9), unit_x * orient * 2.6, unit_y * 1))
    ellipse(screen, BROWN, (x + unit_x * orient * (1.8), y + unit_y * (4.1), unit_x * orient * 1.5, unit_y * 2.8))
    ellipse(screen, BROWN, (x + unit_x * orient * (2.4), y + unit_y * (5.95), unit_x * orient * 2.3, unit_y * 0.95))

    #arms
    ellipse(screen, BROWN, (x + unit_x * orient * (-4.2), y + unit_y * (-1.2), unit_x * orient * 3.9, unit_y * 1.4))
    rotated_ellipse(screen, BROWN, (x + unit_x * orient * (2.6), y + unit_y * (-0.3), unit_x * orient * 3.4, unit_y * 1.2), -50)  
    
    #body (rectangles)
    rect(screen, DARK_BROWN, (x + unit_x * orient * (0.2), y + unit_y * (-2.5), unit_x * orient * 1.4, unit_y * 6.3))
    rect(screen, DARK_BROWN, (x + unit_x * orient * (-2.7), y + unit_y * (4), unit_x * orient * 7.3, unit_y * 1))

    #face
    line(screen, BLACK, (x + unit_x * orient * (0.1), y + unit_y * (-4.8)), (x + unit_x * orient * (0.9), y + unit_y * (-4.5)))
    line(screen, BLACK, (x + unit_x * orient * (1.7), y + unit_y * (-4.5)), (x + unit_x * orient * (2.4), y + unit_y * (-4.9)))
    arc(screen, BLACK, (x + unit_x * orient * (-1), y + unit_y * (-3.8), unit_x * orient * (5.1), unit_y * 2.4), (0.5 - 1/7.5) * math.pi, (0.5 + 1/8) * math.pi)

    #stick
    line(screen, BLACK, (x + unit_x * orient * (-4), y + unit_y * (-6.8)), (x + unit_x * orient * (-3), y + unit_y * (6.8)))    

needle()
cat()
man()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()