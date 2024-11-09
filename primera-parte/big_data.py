import time
from pyscipopt import Model

def distribuir_archivos(d_t, F, s, time_limit=18000000000):
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

    # Registrar el tiempo de inicio antes de optimizar
    start_time = time.time()
    feasible_solution_time = None

    # Comienza la optimización en modo no bloqueante
    model.optimize()

    # Bucle para monitorear el progreso hasta el tiempo límite
    while model.getStatus() not in ["optimal", "infeasible", "timelimit"]:
        # Verificar si se encontró la primera solución factible
        if model.getNSols() > 0 and feasible_solution_time is None:
            feasible_solution_time = time.time() - start_time
            print(f"Se encontró la primera solución factible en {feasible_solution_time:.4f} segundos")
        
        # Si ya pasamos el límite de tiempo, detenemos la optimización
        if time.time() - start_time > time_limit:
            model.interrupt()  # Interrumpir la optimización manualmente
            break
    
    total_time = time.time() - start_time
    if model.getStatus() == "optimal":
        print("Se encontró un óptimo!")

    # Imprimir tiempos
    if feasible_solution_time is not None:
        print(f"Tiempo para la primera solución factible: {feasible_solution_time:.4f} segundos")
    elif model.getStatus() is not "optimal":
        print("No se encontró una solución factible dentro del tiempo límite.")

    print(f"Tiempo total hasta la mejor solución o límite alcanzado: {total_time:.4f} segundos")

    # Obtener la mejor solución encontrada
    sol = model.getBestSol()
    if sol is not None and (model.getStatus() == "optimal" or model.getStatus() == "feasible"):
        return [F, model, y, x, s]
    else:
        return None
