from pyscipopt import Model

def distribuir_archivos(capacidad_discos, nombres_archivos, tamaños_archivos):
    model = Model("big_data")

    y_j = [0] * len(nombres_archivos)
    obj = []

    for i in range(len(y_j)):
        var = model.addVar(f"y_{i}", vtype="INTEGER")
        obj.append(var)

    model.setObjective(sum(obj), sense="minimize")
    print(obj)


'''
d = capacidad de los discos
f_{i} = capacidad del archivo i CONSTANTE (input) - n archivos
x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
y_{j} = 1 si se elige el disco j, 0 si no

minimize    y_1 + y_2 + ... + y_n

s.t 
    1. que no se pasen de capacidad los discos

    x_{1, 1} * f_{1} + x_{2, 1} * f_{2} + ... + x_{n, 1} * f_{1} <= d * y_{1}
    x_{1, 2} * f_{1} + x_{2, 2} * f_{2} + ... + x_{n, 2} * f_{2} <= d * y_{2}
    x_{1, 3} * f_{1} + x_{2, 3} * f_{2} + ... + x_{n, 3} * f_{3} <= d * y_{3}
        (. . .)
    x_{1, j} * f_{1} + x_{2, j} * f_{2} + ... + x_{n, k} * f_{n} <= d * y_{k}

    2. que los archivos se elijan solo para un disco

    x_{1, 1} + x_{1, 2} + ... + x_{1, k} = 1
    x_{2, 1} + x_{2, 2} + ... + x_{2, k} = 1
    x_{3, 1} + x_{3, 2} + ... + x_{3, k} = 1
        (. . .)
    x_{n, 1} + x_{n, 2} + ... + x_{n, k} = 1

    3. generales

    x_{i, j}, y_{j} pert {0, 1}
    d, f_{i} >= 0

'''

