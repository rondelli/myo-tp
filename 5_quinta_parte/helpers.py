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
                if not agregado:
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

    archivos.sort(key=lambda x: x[1], reverse=True)

    while archivos:
        subconjunto = set()
        espacio_restante = tamaño_disco

        for archivo in archivos[:]:
            if archivo[1] <= espacio_restante:
                subconjunto.add(archivo[0])
                espacio_restante -= archivo[1]
                archivos.remove(archivo)

        H.append(subconjunto)

    return H

def generar_subconjuntos_pares(tamaño_disco, nombres_archivos, tamaños_archivos):
    H = []
    archivos = list(zip(nombres_archivos, tamaños_archivos))

    mitad = len(archivos) // 2
    archivos1 = archivos[:mitad]
    archivos2 = archivos[mitad:]

    if len(archivos) % 2 == 1:
        archivos2.append(archivos[-1])
        
    for i in range(min(len(archivos1), len(archivos2))):
        subconjunto = {archivos1[i][0], archivos2[i][0]}
        total_size = archivos1[i][1] + archivos2[i][1]
        if total_size <= tamaño_disco:
            H.append(subconjunto)

    if len(archivos1) > len(archivos2):
        if archivos1[-1][1] <= tamaño_disco:
            H.append({archivos1[-1][0]})
    elif len(archivos2) > len(archivos1):
        if archivos2[-1][1] <= tamaño_disco:
            H.append({archivos2[-1][0]})

    return H


def generar_subconjuntos_tercios(tamaño_disco, nombres_archivos, tamaños_archivos):
    H = []
    archivos = list(zip(nombres_archivos, tamaños_archivos))

    tercio = len(archivos) // 3
    archivos1 = archivos[:tercio]
    archivos2 = archivos[tercio:2*tercio]
    archivos3 = archivos[2*tercio:]

    if len(archivos) % 3 == 1:
        archivos3.append(archivos[-1])
    elif len(archivos) % 3 == 2:
        archivos2.append(archivos[-2])
        archivos3.append(archivos[-1])

    for i in range(min(len(archivos1), len(archivos2), len(archivos3))):
        subconjunto = {archivos1[i][0], archivos2[i][0], archivos3[i][0]}
        total_size = archivos1[i][1] + archivos2[i][1] + archivos3[i][1]
        if total_size <= tamaño_disco:
            H.append(subconjunto)

    if len(archivos1) > len(archivos2):
        subconjunto = {archivos1[-1][0], archivos2[-1][0]}
        total_size = archivos1[-1][1] + archivos2[-1][1]
        if total_size <= tamaño_disco:
            H.append(subconjunto)
    elif len(archivos2) > len(archivos3):
        subconjunto = {archivos2[-1][0], archivos3[-1][0]}
        total_size = archivos2[-1][1] + archivos3[-1][1]
        if total_size <= tamaño_disco:
            H.append(subconjunto)
    elif len(archivos3) > len(archivos1):
        subconjunto = {archivos3[-1][0], archivos1[-1][0]}
        total_size = archivos3[-1][1] + archivos1[-1][1]
        if total_size <= tamaño_disco:
            H.append(subconjunto)

    if len(archivos1) > len(archivos2) and len(archivos1) > len(archivos3):
        if archivos1[-1][1] <= tamaño_disco:
            H.append({archivos1[-1][0]})
    elif len(archivos2) > len(archivos1) and len(archivos2) > len(archivos3):
        if archivos2[-1][1] <= tamaño_disco:
            H.append({archivos2[-1][0]})
    elif len(archivos3) > len(archivos1) and len(archivos3) > len(archivos2):
        if archivos3[-1][1] <= tamaño_disco:
            H.append({archivos3[-1][0]})

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