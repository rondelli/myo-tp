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

    # Dividir la lista de nombres de archivos en tres partes
    tercio = len(nombres_archivos) // 3
    nombres1 = nombres_archivos[:tercio]
    nombres2 = nombres_archivos[tercio:2*tercio]
    nombres3 = nombres_archivos[2*tercio:]

    # Si la longitud de nombres_archivos no es divisible por 3, manejar los elementos restantes
    if len(nombres_archivos) % 3 == 1:
        nombres3.append(nombres_archivos[-1])
    elif len(nombres_archivos) % 3 == 2:
        nombres2.append(nombres_archivos[-2])
        nombres3.append(nombres_archivos[-1])

    # Crear subconjuntos de tres elementos
    for i in range(min(len(nombres1), len(nombres2), len(nombres3))):
        H.append({nombres1[i], nombres2[i], nombres3[i]})

    # Crear subconjuntos de dos elementos si hay elementos restantes
    if len(nombres1) > len(nombres2):
        H.append({nombres1[-1], nombres2[-1]})
    elif len(nombres2) > len(nombres3):
        H.append({nombres2[-1], nombres3[-1]})
    elif len(nombres3) > len(nombres1):
        H.append({nombres3[-1], nombres1[-1]})

    # Crear subconjuntos de un elemento si hay un elemento restante
    if len(nombres1) > len(nombres2) and len(nombres1) > len(nombres3):
        H.append({nombres1[-1]})
    elif len(nombres2) > len(nombres1) and len(nombres2) > len(nombres3):
        H.append({nombres2[-1]})
    elif len(nombres3) > len(nombres1) and len(nombres3) > len(nombres2):
        H.append({nombres3[-1]})

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