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

def generar_subconjuntos_prueba(tamaño_disco, nombres_archivos, tamaños_archivos):
    H = []
    archivos = list(zip(nombres_archivos, tamaños_archivos))
    archivos.sort(key=lambda x: x[1], reverse=True)

    archivo_menor = archivos[len(archivos) - 1]

    # Tratar de combinar el mínimo con otros archivos.
    for archivo in archivos:

        # No entra con el mínimo. No entra con ninguno.
        if archivo_menor[1] + archivo[1] > tamaño_disco:
            H.append({archivo[0]})

        # Entra en el subconjunto.
        else:
            H.append({archivo_menor[0], archivo[0]})

    return H

def generar_subconjuntos_pares(tamaño_disco, nombres_archivos, tamaños_archivos):
    H = []
    archivos = list(zip(nombres_archivos, tamaños_archivos))

    archivos.sort(key=lambda x: x[1], reverse=False)

    for i in range(len(archivos)):
        archivo_actual = archivos[i]

        # Encontrar el mayor archivo restante que pueda combinarse con el archivo actual
        for j in range(len(archivos) - 1, 0, -1):
            archivo_max = archivos[j]

            if archivo_actual[1] + archivo_max[1] <= tamaño_disco:
                H.append({archivo_actual[0], archivo_max[0]})
                break
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