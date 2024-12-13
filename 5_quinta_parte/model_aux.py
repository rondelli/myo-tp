from pyscipopt import Model

########################################################################
    # d_t: capacidad del discoen TB,
    # F: nombres de los archivos,
    # s: tamaños de los archvios,
    # time_limit: threshold en segundos
########################################################################

def generar_conjuntos(d_t, F, s, time_limit=420):
    model = Model("Partition Files")
    model.setParam("limits/time", time_limit)
    
    d = d_t * 10**6
    n = len(F)

    # x[i][j] = 1 si el archivo i está en el disco j
    x = {}

    # y[j] = 1 si el disco j se usa
    y = {}

    max_disks = n

    for i in range(n):
        for j in range(max_disks):
            x[i, j] = model.addVar(vtype="B", name=f"x({i},{j})")

    for j in range(max_disks):
        y[j] = model.addVar(vtype="B", name=f"y({j})")

    # Cada archivo debe estar en al menos un disco
    for i in range(n):
        model.addCons(sum(x[i, j] for j in range(max_disks)) >= 1, name=f"coverage({i})")

    # Capacidad de cada disco
    for j in range(max_disks):
        model.addCons(
            sum(x[i, j] * s[i] for i in range(n)) <= d * y[j],
            name=f"capacity({j})"
        )

    # Minimizar discos
    model.setObjective(sum(y[j] for j in range(max_disks)), sense="minimize")

    model.optimize()
    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus() == "feasible":
        conjuntos = []
        for j in range(max_disks):
            if model.getVal(y[j]) > 0.5:
                archivos_en_disco = [
                    F[i] for i in range(n) if model.getVal(x[i, j]) > 0.5
                ]
                conjuntos.append(archivos_en_disco)
        return conjuntos
    else:
        return None
    

def obtener_conjuntos_seleccionados(solucion):
    conjuntos_seleccionados = [i for i in range(len(solucion)) if solucion[i] == 1]
    return conjuntos_seleccionados


def obtener_solucion_entera(model, solucion_continua):
    variables = model.getVars()
    sol = model.getBestSol()
    mejor_combinacion = None
    mejor_solucion = float('inf')

    for i in range(1, 10):
        umbral = i/10
        redondeos = [1 if valor >= umbral else 0 for valor in solucion_continua]

        if es_optimo(model, variables, redondeos, sol):
            valor_objetivo = model.getSolObjVal(sol)
            model.hideOutput()

            if valor_objetivo < mejor_solucion:
                mejor_solucion = valor_objetivo
                mejor_combinacion = redondeos

    return mejor_combinacion


def es_optimo(model, variables, solucion, sol):
    for var, val in zip(variables, solucion):
        model.setSolVal(sol, var, val)
    
    return model.checkSol(sol)