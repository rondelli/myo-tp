from pyscipopt import Model

# Model segunada parte
def distribuir_archivos(d_t, F, s, I):
    model = Model("importance")
    d = d_t * 10**6

    if d < 0 or any(s_i < 0 for s_i in s):
        return

    n = len(F)

    # x_{i} = 1 si se elige el archivo i, 0 si no
    x = [model.addVar(f"y_{i}", vtype="BINARY") for i in range(n)]

    model.setObjective(sum(x[i] * I[i] for i in range(n)), sense="maximize")

    # los archivos elegidos deben entrar en el disco
    model.addCons(sum(x[i] * s[i] for i in range(n)) <= d)

    model.optimize()
    sys.stderr.write(f"[Debuggin] Time: {model.getSolvingTime()}\n\n")

    sys.stderr.write(f"[Debuggin] Cantidad sols: {model.getNSols()}\n\n")

    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus(
    ) == "feasible":
        sys.stderr.write(f"[Debuggin] {model.getStatus()}: {model.getBestSol()}\n\n")
        return [F, model, x, I, s]
    else:
        return None
