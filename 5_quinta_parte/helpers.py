from itertools import combinations_with_replacement
import time

def generar_subconjuntos_5(peso_disco, nombres_archivos, pesos_archivos):
            H = []
            archivos = list(zip(nombres_archivos, pesos_archivos))
            for i in range(len(archivos)):
                agregado = False
                for j in range(i + 1, len(archivos)):
                    combo = [archivos[i], archivos[j]]
                    total_size = sum(peso for _, peso in combo)
                    if total_size <= peso_disco:
                        H.append([nombre for nombre, _ in combo])
                        agregado = True
                if not agregado:
                     H.append([archivos[i][0]])
            return H

def generar_subconjuntos_6(tamaño_disco, archivos):
    patrones = []
    peso_minimo = min(archivos.values())

    for r in range(1, len(archivos) + 1):
        for combinacion in combinations_with_replacement(archivos.values(), r):
            
            tamaño_combinacion = sum(tamaño for tamaño in combinacion)
            if tamaño_combinacion <= tamaño_disco and tamaño_disco - tamaño_combinacion < peso_minimo:
                patron = {}
                
                for tamaño in combinacion:
                    patron[tamaño] = patron.get(tamaño, 0) + 1
                
                if patron not in patrones:
                    patrones.append(patron)
                # patrones.append([nombre for nombre, _ in combo])

    return patrones

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