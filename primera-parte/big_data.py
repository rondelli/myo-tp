from pyscipopt import Model
from generardor_output_1 import *

def distribuir_archivos(d_t, F, s):
    model = Model("big_data")
    d = d_t * 10**6

    # esto no es una constraint del modelo en sí
    if d < 0 or any(s_i < 0 for s_i in s):
        return

    n = len(F)

    # esto está medio de más...
    m = n   # No se puede tener más discos que archivos

    # y_{j} = 1 si se elige el disco j, 0 si no
    y = [model.addVar(f"y_{j}", vtype="BINARY") for j in range(m)]

    model.setObjective(sum(y), sense="minimize")

    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    x = {}
    for i in range(m):
        for j in range(m):
            x[i, j] = model.addVar(f"x_{i}_{j}", vtype="BINARY")

    # que los archivos se elijan solo para un disco
    for i in range(n):
        model.addCons(sum(x[i, j] for j in range(m)) == 1)

    # que no se pasen de capacidad los discos
    for j in range(m):
        model.addCons(sum(x[i, j] * s[i] for i in range(n)) <= d * y[j])

    # si el disco no tiene archivos, no puede haber sido elegido
    for j in range(m):
        model.addCons(sum(x[i, j] for i in range(n)) <= n * y[j])

    model.optimize()
    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus() == "feasible":
        generar_output("a_1.out", F, model, y, x, s)
    else:
        generar_output_fallido("a_1.out")
 