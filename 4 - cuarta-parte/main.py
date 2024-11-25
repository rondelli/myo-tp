#!/usr/bin/env python3

from pyscipopt import Model, quicksum
import sys
from configuracion_4 import *
from generador_output_4 import *
from model import *

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]
print(f"Utilizando {archivo}\n")

# generar_configuracion(archivo)

capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{archivo}")

max_cant_tamaños = 11
solucion = distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, max_cant_tamaños)

if solucion is not None:
    generar_output(f"{archivo[:-3]}.out", solucion)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")
