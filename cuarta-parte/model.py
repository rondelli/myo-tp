from pyscipopt import Model

"""
d_t --> capacidad del disco
F --> archivos
S --> tamaños de archivos 
T --> maxima cantidad de tamaños
"""
def distribuir_archivos(d_t, F, S, t):
    model = Model("Model")
    d = d_t * 10**6

    if d < 0 or any(s_i < 0 for s_i in S):
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

    # z{s, j} = 1 si el tamaño size está en el disco j, 0 si no
    z = {}
    for s in set(S):
        for j in range(m):
            z[s, j] = model.addVar(f"t_{s}_{j}", vtype="BINARY")

    # Cada archivo se elige solo para un disco
    for i in range(n):
        model.addCons(sum(x[i, j] for j in range(m)) == 1)

    # Los archivos no superan de capacidad los discos
    for j in range(m):
        model.addCons(sum(x[i, j] * S[i] for i in range(n)) <= d * y[j])

     # z{s, j} = 1 si ese tamaño está en el disco
     # aca decimos que si no esta el tamaño en el disco, la variable vale 0
     # pero creo que no dice que si el tamaño *si* está en el disco la variable *tiene* que ser 1
    for s in set(S):
        for j in range(m):
            model.addCons(z[s, j] <= sum(x[i, j] for i in range(n) if S[i] == s))

    # Limitamos los tamaños únicos por disco
    for j in range(m):
        model.addCons(sum(z[s, j] for s in set(S)) <= t)

    model.optimize()
    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus(
    ) == "feasible":
        return [F, model, y, x, S]
    else:
        return None
