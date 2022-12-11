import math
from random import choice
from random import randint as rnd

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600
FLOOR = 450    #координата пола

GRAVITY = 2
ATTENUATION = 0.3   #коэффициент затухания при ударе шарика о стенки

targets_number = 2

class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= GRAVITY

        if((self.x + self.r >= WIDTH) or (self.x - self.r <= 0)):
            self.vx = -self.vx
        elif(self.y + self.r <= 0):
            self.vy = -self.vy
        elif(self.y - self.r > FLOOR):
            self.y = FLOOR + self.r + 1
            self.vy = - self.vy * ATTENUATION
            self.vx = self.vx * ATTENUATION
            self.live -= 1
            if(self.live == 0):
                self.color = WHITE     # need to be fixed!!

        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """Отрисовка мяча"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj"""
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2 <= (self.r + obj.r)**2):
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """Отрисовка пушки"""
        len = 30 + self.f2_power
        gun_x, gun_y = 40, 450
        pygame.draw.line(
            self.screen,
            self.color,
            (gun_x, gun_y),
            (gun_x + len * math.cos(self.an), gun_y + len * math.sin(self.an)),
            10
        )

    def power_up(self):
        """Увеличение силы выстрела пушки"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self, screen, x = 700, y = 450, r = 20):
        self.points = 0
        self.live = 1
        self.screen = screen
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        self.r = r
        self.color = RED
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 400)
        self.v_x = rnd(-7, 7)
        self.v_y = rnd(-7, 7)
        if(self.v_x == 0):
            self.v_x = 5
        r = self.r = rnd(2, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def move(self):
        '''Движение цели'''
        if ((self.x + self.r >= WIDTH) or (self.x - self.r <= 0)):
            self.v_x = -self.v_x
        if (self.y + self.r <= 0):
            self.v_y = -self.v_y
        if (self.y - self.r >= FLOOR):
            self.y = FLOOR + self.r + 1
            self.v_y = -self.v_y
        self.x += self.v_x
        self.y += self.v_y

    def draw(self):
        """Отрисовка цели"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)

targets = []
for i in range(targets_number):
    targets.append(Target(screen))

finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for target in targets:
        target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        for target in targets:
            if b.hittest(target) and target.live:
                target.live = 0
                target.hit()
                target.new_target()
    gun.power_up()

    for target in targets:
        target.move()

pygame.quit()
