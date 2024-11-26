import sys
from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING

# Model segunada parte
def distribuir_archivos(d_t, F, s, I):
    model = Model("importance")
    d = d_t * 10**6

    if d < 0 or any(s_i < 0 for s_i in s):
        return

    n = len(F)

    # x_{i} = 1 si se elige el archivo i, 0 si no
    x = [model.addVar(f"y_{i}", vtype="BINARY") for i in range(n)]

    model.setObjective(quicksum(x[i] * I[i] for i in range(n)), sense="maximize")

    # los archivos elegidos deben entrar en el disco
    model.addCons(quicksum(x[i] * s[i] for i in range(n)) <= d)
    model.optimize()

    sys.stderr.write(f"[Debuggin] Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debuggin] Cantidad sols: {model.getNSols()}\n\n")

    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus(
    ) == "feasible":
        sys.stderr.write(f"[Debuggin] {model.getStatus()}: {model.getBestSol()}\n\n")
        return [F, model, x, I, s]
    else:
        return None

# Crea el modelo y lo devuelve optimizado
def crear_modelo_2(d_t: int, F: list[str], s: list[int], I: float, time_limit=420):
    model = Model("model_part_2")

    d = d_t * 10**6

    n = len(F)

    ########################################################################
    # BINARY
    # x_{i} = 1 si se elige el archivo i, 0 si no
    """
    x = [model.addVar(f"y_{i}", vtype="BINARY") for i in range(n)]
    """
    ########################################################################

    ########################################################################
    # CONTINUOUS
    # x_{i} = 1 si se elige el archivo i, 0 si no
    x = [model.addVar(f"y_{i}", lb=0, ub=1, vtype="CONTINUOUS") for i in range(n)]
    ########################################################################

    # maximize importance:
    model.setObjective(quicksum(x[i] * I[i] for i in range(n)), sense="maximize")

    # los archivos elegidos deben entrar en el disco
    model.addCons(quicksum(x[i] * s[i] for i in range(n)) <= d)

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

    sys.stderr.write(f"[Debugging] Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debugging] Cantidad sols: {model.getNSols()}\n\n")

    return model

def obtener_solucion_primal_2(model):
    sol = model.getBestSol()
    status = model.getStatus()

    if sol is not None and status in ["optimal", "feasible"]:
        sys.stderr.write(f"[Debugging] {model.getStatus()}: {model.getBestSol()}\n\n")

        x = [v.getLPSol() for v in model.getVars(False)]

        sys.stderr.write(f"[Debugging]: todas las variables del primal model_part_1 {x}\n\n")
        return x, model.getObjVal()
    else:
        return None

def obtener_solucion_dual(model):
    # No debería ser necesario si el modelo ya viene optimizado con el presolving off
    # Aseguarse de apagar el presolving
    # model.setPresolve(SCIP_PARAMSETTING.OFF)

    # La longitud de y coincide con la cantidad de archivos del input
    y = [model.getDualSolVal(c) for c in model.getConss(False)]

    return y, quicksum(y)
