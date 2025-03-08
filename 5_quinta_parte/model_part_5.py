import sys
import time

sys.path.insert(0, "../2_segunda_parte")
sys.path.insert(0, "../3_tercera_parte")
sys.path.insert(0, "../utils")

# import generacion_conjuntos
import helpers
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

    print("PASO 1")
    # 1) Obtener H cursiva.
    conjuntos = helpers.generar_subconjuntos_5(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)
    if conjuntos is None:
        return None

    while True:
        tiempo = time.time() - tiempo_inicio
        if not helpers.hay_tiempo(tiempo_inicio, threshold):
            print("TIEMPO")
            termino_tiempo = True
            break

        print("PASO 2")
        # 2) Plantear un modelo como el de seccion 3 pero relajado --> lo denominamos P.
        modelo_P = model_part_3.crear_modelo_3(nombres_archivos, conjuntos, threshold - tiempo)
        # 2.1) Obtenemos la solución de P.
        x, _ = model_part_3.obtener_solucion_primal_3(modelo_P)
        if x is None:
            encontro_solucion = False
            break

        if not helpers.hay_tiempo(tiempo_inicio, threshold):
            print("TIEMPO")
            termino_tiempo = True
            break

        print("PASO 3")
        # 3) Obtener una solucion y* del dual de P --> y* le asigna un valor a cada archivo.
        y, _ = model_part_3.obtener_solucion_dual_3(modelo_P)

        print("PASO 4")
        # 4) Resolver el problema de la seccion 2 --> El indicador de importancia I_f de cada archivo f viene dado por el valor dual y*_f 
        # --> Obtenemos un conjunto de maxima importancia H.
        distribucion = model_part_2.distribuir_archivos_2(capacidad_disco, nombres_archivos, tamaños_archivos, y, threshold - tiempo) # [F, model, fake_x, I, s]
        solucion_modelo_2 = outputs.obtener_solucion_2(distribucion)
        
        if not helpers.hay_tiempo(tiempo_inicio, threshold):
            print("TIEMPO")
            termino_tiempo = True
            break

        if solucion_modelo_2 is None:
            encontro_solucion = False
            break
        # 5) Si la funcion objetivo del paso anterior es > 1, agregamos H a H cursiva y volvemos al paso 3.
        if sum(solucion_modelo_2[1]) > 1:
            print("PASO 5")
            existe_subconjunto = False
            for subconjunto in conjuntos:
                if set(solucion_modelo_2[0]).issubset(set(subconjunto)):
                    existe_subconjunto = True
                    break

            if not existe_subconjunto:
                conjuntos.append(set(solucion_modelo_2[0]))
            else:
                break
        else:
            break
    
    tiempo = time.time() - tiempo_inicio
    
    if encontro_solucion or termino_tiempo: # Retorna la solucion optima o, en caso de que se haya terminado el tiempo, la ultima solucion factible encontrada
        soluc_entera = helpers.obtener_solucion_entera(modelo_P, x)
        conjuntos_seleccionados = helpers.obtener_conjuntos_seleccionados(soluc_entera)
        return [conjuntos_seleccionados, modelo_P, conjuntos, nombres_archivos, tamaños_archivos, tiempo]
    return None