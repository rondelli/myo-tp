from pyscipopt import Model

def distribuir_archivos(capacidad_discos, nombres_archivos, tamaños_archivos):
    return "holaa"


model = Model("big_data")



'''
d_{j} = capacidad del disco j CONSTANTE (input) - k discos
a_{i} = capacidad del archivo i CONSTANTE (input) - n archivos
x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
y_{j} = 1 si se elige el disco j, 0 si no

minimize    y_1 + y_2 + ... + y_n

s.t 
    1. que no se pasen de capacidad los discos

    x_{1, 1} * a_{1} + x_{2, 1} * a_{2} + ... + x_{n, 1} * a_{1} <= d_{1} * y_{1}
    x_{1, 2} * a_{1} + x_{2, 2} * a_{2} + ... + x_{n, 2} * a_{2} <= d_{2} * y_{2}
    x_{1, 3} * a_{1} + x_{2, 3} * a_{2} + ... + x_{n, 3} * a_{3} <= d_{3} * y_{3}
        (. . .)
    x_{1, j} * a_{1} + x_{2, j} * a_{2} + ... + x_{n, k} * a_{n} <= d_{k} * y_{k}

    2. que los archivos se elijan solo para un disco

    x_{1, 1} + x_{1, 2} + ... + x_{1, k} = 1
    x_{2, 1} + x_{2, 2} + ... + x_{2, k} = 1
    x_{3, 1} + x_{3, 2} + ... + x_{3, k} = 1
        (. . .)
    x_{n, 1} + x_{n, 2} + ... + x_{n, k} = 1

    3. generales

    x_{i, j}, y_{j} pert {0, 1}
    d_{j}, a_{i} >= 0

'''

# esto NO ES LO QUE QUEREMOS MODELAR, está para recordar sintaxis jeje ;)
x = model.addVar("x", vtype="INTEGER")
y = model.addVar("y", vtype="INTEGER")

model.setObjective(x + y, sense="maximize")

model.addCons(2 * x - y >= 0)
model.addCons(2 * x - y <= 100)

model.addCons(x <= 10)
model.addCons(x >= 0)

model.addCons(y <= 100)
model.addCons(y >= 0)

model.optimize()

sol = model.getBestSol()
print(f"x: {sol[x]}")
print(f"y: {sol[y]}")
