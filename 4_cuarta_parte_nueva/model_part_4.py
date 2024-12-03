#!/usr/bin/env python3

from pyscipopt import Model, quicksum
from configuracion_4 import *
from generador_output_4 import *
import sys
import os
import random


def distribuir_archivos_4(d_t: int, F: list[str], S: list[int], time_limit=420):
    # Tamaño del disco en MB
    d = d_t * 10**6

    # Cantidad de archivos
    n = len(F)

    # Cantidad de tamaños de archivos
    S = list(dict.fromkeys(S))
    q = len(S)

    # Cantidad de discos, a lo sumo, un disco por archivo
    m = n

    # Define model
    model = Model("model_part_4")

    # c[k, j] integer: cantidad de archivos de tamaño $k$ que entran en el disco $j$
    c = {}
    for k in range(q):
        for j in range(m):
            c[k, j] = model.addVar(vtype='I', name=f"c_{k}_{j}")

    # y[j] binary: 1 si se usa el disco $j$, 0 en caso contrario
    y = [model.addVar(vtype='B', name=f"y_{j}") for j in range(m)]

    # minimize disks:
    model.setObjective(quicksum(y), sense="minimize")

    ########################################################################
    # FIXME: Esta restricción está de más?
    # No pueden haber discos usados con cero cantidad de archivos
    for j in range(m):
        model.addCons(quicksum(c[k, j] for k in range(q)) >= 1)
    ########################################################################

    # Cantidad archivos de tamaño $k$ que entran en el disco $j$
    for j in range(m):
        model.addCons(quicksum(s[k] * c[k, j] for k in range(q)) <= d * y[j])

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)

    model.optimize()

    sys.stderr.write(f"[Debugging] [MODELO 4] Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debugging] [MODELO 4] Cantidad sols: {model.getNSols()}\n\n")

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

print(f"d: {disk_size}\nnames: {file_names}\nsizes: {file_sizes}")

"""
solution = distribuir_archivos_4(disk_size, file_names, file_sizes)

if solution is not None:
    generar_output(f"{input_file_name[:-3]}.out", solution)
else:
    generar_output_fallido(f"{input_file_name[:-3]}.out")
"""
