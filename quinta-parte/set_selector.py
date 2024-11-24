from pyscipopt import Model
from pyscipopt import SCIP_PARAMSETTING

# Función para seleccionar conjuntos dados los archivos y conjuntos
def elegir_conjuntos(F: list, H: list):
    model = Model("set_selector")
    model.setPresolve(SCIP_PARAMSETTING.OFF)
    
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
    constraints = []
    for i in range(n):
        cons = model.addCons(sum(y[i, j] * x[j] for j in range(m)) >= 1)
        constraints.append(cons)

    # Optimizar el modelo
    model.optimize()
    sol = model.getBestSol()
    
    if sol is not None and (model.getStatus() == "optimal" or model.getStatus() == "feasible"):
        conjuntos_seleccionados = [j for j in range(m) if model.getVal(x[j]) > 0.5]

        # Obtener valores duales para cada restricción
        solucion_dual = [model.getDualSolVal(c) for c in constraints]

        # Calcular el valor objetivo del primal y dual
        primal_obj_value = model.getObjVal()
        dual_obj_value = sum(solucion_dual)  # rhs es 1 para todas las restricciones

        print("\nSol>>>")
        print("Primal:", primal_obj_value)
        print("Dual:", dual_obj_value)
        print("Gap: {:.2%}".format(abs(primal_obj_value - dual_obj_value) / primal_obj_value))

        print("x*: ", conjuntos_seleccionados)
        print("y*: ", solucion_dual)
        print("primal obj: ", primal_obj_value)
        print("dual obj: ", dual_obj_value)

        if abs(dual_obj_value - primal_obj_value) < 1e-6:
            print("¡Dualidad fuerte confirmada!")
        else:
            print("Los valores objetivo del primal y del dual no coinciden.")

        return conjuntos_seleccionados
    else:
        print("No se encontró una solución factible.")
        return None

# Ejemplo de uso
F = ["archivo1", "archivo2", "archivo3", "archivo4"]
H = [
    {"archivo1", "archivo2"},
    {"archivo2", "archivo3"},
    {"archivo1", "archivo3", "archivo4"},
]

#elegir_conjuntos(F, H)
