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
    encontro_solucion = True
    termino_tiempo = False
    modelo_P = None

    tiempo_inicio = time.time()

    # 1) Obtener H cursiva.
    # * Este paso puede llegar a retornar soluciones ya optimas --> el while de abajo pareciera "entorpecer" el asunto, ya que
    # hace que algunos archivos aparezcan en más de un disco.
    # * Este paso lleva mucho tiempo, tanto que practicamente consume los 7' --> el limite de este paso termina siendo el limite de todo el modelo 5.
    # --> otra opción puede ser hacer un algoritmo y listo, pero no sé si es a lo que apunta el profe :s
    conjuntos = model_aux.generar_conjuntos(capacidad_disco, nombres_archivos, tamaños_archivos, threshold)
    print("CONJUNTOS:", conjuntos)
    if conjuntos is None:
        return None
    
    while True:
        tiempo = time.time() - tiempo_inicio
        if tiempo >= threshold:
            termino_tiempo = True
            break
        
        # 2) Plantear un modelo como el de seccion 3 pero relajado --> lo denominamos P.
        modelo_P = model_part_3.crear_modelo_3(nombres_archivos, conjuntos, threshold - tiempo)

        # 2.1) Obtenemos la solución de P.
        x, _ = model_part_3.obtener_solucion_primal_3(modelo_P)

        # 3) Obtener una solucion y* del dual de P --> y* le asigna un valor a cada archivo.
        y, _ = model_part_3.obtener_solucion_dual_3(modelo_P)

        # 4) Resolver el problema de la seccion 2 --> El indicador de importancia I_f de cada archivo f viene dado por el valor dual y*_f 
        # --> Obtenemos un conjunto de maxima importancia H.
        distribucion = model_part_2.distribuir_archivos_2(capacidad_disco, nombres_archivos, tamaños_archivos, y, threshold - tiempo) # [F, model, fake_x, I, s]
        solucion_modelo_2 = outputs.obtener_solucion_2(distribucion)

        if solucion_modelo_2 is None or x is None or modelo_P is None:
            encontro_solucion = False
            break

        # 5) Si la funcion objetivo del paso anterior es > 1, agregamos H a H cursiva y volvemos al paso 3.
        elif sum(solucion_modelo_2[1]) > 1:
            conjuntos.append(set(solucion_modelo_2[0]))
        else:
            print("CONJUNTOS RESULTADO:", conjuntos)
            # encontro_solucion = True
            break
    
    tiempo = time.time() - tiempo_inicio

    # print("X:", x, "\nY*:", y, "\nDistribucion:", distribucion,"\nSolucion modelo 2:", solucion_modelo_2, "\nConjuntos", conjuntos, "\n")
    
    if encontro_solucion or termino_tiempo: # en caso de que termine el tiempo, x sería factible, no óptima (creo)
        soluc_entera = model_aux.obtener_solucion_entera(modelo_P, x)
        conjuntos_seleccionados = model_aux.obtener_conjuntos_seleccionados(soluc_entera)
        # print("\nSolucion entera: ", soluc_entera, "\nConjuntos seleccionados: ", conjuntos_seleccionados, "\n")
        return [conjuntos_seleccionados, modelo_P, conjuntos, nombres_archivos, tamaños_archivos, tiempo]
    return None