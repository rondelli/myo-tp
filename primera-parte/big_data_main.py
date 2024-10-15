#!/usr/bin/env python3
import sys
from configuracion_1 import *
from generardor_output_1 import *
from big_data import *

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]
print(f"Utilizando {archivo}\n")

generar_configuracion(archivo)
capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{archivo}")

solucion = distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos)
if solucion is not None:
    generar_output(f"{archivo[:-3]}.out", solucion)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")
