#!/usr/bin/env python3

import sys
from configuracion_5 import *
from set_selector import *
from generador_output_5 import * 
from importance import *

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]
print(f"Utilizando {archivo}\n")

generar_configuracion(archivo)
capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{archivo}")

conjuntos = generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)

solucion_dual = elegir_conjuntos(nombres_archivos, conjuntos)
#solucion_D = importancia_archivos(nombres_archivos, conjuntos)

#solucion = distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, solucion_D)

if solucion_dual is not None:
    generar_output(f"{archivo[:-3]}.out", solucion_dual, conjuntos)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")

#archivos = []
# for conjunto in conjuntos:
#     for archivo in conjunto:
#         if archivo not in archivos:
#             archivos.append(archivo)
# print(len(archivos) == len(nombres_archivos))
