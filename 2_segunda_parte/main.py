#!/usr/bin/env python3

import sys
from configuracion_2 import *
from generador_output_2 import *
from model_part_2 import *

if len(sys.argv) != 3:
    print(f"Uso: {sys.argv[0]} OPTION nombre_archivo")
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

capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos = leer_configuracion(f"{archivo}")

solucion = distribuir_archivos_2(capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos)
sys.stderr.write(f"[Debugging] [MODELO 2] Time: {solucion[1].getSolvingTime()}\n\n")

if solucion is not None:
    generar_output(f"{archivo[:-3]}.out", solucion)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")
