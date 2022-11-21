import math
import random
from random import choice

import pygame
from pygame.draw import *


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
ORANGE = (255, 100, 0)
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1200
HEIGHT = 600
grav = 3

class Floor:
    def __init__(self, screen):
        """создает пол"""
        global HEIGHT
        self.screen = screen
        self.height = HEIGHT - 80

    def draw(self):
        """рисует пол"""
        pygame.draw.line(self.screen, BLACK, (0, self.height), (WIDTH, self.height), 1)


class Ball:
    def __init__(self, screen):
        """
        создает шарик.
        х,у - координаты центра шарика,
        vx, vy - скорости шарика по соответствующим осям
        """
        self.screen = screen
        self.x = 40
        self.y = 450
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 10

    def move(self):
        """
        движение шарика.
        реализована гравитация, отскок о пола и правой стены
        """
        global HEIGHT, balls

        self.x += self.vx
        self.y -= self.vy
        self.vy -= grav

        if self.y > -self.r + floor.height:
            self.vy = -self.vy * 0.5
            self.vx = self.vx * 0.6
            if self.y > -self.r + floor.height:
                self.y = -self.r + floor.height
            if self.vy < 5:
                self.vy = 0

        if self.x > WIDTH - self.r:
            self.vx = -self.vx

        if self.y == floor.height - self.r:
            self.live -= 1

        for b in balls:
            if self.live == 0:
                balls.remove(b)

    def draw(self):
        """рисует шарик"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """проверяет столкновение с круглой мишенью"""
        a = obj.x - self.x
        b = obj.y - self.y
        if ((b**2 + a**2) <= (self.r + obj.r)**2) :
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        """создает пушку. f2_power - сила выстрела, l - длина"""
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = BLACK
        self.x = 10
        self.y = 500
        self.l = 10

    def fire2_start(self):
        """обозначает начало выстрела"""
        self.f2_on = 1

    def fire2_end(self, event):
        """
        Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet, len, shoots
        bullet += 1

        self.an = math.atan2((event.pos[1]-self.y), (event.pos[0]-self.x))
        new_ball = Ball(self.screen)
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        new_ball.x = self.x
        new_ball.y = self.y
        self.f2_on = 0
        self.f2_power = 10
        balls.append(new_ball)

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        y = event.pos[1]
        x = event.pos[0]
        if x - 20 <= 0:
            x = 20.00000000000001
        self.an = math.atan((y-450) / (x-20))
        if self.f2_on:
            self.color = ORANGE
        else:
            self.color = BLACK

    def draw(self):
        """рисует пушку"""
        len = 20 + self.f2_power

        coss = math.cos(self.an)
        sinn = math.sin(self.an)

        if math.sin(self.an) >= 0:
            sinn = 0
            coss = 1

        line(screen, self.color, (self.x, self.y), (self.x + len * coss, self.y + len * sinn), 7)

    def power_up(self):
        """увеличивает силу выстрела"""
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = ORANGE
        else:
            self.color = BLACK


class Target:

    """Поступательно движущаяся круглая мишень. За попадание дается 1 очко"""

    def __init__(self, screen):

        self.screen = screen
        self.r = random.randint(10, 100)
        self.color = choice(GAME_COLORS)
        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = random.randint(self.r, HEIGHT - self.r)
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)
        self.live = 1
        self.points = 0

    def new_target(self):
        """инициализирует новую мишень"""

        self.r = random.randint(10, 100)
        self.color = choice(GAME_COLORS)
        self.x = random.randint(self.r, WIDTH - self.r)
        self.y = random.randint(self.r, HEIGHT - self.r)
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)
        self.live = 1
        self.points = 0

    def draw(self):
        """рисует мишень"""
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def hit(self):
        """Попадание шарика в цель (начисление очков)"""
        self.points += 1

    def move(self):
        """движение мишени с отражением от всех четырех стен"""
        self.x += self.vx
        self.y += self.vy

        if (self.x + self.r >= WIDTH) or (self.x - self.r <= 0):
            self.vx = -self.vx
        if (self.y - self.r <= 0) or (self.y + self.r >= floor.height):
            self.vy = -self.vy

        if self.y > -self.r + floor.height:
            self.y = -self.r + floor.height

