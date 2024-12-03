from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING
from itertools import product
from math import floor, ceil

import pyscipopt

def elegir_conjuntos(F: list, H: list, time_limit=420):
    model = Model("model_part_3")
    model.setParam("limits/time", time_limit)

    n = len(F)  # cantidad de archivos
    m = len(H)  # cantidad de conjuntos

    if n == 0: return

    # x_{i} = 1 si se elige el conjunto i, 0 si no
    x = [model.addVar(f"x_{j}", vtype="BINARY") for j in range(m)]

    # y_{i, j} = constante. 1 si el archivo i esta en el conjunto j, 0 si no
    y = {}
    for i in range(n):
        for j in range(m):
            y[i, j] = 1 if F[i] in H[j] else 0

    model.setObjective(quicksum(x[j] for j in range(m)), sense="minimize")

    # Todos los archivos deben estar en al menos un conjunto elegido
    for i in range(n):
        model.addCons(quicksum(y[i, j] * x[j] for j in range(m)) >= 1)

    model.optimize()
    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus(
    ) == "feasible":
        conjuntos_seleccionados = [
            j for j in range(m) if model.getVal(x[j]) > 0.5
        ]
        return conjuntos_seleccionados
    else:
        return None

# Crea el modelo relajado y lo devuelve optimizado
def crear_modelo_3(F: list, H: list, time_limit=420):
    model = Model("model_part_3")
    model.setParam("limits/time", time_limit)
    
    n = len(F)  # cantidad de archivos
    m = len(H)  # cantidad de conjuntos

    ########################################################################
    # CONTINUOUS
    # x_{j} = 1 si se elige el conjunto j, 0 si no
    x = [model.addVar(f"x_{j}", lb=0, ub=1, vtype="CONTINUOUS") for j in range(m)]
    #
    ########################################################################

    # a_{i, j} = constante. 1 si el archivo i esta en el conjunto j, 0 si no
    a = {}
    for i in range(n):
        for j in range(m):
            a[i, j] = 1 if F[i] in H[j] else 0

    model.setObjective(quicksum(x[j] for j in range(m)), sense="minimize")

    # Todos los archivos deben estar en al menos un conjunto elegido
    for i in range(n):
        model.addCons(quicksum(a[i, j] * x[j] for j in range(m)) >= 1)
    
    # Desactivación temporal de presolve
    model.setPresolve(SCIP_PARAMSETTING.OFF)

    ####################################################
    #
    model.disablePropagation()
    model.setHeuristics(pyscipopt.SCIP_PARAMSETTING.OFF)
    #
    ####################################################

    #model.setHeuristics(SCIP_PARAMSETTING.AGGRESSIVE)
    model.setHeuristics(SCIP_PARAMSETTING.FAST) # Parece más rápido

    model.setEmphasis(pyscipopt.SCIP_PARAMEMPHASIS.EASYCIP)
    model.setParam("parallel/maxnthreads", 16)

    model.optimize()
    return model


def obtener_solucion_primal_3(model):
    # Activación de presolve
    model.setPresolve(SCIP_PARAMSETTING.DEFAULT)
    sol = model.getBestSol()
    status = model.getStatus()

    status = model.getStatus()
    if sol is not None and status in ["optimal", "feasible"]:
        x = [v.getLPSol() for v in model.getVars()]
        return x, model.getObjVal()
    return None, None

# Esta función supone que el model es `optimal`
def obtener_solucion_dual_3(model):
    y = [model.getDualSolVal(c) for c in model.getConss(False)]
    return y, quicksum(y)

def obtener_conjuntos_seleccionados(solucion):
    conjuntos_seleccionados = [i for i in range(len(solucion)) if solucion[i] == 1]
    return conjuntos_seleccionados
