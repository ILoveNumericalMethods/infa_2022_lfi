import pygame
from pygame import circle

class Star:
    """
    Тип данных, описывающий звезду.
    type - объект
    x - x кооридината 
    y - y кооридината
    mass - масса
    radius - изображаемый радиус
    color - цвет объекта
    x_velocity - скорость по оси x
    y_velocity - скорость по оси y
    x_acceleration - усорение по оси x
    y_acceleration - усорение по оси y
    """

    def __init__ (self, radius, color, mass, x, y, x_velocity, y_velocity):
        """
        Конструктор
        """
        self.type = "star"
        self.mass = mass
        self.x = x
        self.y = y
        self.radius = radius 
        self.color = color
        self.x_velocity = x_velocity 
        self.y_velocity = y_velocity 
        self.x_acceleration = 0 
        self.y_acceleration = 0

    def move(self, dt):
        """
        Движение звезды и обнкление ее ускорения для дальнейшего расчета.
        dt - время движения
        """
        self.x = self.x_velocity * dt
        self.x = self.x_velocity * dt

        self.x_velocity = self.y_acceleration * dt
        self.y_velocity = self.y_acceleration * dt

        self.x_acceleration = 0
        self.y_acceleration = 0

    def get_acceleration(self, star, G):
        """
        Расчитывает взаимодействиемежу телами.
        star - взаимодей ствующий объект
        G - гравитационная постоянная Ньютона
        """
        distance = ((self.x - star.x) ** 2 +  (self.y - star.y) ** 2) ** 2
        module_force = G * self.mass * star.mass / distance ** 2
        x_force = module_force / distance * (star.x - self.x)
        y_force = module_force / distance * (star.y - self.y)

        self.x_acceleration, star.x_acceleration = x_force / self.mass, -1 * x_force / star.mass
        self.y_acceleration, star.y_acceleration = y_force / self.mass, -1 * y_force / star.mass

    def print (self, screen):
        """
        Рисует звезду
        """
        circle(screen, self.color, (self.x, self.y), self.radius)
  

class Planet (Star):
    """
    Тип данных, описывающий планету.
    Отличие от типа Star - поле type, в остальном идентичны
    """
    def __init__ (self, radius, color, mass, x, y, x_velocity, y_velocity):
        """
        Конструктор
        """
        self.type = "planet"
        self.mass = mass
        self.x = x
        self.y = y
        self.radius = radius 
        self.color = color
        self.x_velocity = x_velocity 
        self.y_velocity = y_velocity 
        self.x_acceleration = 0 
        self.y_acceleration = 0