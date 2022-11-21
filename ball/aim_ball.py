import pygame
from pygame.draw import circle
from pygame.draw import rect
from random import randint
pygame.init()
pygame.font.init()

FPS = 30

screen = pygame.display.set_mode((1200, 900))

font1 = pygame.font.SysFont('freesanbold.ttf', 50)
text1 = font1.render('score 0', True, (255, 255, 0))
textRect1 = text1.get_rect()
textRect1.center = (150, 50)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

class Ball:
    '''
    Класс шарика
    r - радиус
    x - координата по гризонтали
    y - координата по вертикали
    color - цвет
    x_velocity - скорость по гризантали
    y_velocity - скорость по вертикали
    '''
    def __init__(self):
        self.r = randint(20, 75)
        self.x = randint(100, 1100)
        self.y = randint(100, 900)
        self.color = COLORS[randint(0, 5)]
        self.x_velocity = randint(0, 100) / 100 * (score/100)
        self.y_velocity = randint(0, 100) / 100 * (score/100)

    def check_hit(self, click_x, click_y):
        '''
        Проверяет попадание
        click_x - x координата нажатия
        click_y - y координата нажатия
        '''
        if ((click_x - self.x) ** 2 + (click_y - self.y) ** 2 <= self.r ** 2):
            return 1

        return 0

    def print(self):
        ''' Рисует шарик'''
        circle(screen, self.color, (self.x, self.y), self.r)

    def move(self):
        '''Расчитывает новое положение шарика'''
        self.x += FPS * self.x_velocity
        self.y += FPS * self.y_velocity

        if self.x >= 1200 - self.r:
            self.x = 1200 - self.r
            self.x_velocity *= -1

        if self.y >= 900 - self.r:
            self.y = 900 - self.r
            self.y_velocity *= -1

        if self.y <= 0 + self.r:
            self.y = 0 + self.r
            self.y_velocity *= -1

        if self.x <= 0 + self.r:
            self.x = 0 + self.r
            self.x_velocity *= -1

def write_score(score):
    '''
    Рисует счет
    score - счет
    '''
    rect(screen, (0, 0, 0), (0, 0, 300, 300))

    print_score = "Score: " + str(score)
    text1 = font1.render(print_score , True, (255, 255, 0))
    textRect1 = text1.get_rect()
    textRect1.center = (150, 50)

    screen.blit(text1, textRect1)

    return 0

def all_balls_print(all_balls):
    '''
    Рисует все шарики массива
    all_balls - массив с шариками
    '''

    for i in all_balls:
        i.print()

    return 0

def all_balls_move(all_balls):
    '''
    Двигает все шарики массива
    all_balls - массив с шариками
    '''

    for i in all_balls:
        i.move()

    return all_balls

def all_balls_check(all_balls, score, click_x, click_y):
    '''
    Проверяет попадаание в любой шарик массива и изменяет счет
    all_balls - массив с шариками
    score - счет
    click_x - х координата нажатия
    click_y - y координта нажатия
    '''

    for i in all_balls:
        if (i.check_hit(click_x, click_y)):
            score += 1
            all_balls.remove(i)
            new_ball = Ball()
            all_balls.append(new_ball)

            randint(1,2)
            if randint(1,2) == 2:
                new_ball = Ball()
                all_balls.append(new_ball)

    return all_balls, score


pygame.display.update()
clock = pygame.time.Clock()
finished = False

score = 0

all_balls=[]
new_ball = Ball()
all_balls.append(new_ball)
all_balls_print(all_balls)

pygame.display.update()

while not finished:

    clock.tick(FPS)
    rect(screen, (0, 0, 0), (0, 0, 1200, 900))
    write_score(score)
    all_balls = all_balls_move(all_balls)
    all_balls_print(all_balls)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("1")
            if event.button == 1:
                print("2")
                all_balls, score = all_balls_check(all_balls, score, event.pos[0], event.pos[1])

            pygame.display.update()

pygame.quit()