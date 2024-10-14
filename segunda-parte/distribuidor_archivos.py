from pyscipopt import Model
from configuracion import generardor_output

def distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos):
    model = Model("big_data")
    d = capacidad_disco * 1000000
    f_i = tamaños_archivos
    b_i = importancia_archivos

    if d < 0 or any(f < 0 for f in f_i):
        return

    cant_archivos = len(nombres_archivos)

    # x_{i} = 1 si se elige el archivo i, 0 si no
    x_i = [model.addVar(f"y_{i}", vtype="BINARY") for i in range(cant_archivos)]

    model.setObjective(sum(x_i[i] * b_i[i] for i in range(cant_archivos)), sense="maximize")
    
    # los archivos elegidos deben entrar en el disco
    model.addCons(sum(x_i[i] * f_i[i] for i in range(cant_archivos)) <= d)

    model.optimize()
    sol = model.getBestSol()

    if sol is not None and model.getStatus() == "optimal" or model.getStatus() == "feasible":
        generardor_output.generar_output("a_2.out", nombres_archivos, model, x_i, b_i, f_i)
    else:
        generardor_output.generar_output_fallido("a_2.out")
