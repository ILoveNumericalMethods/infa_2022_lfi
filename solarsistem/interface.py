import pygame 
from pygame.draw import circle

button_stop = pygame.image.load('stop_button.png').convert_alpha()
button_start = pygame.image.load('sart_button.png').convert_alpha()
button_save_off = pygame.image.load('save_button_off.png').convert_alpha()
button_save_on = pygame.image.load('save_button_on.png').convert_alpha()
time_scale = pygame.image.load('time_scale.png').convert_alpha()

def draw_interface(screen, width, height, is_stop_button, is_save_button_pressed, x_cord_of_time_scale_point):
    """
    Функция рисует интерфейс программы
    """
    button_stop = pygame.transform.scale(button_stop, (width / 4, height / 5))
    button_start = pygame.transform.scale(button_start, (width / 4, height / 5))
    
    button_save_on = pygame.transform.scale(button_save_on, (width / 4, height / 5))
    button_save_off = pygame.transform.scale(button_save_off, (width / 4, height / 5))

    time_scale = pygame.transform.scale(time_scale, (width / 2, height / 5))

    screen.fill(0, 0, 0)
    
    if(is_stop_button):
        screen.blit(button_stop, (0, height * 4 / 5))
    else:
        screen.blit(button_start, (0, height * 4 / 5))

    if(is_save_button_pressed):
        screen.blit(button_save_on, (width / 4, height * 4 / 5))
    else:
        screen.blit(button_save_off, (width / 4, height * 4 / 5))

    screen.blit(time_scale, (width / 2, height * 4 / 5))
    circle(screen, (255, 255, 255), (x_cord_of_time_scale_point, height * 9 / 10), height / 20)
