from objects import Star, Planet

def read_constants_from_file(input_filename):
    """Cчитывает постянныеданные.
    input_filename — имя входного файла
    Формат ввода: "G dt T width height output file"
                 <G> <dt> T <width> <height> <output_file>
    """

    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == 'G':
                continue
            
            constants = line.split()
            return constants[0], constants[1], constants[2], constants[3], constants[4], constants[5]


def read_objects_data_from_file(input_filename):
    """Cчитывает данные о космических объектах из файла, создаёт сами объекты.
    input_filename — имя входного файла
    Формат ввода: <type> <radius> <color> <mass> <x> <y> <x_velocity> <y_velocity>
    """

    objects = []
    with open(input_filename, 'r') as input_file:
        for line in input_file:
            if len(line.strip()) == 0 or line[0] == '#':
                continue

            object_type = line.split()[0].lower()
            if object_type == "star":
                parameters = line.split()
                star = Star(int(parameters[1]), parameters[2], float(parameters[3]), float(parameters[4]), float(parameters[7]), float(parameters[7]), float(parameters[7]))
                objects.append(star)
            elif object_type == "planet":
                planet = Planet(int(parameters[1]), parameters[2], float(parameters[3]), float(parameters[4]), float(parameters[7]), float(parameters[7]), float(parameters[7]))
                objects.append(planet)

    return objects

def write_space_objects_data_to_file(output_filename, objects):
    """Сохраняет данные о космических объектах в файл.
    Строки имеют следуюший формат:
    Star <радиус в пикселах> <цвет> <масса> <x> <y> <x_velocity> <y_velocity>
    Planet <радиус в пикселах> <цвет> <масса> <x> <y> <x_velocity> <y_velocity>
    """
    
    with open(output_filename, 'w') as out_file:
        for object in objects:
            print(out_file, object.type, object.radius, object.mass, object.x, object.y, object.x_velocity, object.y_velocity)
            
