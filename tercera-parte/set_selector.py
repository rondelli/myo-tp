from pyscipopt import Model

# recibe: archivos, conjuntos H
def elegir_conjuntos(F: list, H: list):
    model = Model("set_selector")
    n = len(F) # cantidad de archivos
    m = len(H) # cantidad de conjuntos

    if n == 0: return

    # x_{i} = 1 si se elige el conjunto i, 0 si no
    x = [model.addVar(f"x_{j}", vtype="BINARY") for j in range(m)]

    # y_{i, j} = constante. 1 si el archivo i esta en el conjunto j, 0 si no
    y = {}
    for i in range(n):
        for j in range(m):
            y[i, j] = 1 if F[i] in H[j] else 0

    model.setObjective(sum(x[j] for j in range(m)), sense="minimize")
    
    # Todos los archivos deben estar en al menos un conjunto elegido
    for i in range(n):
        model.addCons(sum(y[i, j] * x[j] for j in range(m)) >= 1)

    model.optimize()
    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus() == "feasible":
        conjuntos_seleccionados = [j for j in range(m) if model.getVal(x[j]) > 0.5]
        return conjuntos_seleccionados
    else:
        return None
