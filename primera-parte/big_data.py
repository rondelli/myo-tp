import time
from pyscipopt import Model

def distribuir_archivos(d_t, F, s, time_limit=60):
    """
    Distribuye archivos entre discos minimizando el número de discos utilizados.
    
    Parámetros:
    - d_t: Capacidad total de cada disco en MB.
    - F: Lista de nombres de archivos.
    - s: Lista de tamaños de archivos correspondientes a cada archivo en MB.
    - time_limit: Tiempo límite en segundos para encontrar la mejor solución posible.

    Retorna:
    - Una lista con la mejor solución encontrada dentro del tiempo límite o None si no se encontró ninguna.
    """
    model = Model("big_data")
    d = d_t * 10**6
    if d < 0 or any(s_i < 0 for s_i in s):
        return None

    n = len(F)
    m = n  # no se puede tener más discos que archivos

    # y_{j} = 1 si se elige el disco j, 0 si no
    y = [model.addVar(f"y_{j}", vtype="BINARY") for j in range(m)]
    model.setObjective(sum(y), sense="minimize")

    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    x = {}
    for i in range(m):
        for j in range(m):
            x[i, j] = model.addVar(f"x_{i}_{j}", vtype="BINARY")

    # Que los archivos se elijan solo para un disco
    for i in range(n):
        model.addCons(sum(x[i, j] for j in range(m)) == 1)

    # Que no se pasen de capacidad los discos
    for j in range(m):
        model.addCons(sum(x[i, j] * s[i] for i in range(n)) <= d * y[j])

    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)

    # Registrar el tiempo de inicio
    start_time = time.time()

    # Ejecutar la optimización
    model.optimize()

    # Calcular el tiempo total de optimización
    total_time = time.time() - start_time

    # Obtener información sobre la primera solución factible y la mejor solución
    feasible_solution_time = None
    if model.getNSols() > 0:
        feasible_solution_time = total_time  # Tiempo hasta la mejor solución dentro del límite

    # Imprimir resultados
    if feasible_solution_time is not None:
        print(f"Tiempo hasta la primera solución factible: {feasible_solution_time:.4f} segundos")
    else:
        print("No se encontró ninguna solución factible dentro del tiempo límite.")

    print(f"Tiempo total hasta la mejor solución o límite alcanzado: {total_time:.4f} segundos")

    # Obtener la mejor solución encontrada
    sol = model.getBestSol()
    if sol is not None and (model.getStatus() == "optimal" or model.getStatus() == "feasible"):
        return [F, model, y, x, s]
    else:
        return None
