import time
import sys
from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING

# No usar esta función
def distribuir_archivos(d_t, F, s, t, time_limit=420):
    modelo = crear_modelo_4(d_t, F, s, t, time_limit)
    x, obj_x = obtener_solucion_primal_4(modelo)
    y, obj_y = obtener_solucion_dual_4(modelo)

    sys.stderr.write(f"[Debugging] obj x {obj_x}\n")
    sys.stderr.write(f"[Debugging] obj y {obj_y}\n")

def crear_modelo_4(d_t: int, F: list[str], S: list[int], t: int, time_limit=420):
    model = Model("model_part_4")

    d = d_t * 10**6
    n = len(F)
    m = n

    ########################################################################
    # BINARY
    # y = [model.addVar(f"y_{j}", vtype="BINARY") for j in range(m)]
    # # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    # x = {}
    # for i in range(m):
    #     for j in range(m):
    #         x[i, j] = model.addVar(f"x_{i}_{j}", vtype="BINARY")
    
    # z = {}
    # for s in set(S):
    #     for j in range(m):
    #         z[s, j] = model.addVar(f"t_{s}_{j}", vtype="BINARY")  
    ########################################################################

    ########################################################################
    # CONTINUOUS
    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    y = [model.addVar(f"y_{j}", vtype="CONTINUOUS") for j in range(m)]
    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    x = {}
    for i in range(m):
        for j in range(m):
            x[i, j] = model.addVar(f"x_{i}_{j}", vtype="CONTINUOUS")
    
    z = {}
    for s in set(S):
        for j in range(m):
            z[s, j] = model.addVar(f"t_{s}_{j}", vtype="CONTINUOUS") 
    ########################################################################

    model.setObjective(quicksum(y), sense="minimize")

     # Cada archivo se elige solo para un disco
    for i in range(n):
        model.addCons(sum(x[i, j] for j in range(m)) == 1)

    # Los archivos no superan de capacidad los discos
    for j in range(m):
        model.addCons(sum(x[i, j] * S[i] for i in range(n)) <= d * y[j])

     # z{s, j} = 1 si ese tamaño está en el disco
    for s in set(S):
        for j in range(m):
            model.addCons(z[s, j] <= sum(x[i, j] for i in range(n) if S[i] == s))

    # Limitamos los tamaños únicos por disco
    for j in range(m):
        model.addCons(sum(z[s, j] for s in set(S)) <= t)

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)
    model.setParam("display/freq", 1)

    # Desactivación temporal de presolve
    model.setPresolve(SCIP_PARAMSETTING.OFF)

    ####################################################

    model.disablePropagation()
    model.setHeuristics(SCIP_PARAMSETTING.OFF)
    
    ####################################################

    model.optimize()

    sys.stderr.write(f"[Debugging] Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debugging] Cantidad sols: {model.getNSols()}\n\n")

    return model

def obtener_solucion_primal_4(model):
    sol = model.getBestSol()
    status = model.getStatus()

    if sol is not None and status in ["optimal", "feasible"]:
        sys.stderr.write(f"[Debugging] {model.getStatus()}: {model.getBestSol()}\n\n")
        x = [v.getLPSol() for v in model.getVars(False)]

        sys.stderr.write(f"[Debugging]: todas las variables del primal model_part_1 {x}\n\n")
        return x, model.getObjVal()
    else:
        return None

def obtener_solucion_dual_4(model):
    y = [model.getDualSolVal(c) for c in model.getConss(False)]

    return y, sum(y)
