import os
import sys
import time
from pyscipopt import SCIP_PARAMSETTING

sys.path.insert(0, "../2_segunda_parte")
sys.path.insert(0, "../3_tercera_parte")
sys.path.insert(0, "../utils")

import model_aux
import inputs
import outputs
import model_part_2
import model_part_3

########################################################################
#   El threshold es en segundos
########################################################################

def obtener_conjuntos(ruta_archivo, threshold: int = float('inf')) -> None:
    capacidad_disco, nombres_archivos, tamaños_archivos = inputs.leer_input_5(ruta_archivo)

    tiempo_inicio = time.time()

    # aca estaba el random!!!
    # conjuntos = generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos) 

    # Hice un modelo que distribuye los archivos en distintos conjuntos
    conjuntos = model_aux.generar_conjuntos(capacidad_disco, nombres_archivos, tamaños_archivos, threshold)
    encontro_solucion = True
    termino_tiempo = False
    modelo = None
    
    while True:
        inicio_ciclo = time.time()
        tiempo = inicio_ciclo - tiempo_inicio
        if tiempo >= threshold or conjuntos is None:
            termino_tiempo = True
            break
        
        modelo = model_part_3.crear_modelo_3(nombres_archivos, conjuntos, threshold - tiempo)

        x, _ = model_part_3.obtener_solucion_primal_3(modelo)
        y, _ = model_part_3.obtener_solucion_dual_3(modelo)

        distribucion = model_part_2.distribuir_archivos_2(capacidad_disco, nombres_archivos, tamaños_archivos, y, threshold - tiempo)
        solucion_modelo_2 = outputs.obtener_solucion_2(distribucion)

        if solucion_modelo_2 is None or x is None:
            encontro_solucion = False
            break
        elif sum(solucion_modelo_2[1]) > 1:
            conjuntos.append(set(solucion_modelo_2[0]))
        else:
            encontro_solucion = True
            break
    
    tiempo = time.time() - tiempo_inicio

    if (encontro_solucion or termino_tiempo) and modelo is not None: # en caso de que termine el tiempo, x sería factible, no óptima (creo)
        soluc_entera = model_aux.obtener_solucion_entera(modelo, x)
        conjuntos_seleccionados = model_aux.obtener_conjuntos_seleccionados(soluc_entera)
        return [conjuntos_seleccionados, modelo, conjuntos, nombres_archivos, tamaños_archivos, tiempo]
    return None