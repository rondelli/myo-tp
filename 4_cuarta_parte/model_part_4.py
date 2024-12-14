#!/usr/bin/env python3

from pyscipopt import Model, quicksum
import Pattern
import sys
import time


# d_t : tamaño del disco en TB
# F : nombres de archivos
# file_sizes: tamaños de archivos
def distribuir_archivos_4(d_t: int, F: list[str], file_sizes: list[int], time_limit=420):

    tiempo_inicio = time.time()
    c = Pattern.Pattern(d_t * 10**6, list(set(file_sizes))).obtener_patrones()
    
    S = {size: file_sizes.count(size) for size in set(file_sizes)}
    S = dict(sorted(S.items(), reverse=True))

    # Cantidad de archivos
    n = len(F) #sum(S[key] for key in S)

    # Cantidad de tamaños de archivos
    s = list(dict.fromkeys(S))
    t = len(s)

    # Cantidad de discos, a lo sumo, un disco por archivo
    # m = n

    # Cantidad de patrones
    q = len(c)

    # Define model
    model = Model("model_part_4")
    # Configurar el límite de tiempo en el solver

    time_limit = time_limit - (time.time() - tiempo_inicio)
    model.setParam("limits/time", time_limit)

    # x[p] entera: cantidad de veces que se usa el patrón p, con p ∈ {1,…,q}, donde x_{p} ≥ 0
    x = [model.addVar(vtype='I', name=f"x_{p}") for p in range(q)]

    # minimize disks:
    model.setObjective(quicksum(x), sense="minimize")

    # Restricción B
    for k in range(t):
        model.addCons(quicksum(c[p][k] * x[p] for p in range(q)) >= S[s[k]]) # con == es infeasible, con >= se pasa del tamaño del disco

    model.optimize()

    solution = model.getBestSol()
    status = model.getStatus()
    
    sys.stderr.write(f"[Debugging] Solution: {solution}\n\n")

    if solution is not None and status in ["optimal", "feasible"]:
        ordenamiento = sorted(list(zip(file_sizes, F)), reverse=True)
        return [F, model, x, file_sizes, ordenamiento, c]
    else:
        return None
