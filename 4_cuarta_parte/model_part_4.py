#!/usr/bin/env python3

from pyscipopt import Model, quicksum
import Pattern
import sys
import time

########################################################################
    # d_t: capacidad del disco en TB,
    # F: nombres de los archivos,
    # s: tamaños de los archvios,
    # time_limit: threshold en segundos
########################################################################

def distribuir_archivos_4(d_t: int, F: list[str], s: list[int], time_limit=420):

    tiempo_inicio = time.time()
   
    # {tamaño: cantidad de archivos con ese tamaño}
    tamaños_cantidades = {size: s.count(size) for size in set(s)}
    # ordena el diccionario por tamaños, de mayor a menor
    tamaños_cantidades = dict(sorted(tamaños_cantidades.items(), reverse=True))

    # lista de los tamaños únicos de archivo de S
    tamaños_existentes = list(dict.fromkeys(tamaños_cantidades))
    t = len(tamaños_existentes) # Cantidad de tamaños diferentes de archivos

    c = Pattern.obtener_patrones(d_t * 10**6, tamaños_cantidades, 420)
    q = len(c) # Cantidad de patrones

    model = Model("model_part_4")
    time_limit = time_limit - (time.time() - tiempo_inicio)
    model.setParam("limits/time", time_limit)

    # x[p] entera: cantidad de veces que se usa el patrón p, con p ∈ {1,…,q}, donde x_{p} ≥ 0
    x = [model.addVar(vtype='I', name=f"x_{p}") for p in range(q)]

    # Minimizar la cantidad de patrones usados
    model.setObjective(quicksum(x), sense="minimize")

    # Hay que cubrir todos los archivos de cada tamaño
    for k in range(t):
        # con == tarda más que con >= Lo correcto CREO que es el ==, ya que el >= permite que haya más archivos de x tamaño de los que
        # en realidad tenemos. El >= se usa en el modelo auxiliar de la parte 5.
        model.addCons(quicksum(c[p][k] * x[p] for p in range(q)) == tamaños_cantidades[tamaños_existentes[k]])

    model.optimize()

    solution = model.getBestSol()
    status = model.getStatus()

    if solution is not None and status in ["optimal", "feasible"]:
        # sys.stderr.write(f"[Debugging] Solution: {solution}\n\n")
        tamaños_nombres = {tamaño: [] for tamaño in tamaños_existentes}
        for i in range(len(s)):
            tamaños_nombres[s[i]].append(F[i])
        return [F, model, x, s, c, tamaños_nombres]
    else:
        sys.stderr.write(f"[Debugging] Solution not found")
        return None
