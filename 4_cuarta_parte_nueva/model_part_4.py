#!/usr/bin/env python3

from pyscipopt import Model, quicksum
from configuracion_4 import *
from generador_output_4 import *
import sys
import os
import random


# d_t : tamaño del disco en TB
# F : nombres de archivos
# file_sizes: tamaños de archivos
# c : matriz de los patrones
def distribuir_archivos_4(d_t: int, F: list[str], file_sizes: list[int], c: list[list[int]], time_limit=420):
    # Tamaño del disco en MB
    d = d_t * 10**6

    ordenamiento = sorted(list(zip(file_sizes, F)), reverse=True)
    file_sizes, F = zip(*ordenamiento)
    F = list(F)

    S = {size: file_sizes.count(size) for size in set(file_sizes)}
    S = dict(sorted(S.items(), reverse=True))

    # Cantidad de archivos
    n = sum(S[key] for key in S)

    # Cantidad de tamaños de archivos
    s = list(dict.fromkeys(S))
    print("S:", S)
    print("s:", s)
    t = len(s)

    # Cantidad de discos, a lo sumo, un disco por archivo
    m = n

    # Cantidad de patrones
    q = len(c)

    # Define model
    model = Model("model_part_4")

    # x_{p} integer: cant de veces que se usa el patrón p
    x = []
    for p in range(q):
        x.append(model.addVar(name=f"x_{p}", vtype="INTEGER"))

    # Minimizar la suma de las variables x[p]
    model.setObjective(quicksum(x), sense="minimize")

    # Restricción B
    for k in range(t):
        model.addCons(quicksum(c[p][k] * x[p] for p in range(q)) == S[s[k]]) # con == es infeasible, con >= se pasa del tamaño del disco

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)

    model.optimize()

    solution = model.getBestSol()
    status = model.getStatus()
    
    if solution is not None and status in ["optimal", "feasible"]:
        objective_value = model.getObjVal()
        sys.stderr.write(f"[Debugging] ObjVal: {objective_value}\n\n")
        return [F, model, x, [key * S[key] for key in S]]
    else:
        return None


# Main
# ----

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} input_file_name_to_generate")
    sys.exit(1)

input_file_name = sys.argv[1]
print(f"Input file name to generate: {input_file_name}\n")

# generar_configuracion(input_file_name)

disk_size, file_names, file_sizes = leer_configuracion(f"{input_file_name}")

"""
# disk in TB
3

# number of files to backup
4

# files: file_id, size (in MB)
chocolate 1350000
fan 1080000
tuerca 930000
ensalada 420000
"""

disk_size = 3
file_names = [ "chocolate", "fan", "tuerca", "ensalada"]
file_sizes = [ 1350000, 1080000, 930000, 420000 ]

# Patrón Marcelo
c = [[2, 0, 0, 0], # DELETEME
     [1, 1, 0, 1],
     [1, 0, 1, 1],
     [1, 0, 0, 3],
     [0, 2, 0, 2],
     [0, 1, 2, 0],
     [0, 1, 1, 2],
     [0, 1, 0, 4],
     [0, 0, 3, 0],
     [0, 0, 2, 2],
     [0, 0, 1, 4],
     [0, 0, 0, 7]]

# Patrón Lucía
c = [[2, 0, 0, 0], [1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 2, 1], [0, 0, 1, 4], [0, 0, 0, 4]]

solution = distribuir_archivos_4(disk_size, file_names, file_sizes, c, 420)

if solution is not None:
    generar_output(f"{input_file_name[:-3]}.out", solution)
else:
    generar_output_fallido(f"{input_file_name[:-3]}.out")
