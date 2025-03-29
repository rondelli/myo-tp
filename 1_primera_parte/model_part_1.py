import sys
from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING
from pyscipopt import *

########################################################################
    # d_t: capacidad del disco en TB,
    # F: nombres de los archivos,
    # s: tamaños de los archvios,
    # time_limit: threshold en segundos
########################################################################
def distribuir_archivos_1(d_t: int, F: list[str], s: list[int], time_limit=420):
    model, fake_y, fake_x = resolver_modelo_binario_1(d_t, F, s, time_limit)

    solution = model.getBestSol()
    status = model.getStatus()

    if solution is not None and status in ["optimal", "feasible"]:
        return [F, model, fake_y, fake_x, s]
    else:
        return None

def resolver_modelo_binario_1(d_t: int, F: list[str], s: list[int], time_limit=420):
    model = Model("model_part_1")
    model.setParam("limits/time", time_limit)

    d = d_t * 10**6

    n = len(F)
    m = n

    ########################################################################
    # BINARY
    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    #
    x = {}
    for i in range(n):
        for j in range(m):
            x[i, j] = model.addVar(name=f"x_{i}_{j}", vtype="BINARY")

    # y_{j} = 1 si se elige el disco j, 0 si no
    y = [model.addVar(f"y_{j}", vtype="BINARY") for j in range(m)]
    #
    ########################################################################

    # Minimizar la cantidad de discos
    model.setObjective(quicksum(y), sense="minimize")

    # Que los archivos se elijan solo para un disco
    for i in range(n):
        model.addCons(quicksum(x[i, j] for j in range(m)) == 1)

    # Que no se pasen de capacidad los discos
    for j in range(m):
        model.addCons(quicksum(x[i, j] * s[i] for i in range(n)) <= d * y[j])

    model.setParam("display/freq", 1)
    model.optimize()
    
    return model, y, x

def obtener_solucion_primal_1(model):
    sol = model.getBestSol()
    status = model.getStatus()

    if sol is not None and status in ["optimal", "feasible"]:
        x = [v.getLPSol() for v in model.getVars(False)]
        return x, model.getObjVal()
    else:
        return None

def obtener_solucion_dual_1(model):
    y = [model.getDualSolVal(c) for c in model.getConss(False)]
    return y, quicksum(y)
