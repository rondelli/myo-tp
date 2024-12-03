import sys
from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING
from pyscipopt import *

# Model segunada parte
def distribuir_archivos_2(d_t: int, F: list[str], s: list[int], I: list[float], time_limit = 420):
    model, fake_x = resolver_modelo_binario_2(d_t, F, s, I, time_limit)
    try:
        x, obj_x = obtener_solucion_primal_2(model)
    except TypeError:
        x, obj_x = None, None

    # sys.stderr.write(f"[Debugging] obj x {obj_x}\n")

    solution = model.getBestSol()
    status = model.getStatus()

    if solution is not None and status in ["optimal", "feasible"]:
        sys.stderr.write(f"[Debuggin] {status}: {solution}\n\n")
        return [F, model, fake_x, I, s]
    else:
        return None

def resolver_modelo_binario_2(d_t: int, F: list[str], s: list[int], I: list[float], time_limit=420):
    model = Model("model_part_2")
    model.setParam("limits/time", time_limit)

    d = d_t * 10**6

    n = len(F)

    ########################################################################
    # BINARY
    # x_{i} = 1 si se elige el archivo i, 0 si no
    x = [model.addVar(f"y_{i}", vtype="BINARY") for i in range(n)]
    ########################################################################

    # maximize importance:
    model.setObjective(quicksum(x[i] * I[i] for i in range(n)), sense="maximize")

    # los archivos elegidos deben entrar en el disco
    model.addCons(quicksum(x[i] * s[i] for i in range(n)) <= d)

    #model.setParam("display/freq", 1)

    
    model.setHeuristics(SCIP_PARAMSETTING.FAST) # Parece más rápido

    model.setEmphasis(SCIP_PARAMEMPHASIS.EASYCIP)
    model.setParam("parallel/maxnthreads", 16)

    model.optimize()

    sys.stderr.write(f"[Debugging] model_part_2 Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debugging] model_part_2 Cantidad sols: {model.getNSols()}\n\n")

    return model, x

# Crea el modelo relajado y lo devuelve optimizado
def crear_modelo_2(d_t: int, F: list[str], s: list[int], I: list[float], time_limit=420):
    model = Model("model_part_2")
    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)

    d = d_t * 10**6

    n = len(F)

    ########################################################################
    # CONTINUOUS
    # x_{i} = 1 si se elige el archivo i, 0 si no
    x = [model.addVar(f"y_{i}", lb=0, ub=1, vtype="CONTINUOUS") for i in range(n)]
    ########################################################################

    # maximize importance:
    model.setObjective(quicksum(x[i] * I[i] for i in range(n)), sense="maximize")

    # los archivos elegidos deben entrar en el disco
    model.addCons(quicksum(x[i] * s[i] for i in range(n)) <= d)

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

    sys.stderr.write(f"[Debugging] model_part_2 Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debugging] model_part_2 Cantidad sols: {model.getNSols()}\n\n")

    return model

def obtener_solucion_primal_2(model):
    sol = model.getBestSol()
    status = model.getStatus()

    if sol is not None and status in ["optimal", "feasible"]:
        sys.stderr.write(f"[Debugging] {status}: {sol}\n\n")

        x = [v.getLPSol() for v in model.getVars(False)]

        sys.stderr.write(f"[Debugging]: {x}\n\n")
        return x, model.getObjVal()
    else:
        return None

def obtener_solucion_dual_2(model):
    # No debería ser necesario si el modelo ya viene optimizado con el presolving off
    # Aseguarse de apagar el presolving
    # model.setPresolve(SCIP_PARAMSETTING.OFF)

    # La longitud de y coincide con la cantidad de archivos del input
    y = [model.getDualSolVal(c) for c in model.getConss(False)]

    return y, quicksum(y)
