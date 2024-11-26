import sys
from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING

"""
def distribuir_archivos(d_t, F, S, t, time_limit=420):
    model = crear_modelo_4(d_t, F, S, t, time_limit)

    x, obj_x = obtener_solucion_primal_4(model)
    y, obj_y = obtener_solucion_dual_4(model)

    sys.stderr.write(f"[Debugging] obj x {obj_x}\n")
    sys.stderr.write(f"[Debugging] obj y {obj_y}\n")
"""

# Para que no se rompa lo viejo
# No usar esta función
def distribuir_archivos(d_t, F, S, t, time_limit=420):
    model = Model("model_part_4")
    d = d_t * 10**6

    if d < 0 or any(s_i < 0 for s_i in S):
        return

    n = len(F)
    m = n  # no se puede tener más discos que archivos

    # y_{j} = 1 si se elige el disco j, 0 si no
    y = [model.addVar(f"y_{j}", vtype="BINARY") for j in range(m)]

    model.setObjective(quicksum(y), sense="minimize")

    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    x = {}
    for i in range(m):
        for j in range(m):
            x[i, j] = model.addVar(f"x_{i}_{j}", vtype="BINARY")

    # z{s, j} = 1 si el tamaño size está en el disco j, 0 si no
    z = {}
    for s in set(S):
        for j in range(m):
            z[s, j] = model.addVar(f"t_{s}_{j}", vtype="BINARY")

    # Cada archivo se elige solo para un disco
    for i in range(n):
        model.addCons(quicksum(x[i, j] for j in range(m)) == 1)

    # Los archivos no superan de capacidad los discos
    for j in range(m):
        model.addCons(quicksum(x[i, j] * S[i] for i in range(n)) <= d * y[j])

     # z{s, j} = 1 si ese tamaño está en el disco
     # aca decimos que si no esta el tamaño en el disco, la variable vale 0
     # pero creo que no dice que si el tamaño *si* está en el disco la variable *tiene* que ser 1
    for s in set(S):
        for j in range(m):
            model.addCons(z[s, j] <= quicksum(x[i, j] for i in range(n) if S[i] == s))

    # Limitamos los tamaños únicos por disco
    for j in range(m):
        model.addCons(quicksum(z[s, j] for s in set(S)) <= t)

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)
    model.setParam("display/freq", 1)

    model.optimize()

    sys.stderr.write(f"[Debuggin] Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debuggin] Cantidad sols: {model.getNSols()}\n\n")

    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus(
    ) == "feasible":
        sys.stderr.write(f"[Debuggin] {model.getStatus()}: {model.getBestSol()}\n\n")
        return [F, model, y, x, S]
    else:
        return None

def crear_modelo_4(d_t: int, F: list[str], S: list[int], t, time_limit=420):
    model = Model("model_part_4")
    d = d_t * 10**6

    n = len(F)
    m = n  # no se puede tener más discos que archivos

    ########################################################################
    # CONTINUOUS
    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    x = {}
    for i in range(n):
        for j in range(m):
            x[i, j] = model.addVar(f"x_{i}_{j}", lb=0, ub=1, vtype="CONTINUOUS")

    # y_{j} = 1 si se elige el disco j, 0 si no
    y = [model.addVar(f"y_{j}", lb=0, ub=1, vtype="CONTINUOUS") for j in range(m)]

    # z{s, j} = 1 si el tamaño size está en el disco j, 0 si no
    z = {}
    for s in set(S):
        for j in range(m):
            z[s, j] = model.addVar(f"t_{s}_{j}", lb=0, ub=1, vtype="CONTINUOUS")
    #
    ########################################################################

    model.setObjective(quicksum(y), sense="minimize")

    # Cada archivo se elige solo para un disco
    for i in range(n):
        model.addCons(quicksum(x[i, j] for j in range(m)) == 1)

    # Los archivos no superan de capacidad los discos
    for j in range(m):
        model.addCons(quicksum(x[i, j] * S[i] for i in range(n)) <= d * y[j])

     # z{s, j} = 1 si ese tamaño está en el disco
     # aca decimos que si no esta el tamaño en el disco, la variable vale 0
     # pero creo que no dice que si el tamaño *si* está en el disco la variable *tiene* que ser 1
    for s in set(S):
        for j in range(m):
            model.addCons(z[s, j] <= quicksum(x[i, j] for i in range(n) if S[i] == s))

    # Limitamos los tamaños únicos por disco
    for j in range(m):
        model.addCons(quicksum(z[s, j] for s in set(S)) <= t)

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

    sys.stderr.write(f"[Debugging] [MODELO 4] Time: {model.getSolvingTime()}\n\n")
    sys.stderr.write(f"[Debugging] [MODELO 4] Cantidad sols: {model.getNSols()}\n\n")

    return model

def obtener_solucion_primal_4(model):
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

def obtener_solucion_dual_4(model):
    # No debería ser necesario si el modelo ya viene optimizado con el presolving off
    # Aseguarse de apagar el presolving
    # model.setPresolve(SCIP_PARAMSETTING.OFF)

    # La longitud de y coincide con la cantidad de archivos del input
    y = [model.getDualSolVal(c) for c in model.getConss(False)]

    return y, quicksum(y)
