from itertools import combinations_with_replacement
import time

# * Retorna conjuntos con los nombres de los archivos, por ejemplo [{'a3', 'a5'}, {'a7', 'a4', 'a1'}, {'a6', 'a2'}]
def generar_subconjuntos_5(peso_disco, nombres_archivos, tamaños_archivos):
    H = []
    archivos = list(zip(nombres_archivos, tamaños_archivos))

    for i in range(len(archivos)):
        agregado = False

        for j in range(i + 1, len(archivos)):
            combo = [archivos[i], archivos[j]]
            total_size = sum(peso for _, peso in combo)
            
            if total_size <= peso_disco:
                H.append(set([nombre for nombre, _ in combo]))
                agregado = True
        if not agregado and archivos[i][1] <= peso_disco:
            H.append(set([archivos[i][0]]))
    return H

# * Esta opcion retorna conjuntos con los nombres de los archivos, por ejemplo [{'a3', 'a5'}, {'a7', 'a4', 'a1'}, {'a6', 'a2'}]
def generar_subconjuntos_6(tamaño_disco, nombres_archivos, tamaños_archivos):
    H = []
    archivos = dict(zip(nombres_archivos, tamaños_archivos))
    archivos_disponibles = set(archivos.keys())

    for archivo in sorted(archivos_disponibles, key=lambda x: archivos[x], reverse=True):
            if archivos[archivo] < tamaño_disco:
                return None

    while archivos_disponibles:
        subconjunto = set()
        espacio_restante = tamaño_disco
        print("Nuevo subconjunto: disponibles:", archivos_disponibles)
        
        # Ordenamos los archivos priorizando archivos grandes.
        for archivo in sorted(archivos_disponibles, key=lambda x: archivos[x], reverse=True):
            if archivos[archivo] <= espacio_restante:
                subconjunto.add(archivo)
                espacio_restante -= archivos[archivo]
                print("\t Nuevo archivo", subconjunto, "Espacio restante:", espacio_restante)

        H.append(subconjunto)
        archivos_disponibles -= subconjunto
        print("Subconjunto creado:", subconjunto, "Espacio restante:", espacio_restante)

    return H

def generar_subconjuntos(tamaño_disco, nombres_archivos, tamaños_archivos):
    H = []
    archivos = list(zip(nombres_archivos, tamaños_archivos))

    for r in range(1, len(archivos) + 1):
        for combinacion in combinations_with_replacement(archivos, r):
            tamaño_combinacion = sum(tamaño for _, tamaño in combinacion)

            if tamaño_combinacion <= tamaño_disco and tamaño_disco:
                h = set([nombre for nombre, _ in combinacion])
                
                # for _, tamaño in combinacion:
                #     h[tamaño] = h.get(tamaño, 0) + 1
                
                if h not in H:
                    H.append(h)
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