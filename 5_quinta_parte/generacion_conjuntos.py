import time
from collections import Counter
from itertools import combinations_with_replacement

# esta no la vamos a necesitar. hice esta y generar_subconjuntos para probar, y la otra es mejor
# la dejé por las dudas pero creo que no la vamos a usar
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


