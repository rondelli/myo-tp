#!/usr/bin/env python3

import sys
from configuracion_3 import *
from generador_output_3 import *
from set_selector import *

if len(sys.argv) != 4:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]
num_archivos = int(sys.argv[2]) # esto esta bien o deberian ser aleatorios tambien?
num_conjuntos = int(sys.argv[3])
print(f"Utilizando {archivo}\n")


generar_configuracion(archivo, num_archivos, num_conjuntos)
archivos, conjuntos = leer_configuracion(f"./{archivo}")
print(archivos)
print(conjuntos)
"""
solucion = elegir_conjuntos(conjuntos)

if solucion is not None:
    generar_output(f"{archivo[:-3]}.out", solucion)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")
"""