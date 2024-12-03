#!/usr/bin/env python3

from pyscipopt import Model, quicksum
from configuracion_4 import *
from generador_output_4 import *
import sys
import os
import random


# d_t : tamaño del disco en TB
# F : nombres de archivos, no se usa en realidad
# S : cantidades de tamaños de archivos
# c : matriz de los patrones
def distribuir_archivos_4(d_t: int, F: list[str], S: dict[int:int], c: list[list[int]], time_limit=420):
    # Tamaño del disco en MB
    d = int(d_t * 10**6)

    # Cantidad de archivos
    n = sum(S[key] for key in S)

    # Cantidad de tamaños de archivos
    s = list(dict.fromkeys(S))
    t = len(s)

    # Cantidad de discos, a lo sumo, un disco por archivo
    m = n

    # Cantidad de patrones
    q = len(c)

    # Define model
    model = Model("model_part_4")

    # x[p] entera: cantidad de veces que se usa el patrón p, con p ∈ {1,…,q}, donde x_{p} ≥ 0
    x = [model.addVar(vtype='I', name=f"x_{p}") for p in range(q)]

    # y[j] binary: 1 si se usa el disco $j$, 0 en caso contrario
    y = [model.addVar(vtype='B', name=f"y_{j}") for j in range(m)]

    # minimize disks:
    model.setObjective(quicksum(y), sense="minimize")

    # Cantidad archivos de tamaño $k$ que entran en el disco $j$
    for j in range(m):
        for k in range(t):
            model.addCons(quicksum(s[k] * c[p][k] * x[p] for p in range(q)) <= d * y[j])

    # Restricción loca
    for k in range(t):
        model.addCons(quicksum(c[p][k] * x[p] for p in range(q)) == S[s[k]])

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)

    model.optimize()

    solution = model.getBestSol()
    status = model.getStatus()
    objective_value = model.getObjVal()

    if solution is not None and status in ["optimal", "feasible"]:
        return [F, model, y, x, s]
    else:
        return None


# Main
# ----

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} input_file_name_to_generate")
    sys.exit(1)

input_file_name = sys.argv[1]
print(f"Input file name to generate: {input_file_name}\n")

generar_configuracion(input_file_name)

disk_size, file_names, file_sizes = leer_configuracion(f"./{input_file_name}")

#print(f"d: {disk_size}\nnames: {file_names}\nsizes: {file_sizes}")

#solution = distribuir_archivos_4(disk_size, file_names, file_sizes)

"""
# disk in MB
300 

# number of files to backup
4

# files: file_id, size (in MB)
chocolate 135
fan 108
tuerca 93
ensalada 42
"""

F = [ "chocolate", "fan", "tuerca", "ensalada"]
S = { 135: 1, 108: 1, 93: 1, 42: 1 }

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

solution = distribuir_archivos_4(0.0003, F, S, c, 420)

if solution is not None:
    generar_output(f"{input_file_name[:-3]}.out", solution)
else:
    generar_output_fallido(f"{input_file_name[:-3]}.out")
