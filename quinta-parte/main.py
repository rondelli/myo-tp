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

#generar_configuracion(archivo)
capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{archivo}")

#capacidad_disco = 2
#nombres_archivos = ["a1", "a2", "a3"]
#tamaños_archivos = [7392401, 8543009, 2383278]
conjuntos = generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)


F = ["archivo1", "archivo2", "archivo3"] 
H = [ {"archivo1", "archivo2"}, {"archivo2", "archivo3"}, {"archivo1", "archivo3"}]

solucion_P = elegir_conjuntos(nombres_archivos, conjuntos)
#solucion_D = importancia_archivos(nombres_archivos, conjuntos)

#solucion = distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, solucion_D)

if solucion_P is not None:
    generar_output(f"{archivo[:-3]}.out", solucion_P, conjuntos)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")

#archivos = []
# for conjunto in conjuntos:
#     for archivo in conjunto:
#         if archivo not in archivos:
#             archivos.append(archivo)
# print(len(archivos) == len(nombres_archivos))
