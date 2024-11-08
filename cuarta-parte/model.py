from pyscipopt import Model

"""
d_t --> capacidad del disco
F --> archivos
s --> tamaños de archivos 
T --> maxima cantidad de tamaños
"""
def distribuir_archivos(d_t, F, s, T):
    model = Model("Model")
    d = d_t * 10**6

    if d < 0 or any(s_i < 0 for s_i in s):
        return

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

    # size_used{size, j} = 1 si el tamaño size está en el disco j, 0 si no
    size_used = {}
    for size in set(s):
        for j in range(m):
            size_used[size, j] = model.addVar(f"size_used_{size}_{j}", vtype="BINARY")

    # Cada archivo se elige solo para un disco
    for i in range(n):
        model.addCons(sum(x[i, j] for j in range(m)) == 1)

    # Los archivos no superan de capacidad los discos
    for j in range(m):
        model.addCons(sum(x[i, j] * s[i] for i in range(n)) <= d * y[j])

     # Se activan los size_used si ese tamaño está en el disco
    for size in set(s):
        for j in range(m):
            model.addCons(size_used[size, j] <= sum(x[i, j] for i in range(n) if s[i] == size))

    # Limitamos los tamaños únicos por disco
    for j in range(m):
        model.addCons(sum(size_used[size, j] for size in set(s)) <= T)


    model.optimize()
    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus(
    ) == "feasible":
        return [F, model, y, x, s]
    else:
        return None
