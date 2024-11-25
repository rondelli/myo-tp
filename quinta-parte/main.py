#!/usr/bin/env python3

import sys
from configuracion_5 import *
from set_selector import *
from generador_output_5 import * 
from importance import *

if len(sys.argv) != 3:
    print(f"Uso: {sys.argv[0]} OPTION nombre_archivo\n")
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

capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{archivo}")

# PASO 1
conjuntos = generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)

while True:
    # PASO 2 Y 3: y*
    modelo = crear_modelo(nombres_archivos, conjuntos)
    
    # El orden de estas dos líneas no importa: x, y ó y, x es lo mismo
    x, obj_x = obtener_solucion_primal(modelo)
    y, obj_y = obtener_solucion_dual(modelo)

    print("[Debugging] obj x\n", obj_x)
    print("[Debugging] obj y\n", obj_y)

    # print("[Debugging] x\n", x)
    optimo = es_optimo(modelo, x)
    print(f"[Debugging] es óptimo: {optimo}")

    # PASO 4
    distribucion = distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, y)
    solucion_modelo_2 = generar_output_modelo_2(distribucion)

    # PASO 5
    # copy_of_model = Model(sourceModel=modelo_3)

    if sum(solucion_modelo_2[1]) > 1:
        conjuntos.append(set(solucion_modelo_2[0]))
        break
    else:
        break

# x_estrella_int = pasar_a_entero(x* real)
# print(y)
# okay = es_optimo(modelo, x_estrella_int)

'''
if solucion_dual is not None:
    generar_output(f"{archivo[:-3]}.out", solucion_dual, conjuntos)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")
'''
#archivos = []
# for conjunto in conjuntos:
#     for archivo in conjunto:
#         if archivo not in archivos:
#             archivos.append(archivo)
# print(len(archivos) == len(nombres_archivos))