class Spinner:

    """Вращающаяся мишень. За попадпние дается 3 очка"""

    def __init__ (self, screen):

        self.screen = screen
        self.R = random.randint(50,100)
        self.r = random.randint(10, 20)
        self.X = random.randint(self.R + self.r, WIDTH - (self.r + self.R))
        self.Y = random.randint(self.R + self.r, HEIGHT - (self.r + self.R))
        self.vx = random.randint(-10,10)
        self.vy = random.randint(-10, 10)

        self.alpha = random.random() * 2 * math.pi
        self.x = self.X + self.R * math.cos(self.alpha)
        self.y = self.Y + self.R * math.sin(self.alpha)
        self.v_spin = random.randint(-10, 10) * (math.pi / 180)

        self.color = choice(GAME_COLORS)
        self.live = 1
        self.points = 0

    def new_spinner(self):
        """инициализирует новую мишень"""
        self.screen = screen
        self.R = random.randint(50, 100)
        self.r = random.randint(10, 20)
        self.X = random.randint(self.R + self.r, WIDTH - (self.r + self.R))
        self.Y = random.randint(self.R + self.r, HEIGHT - (self.r + self.R))
        self.vx = random.randint(-10, 10)
        self.vy = random.randint(-10, 10)

        self.alpha = random.random() * 2 * math.pi
        self.x = self.X + self.R * math.cos(self.alpha)
        self.y = self.Y + self.R * math.sin(self.alpha)
        self.v_spin = random.randint(-10, 10) * (math.pi / 180)

        self.color = choice(GAME_COLORS)
        self.live = 1
        self.points = 0

    def draw(self):
        """рисует мишень"""
        circle(self.screen, BLACK, (self.X, self.Y), self.R, 4)
        circle(self.screen, self.color, (self.x, self.y), self.r)

    def move(self):
        """движение минени с отскоком от всех четырех стен"""
        self.X += self.vx
        self.Y += self.vy

        self.alpha += self.v_spin
        self.x = self.X + self.R * math.cos(self.alpha)
        self.y = self.Y + self.R * math.sin(self.alpha)

        if (self.X + self.R + self.r >= WIDTH) or (self.X - self.R - self.r <= 0):
            self.vx = -self.vx
        if (self.Y - self.R - self.r <= 0) or (self.Y + self.R + self.r>= floor.height):
            self.vy = -self.vy

        if self.Y > -self.R + floor.height:
            self.Y = -self.R + floor.height

    def hit(self):
        """Попадание шарика в цель (начисление очков)"""
        self.points += 3


class Text:

    def write_points(self):
        """пишет количество очков"""
        text_p = font.render('Oчки: ' + str(points), False, BLACK)
        screen.blit(text_p, (10, 10))


pygame.init()
pygame.font.init()
bullet = 0
balls = []
targets = []
spinners = []
targets_number = 4
spinners_number = 1
points = 0

font = pygame.font.SysFont(None, 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
gun = Gun(screen)
floor = Floor(screen)
text = Text()
spinner = Spinner(screen)
finished = False

for i in range(targets_number):
    target = Target(screen)
    targets.append(target)

for i in range(spinners_number):
    spinner = Spinner(screen)
    spinners.append(spinner)

while not finished:
    screen.fill(WHITE)
    floor.draw()
    gun.draw()
    text.write_points()

    for b in balls:
        b.draw()

    for t in targets:
        t.move()
        t.draw()

    for s in spinners:
        s.move()
        s.draw()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif (event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1):
            gun.fire2_start()
        elif (event.type == pygame.MOUSEBUTTONUP) and (event.button == 1):
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t) and t.live:
                t.live = 0
                t.hit()
                points += t.points
                t.new_target()
        for s in spinners:
            if b.hittest(s) and s.live:
                s.live = 0
                s.hit()
                points += s.points
                s.new_spinner()

    gun.power_up()

pygame.quit()