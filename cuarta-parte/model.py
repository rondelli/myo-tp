from pyscipopt import Model, quicksum

# d_t: disk size in TB
# F: file names with sizes in MB
# S: File sizes in MB
def distribuir_archivos(d_t, F, S):
    if d_t < 0 or any(i < 0 for i in S):
        return

    # Tamaño del disco en MB
    d = d_t * 10**6

    # Cantidad de archivos
    n = len(F)

    size_counts = {}
    for s in S:
        size_counts[s] = size_counts.get(s, 0) + 1

    S = list(dict.fromkeys(S))
    # X: con esto se pierden los tamaños de los archivos
    # H: claro, acá falta contar la cantidad de cada tamaño de archivos
    # tipo:
    #
    # MB    count
    # -----------
    # 50    5
    # 80    2
    # 100   7
    # 
    # por eso puse un map

    # Cantidad de tamaños de archivos
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

    for j in range(m):
        model.addCons(quicksum(c[k, j] for k in range(q)) >= 1)

    # Cantidad archivos de tamaño $k$ que entran en el disco $j$
    for j in range(m):
        model.addCons(quicksum(S[k] * c[k, j] for k in range(q)) <= d * y[j])

    # No pueden entrar más de $n$ archivos por disco
    # for j in range(m):
        # model.addCons(quicksum(c[k, j] for k in range(q)) <= n * y[j])

    model.optimize()
    solution = model.getBestSol()

    model.getBestSol()
    
    if solution:
        print("Solución encontrada:")
        print(f"Cantidad de discos utilizados: {round(float(model.getObjVal()))}\n")
        for j in range(m):
            if model.getVal(y[j]) == 0:
                continue
            archivos_en_disco = []
            used_space = 0
            for i in range(n):
                if (i, j) in c and model.getVal(c[i, j]) > 0:
                    archivos_en_disco.append(f"{F[i]}  {S[i]} MB")
                    used_space += S[i]
            print(f"Disco {j + 1}: {used_space} MB")
            for archivo in archivos_en_disco:
                print(f"  {archivo}")
    else:
        print("No se encontró una solución.")

    if solution is not None and model.getStatus() == "optimal" or model.getStatus() == "feasible":
        return [F, model, y, c, S]
    else:
        return None
