from pyscipopt import Model
from pyscipopt import SCIP_PARAMSETTING

# Función para seleccionar conjuntos dados los archivos y conjuntos
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
        conjuntos_seleccionados = [j for j in range(m) if model.getVal(x[j]) > 0.5]

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

def crear_modelo(F: list, H: list):
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
    
    model.disablePropagation()  # esto parece ser la clave para que obj(dual) = obj(primal)
    model.optimize()

    return model

'''
def obtener_solucion_primal(model):
    sol = model.getBestSol()
    
    if sol is not None and (model.getStatus() == "optimal" or model.getStatus() == "feasible"):
        # x* NO SE ESTA USANDO
        conjuntos_seleccionados = [j for j in range(m) if model.getVal(x[j]) > 0.5]
        return conjuntos_seleccionados, model.getObjVal()
'''

def obtener_solucion_dual(model):
    # Desactivación temporal de presolve
    model.setPresolve(SCIP_PARAMSETTING.OFF)
    
    # y*
    y = [model.getDualSolVal(c) for c in model.getConss(False)]

    # Activación de presolve
    model.setPresolve(SCIP_PARAMSETTING.DEFAULT)
    return y, sum(y)

def es_optimo(model, solucion):
    model.freeTransform()
    variables = model.getVars() 

    for var, val in zip(variables, solucion): 
        model.fixVar(var, val)

    model.optimize()
    status = model.getStatus()

    for var in variables: 
        model.freeTransform() 
    
    if status in ["optimal", "feasible"]:
        valor_objetivo = model.getObjVal() 
        return [True, valor_objetivo]
    else: 
        return [False, None]


