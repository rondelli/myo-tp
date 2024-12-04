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
    model.setObjective(quicksum(x), sense="minimize")

    # Cantidad archivos de tamaño $k$ que entran en el disco $j$
    # Restricción A
    # for j in range(m):
    #     for k in range(t):
    #         model.addCons(quicksum(s[k] * c[p][k] * x[p] for p in range(q)) <= d * y[j])

    # Restricción B
    for k in range(t):
        model.addCons(quicksum(c[p][k] * x[p] for p in range(q)) >= S[s[k]]) # con == es infeasible, con >= se pasa del tamaño del disco

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)
    model.optimize()

    solution = model.getBestSol()
    status = model.getStatus()
    objective_value = model.getObjVal()

    sys.stderr.write(f"[Debugging] Solution: {solution}\n\n")
    sys.stderr.write(f"[Debugging] ObjVal: {objective_value}\n\n")

    if solution is not None and status in ["optimal", "feasible"]:
        return [F, model, y, x, [key * S[key] for key in S], ordenamiento, c]
    else:
        return None
