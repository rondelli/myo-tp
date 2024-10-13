from pyscipopt import Model

def distribuir_archivos(capacidad_discos, nombres_archivos, tamaños_archivos):
    model = Model("big_data")
    d = capacidad_discos * 1000000
    f_i = tamaños_archivos

    # esto no es una constraint del modelo en sí
    if d < 0 or any(f < 0 for f in f_i):
        return

    cant_archivos = len(nombres_archivos)

    # y_{j} = 1 si se elige el disco j, 0 si no
    y_j = [model.addVar(f"y_{j}", vtype="BINARY") for j in range(cant_archivos)]

    model.setObjective(sum(y_j), sense="minimize")

    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    x_ij = {}
    for i in range(cant_archivos):
        for j in range(cant_archivos):  # No se puede tener más discos que archivos
            x_ij[i, j] = model.addVar(f"x_{i}_{j}", vtype="BINARY")

    # que los archivos se elijan solo para un disco
    for i in range(cant_archivos):
        model.addCons(sum(x_ij[i, j] for j in range(cant_archivos)) == 1)

    # que no se pasen de capacidad los discos
    for j in range(cant_archivos):
        model.addCons(sum(x_ij[i, j] * f_i[i] for i in range(cant_archivos)) <= d * y_j[j])

    model.optimize()
    sol = model.getBestSol()

    print()
    if sol is not None:
        cant_discos = sum(1 for j in range(cant_archivos) if model.getVal(y_j[j]) > 0.5)
        print(f"Para la configuración del archivo, {cant_discos} discos son suficientes.\n")

        for j in range(cant_discos):    # esto funciona porque los elige en orden ;)
            archivos_en_disco = []
            espacio_ocupado = 0

            for i in range(cant_archivos):
                if model.getVal(x_ij[i, j]) > 0.5: # se eligio el archivo
                    archivos_en_disco.append(f"{nombres_archivos[i]}  {f_i[i]}")
                    espacio_ocupado = espacio_ocupado + f_i[i]

            print(f"Disco {j+1}: {espacio_ocupado} MB")

            for archivo in archivos_en_disco:
                print(archivo)

            print() # jas que feo
    else:
        print("No se encontró una solución factible.")


'''
d = capacidad de los discos CONSTANTE
f_{i} = tamaño del archivo i CONSTANTE (input) - n archivos
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

