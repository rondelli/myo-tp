#!/usr/bin/env python3

import sys
import time

from configuracion_6 import *
from generador_output_6 import * 
import model_part_6

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

tiempo_inicio = time.time()
datos = model_part_6.obtener_conjuntos(archivo, 7)
tiempo_tardado = time.time() - tiempo_inicio

if datos is not None:
    print(f"Tiempo de ejecución: {datos[-1]} segundos")
    print(f"Solución: {datos[0]}")
else:
    print("No se encontró solución")
print(f"Tiempo de ejecución: {tiempo_tardado}")
