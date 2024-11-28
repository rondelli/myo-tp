from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING
from itertools import product
from math import floor, ceil

import pyscipopt

def elegir_conjuntos(F: list, H: list):
    model = Model("model_part_3")
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
def crear_modelo_3(F: list, H: list):
    model = Model("model_part_3")
    
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
    # Esto es la clave para que obj(dual) = obj(primal)
    # según documentación de pyscipopt
    #
    model.disablePropagation()
    model.setHeuristics(pyscipopt.SCIP_PARAMSETTING.OFF)
    #
    ####################################################

    model.optimize()
    return model

# La cantidad de constraints coinciden con la cantidad de archivos, por
# ende, la cantidad de variables del dual coinciden con la cantidad de
# archivos del input.
def obtener_solucion_primal_3(model):
    # Activación de presolve
    model.setPresolve(SCIP_PARAMSETTING.DEFAULT) # esta línea no tiene efecto porque el model ya está optimize()

    sol = model.getBestSol()
    
    # esto no debería necesitarse si el modelo ya viene optimizado con el presolving off
    # model.setPresolve(SCIP_PARAMSETTING.OFF)

    status = model.getStatus()
    if sol is not None and status in ["optimal", "feasible"]:
        # Ya no devuelve un array de posiciones, devuelve la solución obtenida por scip
        x = [v.getLPSol() for v in model.getVars()]

        return x, model.getObjVal()

# Esta función supone que el model es `optimal`
def obtener_solucion_dual_3(model):
    # No debería ser necesario si el modelo ya viene optimizado con el presolving off
    # Aseguarse de apagar el presolving
    # model.setPresolve(SCIP_PARAMSETTING.OFF)

    # La longitud de y coincide con la cantidad de archivos del input
    y = [model.getDualSolVal(c) for c in model.getConss(False)]

    return y, quicksum(y)

def obtener_conjuntos_seleccionados(solucion):
    conjuntos_seleccionados = [i for i in range(len(solucion)) if solucion[i] == 1]
    return conjuntos_seleccionados
