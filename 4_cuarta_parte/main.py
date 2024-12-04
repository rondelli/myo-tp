#!/usr/bin/env python3

import sys
from configuracion_4 import *
import model_part_4
import Pattern
from generador_output_4 import *

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]

print(f"Utilizando {archivo}\n")

capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"{archivo}")

ordenamiento = sorted(list(zip(tamaños_archivos, nombres_archivos)), reverse=True)
tamaños_archivos, nombres_archivos = zip(*ordenamiento)

solution = model_part_4.distribuir_archivos_4(capacidad_disco, list(nombres_archivos), list(tamaños_archivos), 1)

if solution is not None:
    generar_output(f"{archivo[:-3]}.out", solution)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")