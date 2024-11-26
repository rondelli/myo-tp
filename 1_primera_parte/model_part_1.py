import time
import sys
from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING

# Para que no se rompa lo viejo
# No usar esta función
def distribuir_archivos(d_t: int, F: list[str], s: list[int], time_limit=420):
    # model = crear_modelo_1(d_t, F, s, time_limit)
    model, fake_y, fake_x = resolver_modelo_binario_1(d_t, F, s, time_limit)

    x, obj_x = obtener_solucion_primal_1(model)
    # y, obj_y = obtener_solucion_dual_1(model)

    sys.stderr.write(f"[Debugging] obj x {obj_x}\n")
    # sys.stderr.write(f"[Debugging] obj y {obj_y}\n")

    solution = model.getBestSol()
    status = model.getStatus()

    if solution is not None and status in ["optimal", "feasible"]:
        return [F, model, fake_y, fake_x, s]
    else:
        return None

def resolver_modelo_binario_1(d_t: int, F: list[str], s: list[int], time_limit=420):
    model = Model("model_part_1")

    d = d_t * 10**6

    n = len(F)
    m = n  # no se puede tener más discos que archivos

    ########################################################################
    # BINARY
    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    #
    x = {}
    for i in range(n):
        for j in range(m):
            x[i, j] = model.addVar(name = f"x_{i}_{j}", vtype="BINARY")

    # y_{j} = 1 si se elige el disco j, 0 si no
    y = [model.addVar(f"y_{j}", vtype="BINARY") for j in range(m)]
    #
    ########################################################################

    # minimize disks:
    model.setObjective(quicksum(y), sense="minimize")

    # Que los archivos se elijan solo para un disco
    for i in range(n):
        model.addCons(quicksum(x[i, j] for j in range(m)) == 1)

    # Que no se pasen de capacidad los discos
    for j in range(m):
        model.addCons(quicksum(x[i, j] * s[i] for i in range(n)) <= d * y[j])

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)
    model.setParam("display/freq", 1)

    model.optimize()

    sys.stderr.write(f"[Debugging] [MODELO 1] Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debugging] [MODELO 1] Cantidad sols: {model.getNSols()}\n\n")

    return model, y, x

# Crea el modelo y lo devuelve optimizado
def crear_modelo_1(d_t: int, F: list[str], s: list[int], time_limit=420):
    model = Model("model_part_1")

    d = d_t * 10**6

    n = len(F)
    m = n  # no se puede tener más discos que archivos

    ########################################################################
    # CONTINUOUS
    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    #
    x = {}
    for i in range(n):
        for j in range(m):
            x[i, j] = model.addVar(name = f"x_{i}_{j}", lb=0, ub=1, vtype="CONTINUOUS")

    # y_{j} = 1 si se elige el disco j, 0 si no
    y = [model.addVar(f"y_{j}", lb=0, ub=1, vtype="CONTINUOUS") for j in range(m)]
    #
    ########################################################################

    # minimize disks:
    model.setObjective(quicksum(y), sense="minimize")

    # Que los archivos se elijan solo para un disco
    for i in range(n):
        model.addCons(quicksum(x[i, j] for j in range(m)) == 1)

    # Que no se pasen de capacidad los discos
    for j in range(m):
        model.addCons(quicksum(x[i, j] * s[i] for i in range(n)) <= d * y[j])

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)
    model.setParam("display/freq", 1)

    # Desactivación temporal de presolve
    model.setPresolve(SCIP_PARAMSETTING.OFF)

    ####################################################
    # Esto es la clave para que obj(dual) = obj(primal)
    # según documentación de pyscipopt
    #
    model.disablePropagation()
    model.setHeuristics(SCIP_PARAMSETTING.OFF)
    #
    ####################################################

    model.optimize()

    sys.stderr.write(f"[Debugging] [MODELO 1] Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debugging] [MODELO 1] Cantidad sols: {model.getNSols()}\n\n")

    return model

def obtener_solucion_primal_1(model):
    sol = model.getBestSol()
    status = model.getStatus()

    if sol is not None and status in ["optimal", "feasible"]:
        sys.stderr.write(f"[Debugging] {model.getStatus()}: {model.getBestSol()}\n\n")

        # El nombre de variable x, acá es missleading, es x porque es el primal.
        # Esta línea devuelve **todas** las variables del modelo, las $x$: archivo seleccionado y las $y$: disco seleccionado
        x = [v.getLPSol() for v in model.getVars(False)]

        sys.stderr.write(f"[Debugging]: todas las variables del primal model_part_1 {x}\n\n")
        return x, model.getObjVal()
    else:
        return None

def obtener_solucion_dual_1(model):
    # No debería ser necesario si el modelo ya viene optimizado con el presolving off
    # Aseguarse de apagar el presolving
    # model.setPresolve(SCIP_PARAMSETTING.OFF)

    # La longitud de y coincide con la cantidad de archivos del input
    y = [model.getDualSolVal(c) for c in model.getConss(False)]

    return y, quicksum(y)
