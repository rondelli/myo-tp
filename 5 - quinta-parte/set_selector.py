from pyscipopt import Model
from pyscipopt import SCIP_PARAMSETTING
from itertools import product
from math import floor, ceil

# Esta función ya no se usa (@Lu si no la usás, borrala tranki)
"""
def elegir_conjuntos(F: list, H: list):
    model = Model("set_selector")
    
    n = len(F)  # cantidad de archivos
    m = len(H)  # cantidad de conjuntos

    if n == 0: return
    
    # x_{j} = 1 si se elige el conjunto j, 0 si no
    x = [model.addVar(f"x_{j}", lb=0, ub=1, vtype="CONTINUOUS") for j in range(m)]

    # y_{i, j} = constante. 1 si el archivo i esta en el conjunto j, 0 si no
    y = {}
    for i in range(n):
        for j in range(m):
            y[i, j] = 1 if F[i] in H[j] else 0

    model.setObjective(sum(x[j] for j in range(m)), sense="minimize")

    # Todos los archivos deben estar en al menos un conjunto elegido
    for i in range(n):
        model.addCons(sum(y[i, j] * x[j] for j in range(m)) >= 1)

    # Desactivación temporal de presolve
    model.setPresolve(SCIP_PARAMSETTING.OFF)
    model.disablePropagation()  # esto parece ser la clave para que obj(dual) = obj(primal)

    model.optimize()

    # y*
    solucion_dual = [model.getDualSolVal(c) for c in model.getConss(False)]

    # Activación de presolve
    model.setPresolve(SCIP_PARAMSETTING.DEFAULT)

    sol = model.getBestSol()
    
    if sol is not None and (model.getStatus() == "optimal" or model.getStatus() == "feasible"):
        # x* NO SE ESTA USANDO

        # Xime no confía ni en python ni en scip
        # conjuntos_seleccionados2 = [j for j in range(m) if model.getVal(x[j]) > 0.5]
        conjuntos_seleccionados = [v.getIndex() for v in model.getVars() if v.getLPSol() > 0.5]

        primal_obj = model.getObjVal()
        dual_obj = sum(solucion_dual) # rhs es 1 para todas las restricciones

        print("\nPrimal obj: ", primal_obj)
        print("Dual obj: ", dual_obj)

        if abs(dual_obj - primal_obj) < 1e-6:
            print("[OK] Los valores objetivo coinciden")
        else:
            print("[NO] Los valores objetivo del primal y del dual no coinciden")

        return model, solucion_dual
    else:
        print("No se encontró una solución factible.")
        return None
"""

# Crea el modelo y lo devuelve optimizado
def crear_modelo(F: list, H: list):
    model = Model("set_selector")
    
    n = len(F)  # cantidad de archivos
    m = len(H)  # cantidad de conjuntos

    if n == 0:
        return
    
    # x_{j} = 1 si se elige el conjunto j, 0 si no
    x = [model.addVar(f"x_{j}", lb=0, ub=1, vtype="CONTINUOUS") for j in range(m)]

    # a_{i, j} = constante. 1 si el archivo i esta en el conjunto j, 0 si no
    a = {}
    for i in range(n):
        for j in range(m):
            a[i, j] = 1 if F[i] in H[j] else 0

    model.setObjective(sum(x[j] for j in range(m)), sense="minimize")

    # Todos los archivos deben estar en al menos un conjunto elegido
    for i in range(n):
        model.addCons(sum(a[i, j] * x[j] for j in range(m)) >= 1)
    
    # Desactivación temporal de presolve
    model.setPresolve(SCIP_PARAMSETTING.OFF)

    # Esto parece ser la clave para que obj(dual) = obj(primal)
    model.disablePropagation()

    model.optimize()
    return model

# La cantidad de constraints coinciden con la cantidad de archivos, por
# ende, la cantidad de variables del dual coinciden con la cantidad de
# archivos del input.
def obtener_solucion_primal(model):
    # Activación de presolve
    # model.setPresolve(SCIP_PARAMSETTING.DEFAULT) # esta línea no tiene efecto porque el model ya está optimize()

    sol = model.getBestSol()
    
    model.setPresolve(SCIP_PARAMSETTING.OFF)

    if sol is not None and (model.getStatus() == "optimal" or model.getStatus() == "feasible"):
        # Ya no devuelve un array de posiciones, devuelve la solución obtenida por scip
        x = [v.getLPSol() for v in model.getVars()]

        return x, model.getObjVal()

def obtener_solucion_dual(model):
    # Aseguarse de apagar el presolving
    model.setPresolve(SCIP_PARAMSETTING.OFF)

    # La longitud de y coincide con la cantidad de archivos del input
    y = [model.getDualSolVal(c) for c in model.getConss(False)]

    return y, sum(y)

# No se usa por el momento
# esto está ok? no debería ser si solucion[i] == 1?
def obtener_conjuntos_seleccionados(solucion):
    conjuntos_seleccionados = [i for i in range(len(solucion)) if solucion[i] == 1]
    return conjuntos_seleccionados

# Esta función supone que el model es `optimal`
def es_optimo(model, solucion):
    variables = model.getVars() 

    sol = model.getBestSol()

    for var, val in zip(variables, solucion):
        model.setSolVal(sol, var, val)

    return model.checkSol(sol)

def obtener_solucion_entera(model, solucion_continua):
    print("CONTINUA:", solucion_continua)
    variables = model.getVars()
    sol = model.getBestSol()
    mejor_combinacion = None
    mejor_solucion = float('inf')
    
    for i in range(1, 10):
        umbral = i/10
        redondeos = [1 if valor >= umbral else 0 for valor in solucion_continua]
        if es_optimo_rapido(model, variables, redondeos, sol):
            valor_objetivo = model.getSolObjVal(sol)
            if valor_objetivo < mejor_solucion:
                print("POSIBLE SOL:", mejor_solucion)
                mejor_solucion = valor_objetivo
                mejor_combinacion = redondeos
        
    print("MEJOR:", mejor_combinacion)
    print("SOL:", mejor_solucion)
    return mejor_combinacion

def es_optimo_rapido(model, variables, solucion, sol):
    for var, val in zip(variables, solucion):
        model.setSolVal(sol, var, val)
    
    return model.checkSol(sol)