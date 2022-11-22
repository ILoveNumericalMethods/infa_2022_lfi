import pygame
from input import *
from objects import *


def modeling(objects, dt, screen):
    """
    Обрабатыает объекты
    """
    for index_of_first_object in range(len(objects)):
        for index_of_second_object in range(index_of_first_object + 1, len(objects)):
            
            objects[index_of_first_object].move(dt)
            objects[index_of_second_object].move(dt)

            objects[index_of_first_object].get_acceleration(objects[index_of_second_object])

            objects[index_of_first_object].print(screen)
            objects[index_of_second_object].print(screen)


def handle_events(events, screen, width, height, is_stop_button, is_save_button_pressed, x_cord_of_time_scale_point):
    
    finished = False

    for event in events:
        
        if event.type == pygame.QUIT:
            finished = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                click_position = event.pos
                
                if(click_position[2] >= height * 4 / 5):
                    
                    if (click_position[1] < width / 4):
                        is_stop_button = not is_stop_button
                    elif (click_position[1] >= width / 4 and click_position[1] < width / 2):
                        is_save_button_pressed = not is_save_button_pressed   
                    else:
                        x_cord_of_time_scale_point = click_position[1]
        
        draw_interface(screen, width, height, is_stop_button, is_save_button_pressed, x_cord_of_time_scale_point)
    
    return finished, is_stop_button, is_save_button_pressed, x_cord_of_time_scale_point

def main():
    """
    Главная функция главного модуля.
    """

    pygame.init()

    print("Файл с постоянными:")
    input_file = input()
    G, dt, T, width, height, output_file = read_constants_from_file(input_file)

    print("Файл с объектами:")
    input_file = input()
    objects = read_constants_from_file(input_file)

    screen = pygame.display.set_mode((width, height))
    
    finished = False
    is_stop_button = False
    is_save_button_pressed = False
    x_cord_of_time_scale_point = width / 2

    while not finished:
        
        finished, is_stop_button, is_save_button, x_cord_of_time_scale_point = handle_events(pygame.event.get(), screen, height, is_stop_button, is_save_button_pressed, x_cord_of_time_scale_point )

        if(not is_stop_button):
            modeling(objects, screen, dt)
        else:
            modeling(objects, screen, 0)

        if(is_save_button_pressed):
            write_space_objects_data_to_file(output_file, objects)
            is_save_button_pressed = not is_save_button_pressed

    print('Modelling finished!')

