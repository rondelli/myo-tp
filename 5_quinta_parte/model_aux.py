import sys

sys.path.insert(0, "../4_cuarta_parte")

from pyscipopt import Model
from pyscipopt import quicksum
import time
from Pattern import obtener_patrones

########################################################################
    # d_t: capacidad del disco en TB,
    # F: nombres de los archivos,
    # s: tamaños de los archvios,
    # time_limit: threshold en segundos
########################################################################

# * Es el modelo del punto 4, con la diferencia de que tiene un >= en lugar de un ==
# * Creo que podria optimizarse haciendo que la función que genera patrones retorne solo los patrones maximales
# (me refiero a los patrones con la mayor cantidad de archivos por disco, en luagr del codigo actual que permite que en el disco
# sobre espacio --> sería descomentar un if nomas).
def generar_conjuntos(d_t, F, s, time_limit=420):
    
    tiempo_inicio = time.time()
   
    # {tamaño: cantidad de archivos con ese tamaño}
    tamaños_cantidades = {size: s.count(size) for size in set(s)}
    # ordena el diccionario por tamaños, de mayor a menor
    tamaños_cantidades = dict(sorted(tamaños_cantidades.items(), reverse=True))

    # lista de los tamaños únicos de archivo de S
    tamaños_existentes = list(dict.fromkeys(tamaños_cantidades))
    t = len(tamaños_existentes) # Cantidad de tamaños diferentes de archivos

    c = obtener_patrones(d_t * 10**6, tamaños_cantidades, 420)
    q = len(c)

    model = Model("model_aux_part_5")
    time_limit = time_limit - (time.time() - tiempo_inicio)
    model.setParam("limits/time", time_limit)

    # x[p] entera: cantidad de veces que se usa el patrón p, con p ∈ {1,…,q}, donde x_{p} ≥ 0
    x = [model.addVar(vtype='I', name=f"x_{p}") for p in range(q)]

    # Minimizar la cantidad de patrones usados
    model.setObjective(quicksum(x), sense="minimize")

    # Hay que cubrir todos los archivos de cada tamaño
    for k in range(t):
        # La consigna dice que cada archivo debe estar en *al menos* un conjunto. En el modelo 4 sí dice ==.
        model.addCons(quicksum(c[p][k] * x[p] for p in range(q)) >= tamaños_cantidades[tamaños_existentes[k]])

    model.optimize()

    solution = model.getBestSol()
    status = model.getStatus()

    if solution is not None and status in ["optimal", "feasible"]:

        tamaños_nombres = {tamaño: [] for tamaño in tamaños_existentes}
        for i in range(len(s)):
            tamaños_nombres[s[i]].append(F[i])

        conjuntos_archivos = []
        for p in range(q):
            cantidad = int(model.getVal(x[p]))
            if cantidad > 0:
                for _ in range(cantidad):
                    conjunto = []
                    for k in range(t):
                        tamaño = tamaños_existentes[k]
                        num_archivos = c[p][k]
                        conjunto.extend(tamaños_nombres[tamaño][:num_archivos])
                        tamaños_nombres[tamaño] = tamaños_nombres[tamaño][num_archivos:]
                    conjuntos_archivos.append(conjunto)
        return conjuntos_archivos
    else:
        return None


def obtener_conjuntos_seleccionados(solucion):
    conjuntos_seleccionados = [i for i in range(len(solucion)) if solucion[i] == 1]
    return conjuntos_seleccionados


def obtener_solucion_entera(model, solucion_continua):
    variables = model.getVars()
    sol = model.getBestSol()
    mejor_combinacion = None
    mejor_solucion = float('inf')

    for i in range(1, 10):
        umbral = i/10
        redondeos = [1 if valor >= umbral else 0 for valor in solucion_continua]

        if es_optimo(model, variables, redondeos, sol):
            valor_objetivo = model.getSolObjVal(sol)
            model.hideOutput()

            if valor_objetivo < mejor_solucion:
                mejor_solucion = valor_objetivo
                mejor_combinacion = redondeos

    return mejor_combinacion


def es_optimo(model, variables, solucion, sol):
    for var, val in zip(variables, solucion):
        model.setSolVal(sol, var, val)
    
    return model.checkSol(sol)