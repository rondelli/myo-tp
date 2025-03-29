import time

# * Esta opcion retorna conjuntos con los nombres de los archivos, por ejemplo [{'a3', 'a5'}, {'a7', 'a4', 'a1'}, {'a6', 'a2'}]
def generar_subconjuntos(tamaño_disco, nombres_archivos, tamaños_archivos, tiempo_limite=420):
    tiempo_inicio = time.time()
    H = []
    archivos = list(zip(nombres_archivos, tamaños_archivos))
    archivos.sort(key=lambda x: x[1], reverse=True)

    while archivos and hay_tiempo(tiempo_inicio, tiempo_limite):
        subconjunto = set()
        espacio_restante = tamaño_disco

        for archivo in archivos[:]:
            if hay_tiempo(tiempo_inicio, tiempo_limite):
                if archivo[1] <= espacio_restante:
                    subconjunto.add(archivo[0])
                    espacio_restante -= archivo[1]
                    archivos.remove(archivo)
            else:
                return None
        H.append(subconjunto)
    return H

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

def hay_tiempo(tiempo_inicio, tiempo_limite):
    return (time.time() - tiempo_inicio) < tiempo_limite