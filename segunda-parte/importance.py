from pyscipopt import Model
from configuracion import generardor_output

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
    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus() == "feasible":
        generardor_output.generar_output("a_2.out", F, model, x, I, s)
    else:
        generardor_output.generar_output_fallido("a_2.out")
