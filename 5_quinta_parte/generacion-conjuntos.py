from collections import Counter
from itertools import combinations_with_replacement

def generar_subconjuntos_peor(tamaño_disco, archivos):
    # no recuerdo si ya hicimos algo así...
    # esto repite patrones, por ahora
    # sorry por los nombres de las variables
    
    patrones = []
    
    for tamaño_archivo, _ in archivos.items():
        tamaño_disco_actual = tamaño_disco
        patron = {}
        
        espacio_restante_patron = tamaño_disco_actual - tamaño_archivo
        patron[tamaño_archivo] = 1
        
        for tamaño_archivo_2, cantidad_archivos_2 in archivos.items():
            cantidad_utilizados = cantidad_archivos_2 - (1 if tamaño_archivo == tamaño_archivo_2 else 0)
            espacio_restante = espacio_restante_patron - (tamaño_archivo_2 * cantidad_utilizados)

            while espacio_restante < 0 and cantidad_utilizados > 0:
                cantidad_utilizados = cantidad_utilizados - 1
                espacio_restante = espacio_restante_patron - (tamaño_archivo_2 * cantidad_utilizados)
            
            patron[tamaño_archivo_2] = patron.get(tamaño_archivo_2, 0) + cantidad_utilizados
            espacio_restante_patron = espacio_restante
        
        patrones.append(patron)

    return patrones

# otra opción
def generar_subconjuntos(tamaño_disco, archivos):
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

# FUNCION DE AGUS
def generar_subconjuntos_Agus(peso_disco, nombres_archivos, pesos_archivos, tiempo_inicio, tiempo_limite_total):
            H = []
            archivos = list(zip(nombres_archivos, pesos_archivos))
            print ("Generando subconjuntos")
            if not chequear_existe_tiempo_ejecucion(tiempo_inicio, tiempo_limite_total):
                print("Se terminó el tiempo generando los conjuntos.")
                return None
            # También generamos subconjuntos de archivos de forma más interdependiente para agregar variedad
            for i in range(len(archivos)):
                for j in range(i + 1, len(archivos)):
                    # Intentamos agregar combinaciones de diferentes pares de archivos
                    combo = [archivos[i], archivos[j]]
                    total_size = sum(peso for _, peso in combo)
                    if not chequear_existe_tiempo_ejecucion(tiempo_inicio, tiempo_limite_total):
                        print("Se terminó el tiempo generando los subconjuntos.")
                        return []
                    if total_size <= peso_disco:
                        H.append([nombre for nombre, _ in combo])
            if not chequear_existe_tiempo_ejecucion(tiempo_inicio, tiempo_limite_total):
                        print("Se terminó el tiempo generando los subconjuntos.")
                        return []
            print ("Termino de generar subconjuntos")
            return H

def chequear_existe_tiempo_ejecucion(tiempo_inicio, tiempo_limite):
    return True

archivos = {'a1': 20, 'a2': 13, 'a3': 20, 'a4': 15, 'a5': 30, 'a6': 15, 'a7': 15}
tamaños_cantidades = dict(Counter(archivos.values()))

print(f"Tamaños y cantidades {tamaños_cantidades}")

tamaño_discos = 50

patrones_1 = generar_subconjuntos_peor(tamaño_discos, tamaños_cantidades)
patrones_2 = generar_subconjuntos(tamaño_discos, archivos)
patrones_agus = generar_subconjuntos_Agus(tamaño_discos, list(archivos.keys()), list(archivos.values()), 0, 0)

print(f"Output primer función {patrones_1}")
print(f"Output segunda función {patrones_2}")
print(f"Output agus {patrones_agus}")







