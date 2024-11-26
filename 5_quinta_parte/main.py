#!/usr/bin/env python3

import sys

from typing import Optional
from configuracion_5 import *
from set_selector import *
from generador_output_5 import * 
#from importance import *

sys.path.insert(0, "../1-primera-parte")
sys.path.insert(0, "../2-segunda-parte")
sys.path.insert(0, "../3-segunda-parte")
sys.path.insert(0, "../4-segunda-parte")
from model_part_1 import *
from model_part_2 import *

import time

#if len(sys.argv) != 4:
if len(sys.argv) != 3:
    print(f"Uso: {sys.argv[0]} OPTION nombre_archivo minutos\n")
    print(f"      OPTIONS: -g | -u")
    print(f"      -g generar archivo")
    print(f"      -u usar archivo ya generado")
    sys.exit(1)

archivo = sys.argv[2]

if sys.argv[1] == "-g":
    print(f"Generando {archivo}\n")
    generar_configuracion(archivo)

if sys.argv[1] == "-u":
    print(f"Usando {archivo}\n")

# try:
#     minutos = float(sys.argv[3])
# except ValueError:
#     print("Ingresa un número válido para los minutos.")
#     sys.exit(1)

def obtener_conjuntos(archivo, threshold: int = float('inf')) -> None:
    capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{archivo}")

    # PASO 1
    conjuntos = generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)

    duracion = threshold * 60
    tiempo_inicio = time.time()

    while True:
        # PASO 2 Y 3: y*
        modelo = crear_modelo(nombres_archivos, conjuntos)
        
        x, obj_x = obtener_solucion_primal(modelo)
        y, obj_y = obtener_solucion_dual(modelo)

        sys.stderr.write(f"[Debugging] obj x {obj_x}\n")
        sys.stderr.write(f"[Debugging] obj y {obj_y}\n")

        optimo = es_optimo(modelo, x)
        sys.stderr.write(f"[Debugging] es óptimo: {optimo}")

        # PASO 4
        distribucion = distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, y)
        solucion_modelo_2 = generar_output_modelo_2(distribucion)

        # PASO 5
        # copy_of_model = Model(sourceModel=modelo_3)
        if sum(solucion_modelo_2[1]) > 1 and time.time() - tiempo_inicio <= duracion:
            conjuntos.append(set(solucion_modelo_2[0]))
            break # una pasada
        else:
            break
    x_estrella_int = obtener_solucion_entera(modelo, x) 
    return x_estrella_int

"""
conjuntos_seleccionados = obtener_conjuntos_seleccionados(x_estrella_int)

if conjuntos_seleccionados is not None:
    generar_output(f"{archivo[:-3]}.out", conjuntos_seleccionados, conjuntos)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")
"""