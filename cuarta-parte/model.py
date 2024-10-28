from pyscipopt import Model, quicksum

# d_t: disk size in TB
# F: file names
# S: File sizes in MB
def distribuir_archivos(d_t: int, F: list[str], S: list[int]):
    if d_t < 0 or any(i < 0 for i in S):
        return

    # Tamaño del disco en MB
    d = d_t * 10**6

    # Cantidad de archivos
    n = len(F)

    # Cantidad de tamaños de archivos
    S = list(dict.fromkeys(S))
    q = len(S)

    # Cantidad de discos, a lo sumo, un disco por archivo
    m = n

    # Define model
    model = Model("big_data_2")

    # c[k, j] integer: cantidad de archivos de tamaño $k$ que entran en el disco $j$
    c = {}
    for k in range(q):
        for j in range(m):
            c[k, j] = model.addVar(vtype='I', name=f"c_{k}_{j}")

    # y[j] binary: 1 si se usa el disco $j$, 0 en caso contrario
    y = [model.addVar(vtype='B', name=f"y_{j}") for j in range(m)]

    # minimize disks:
    model.setObjective(quicksum(y), sense="minimize")

    # No pueden haber discos usados con cero cantidad de archivos
    for j in range(m):
        model.addCons(quicksum(
            c[k, j] for k in range(q)) >= 1)

    # Cantidad archivos de tamaño $k$ que entran en el disco $j$
    for j in range(m):
        model.addCons(quicksum(S[k] * c[k, j] for k in range(q)) <= d * y[j])

    model.optimize()
    solution = model.getBestSol()

    if solution is not None and model.getStatus() == "optimal" or model.getStatus() == "feasible":
        return [F, model, y, c, S]
    else:
        return None
