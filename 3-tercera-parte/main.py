#!/usr/bin/env python3

import sys
from configuracion_3 import *
from generador_output_3 import *
from set_selector import *

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]
#num_archivos = int(sys.argv[2])
#num_conjuntos = int(sys.argv[3])
print(f"Utilizando {archivo}\n")

generar_configuracion(archivo)
archivos, conjuntos = leer_configuracion(f"./{archivo}")

solucion = elegir_conjuntos(archivos, conjuntos)

if solucion is not None:
    generar_output(f"{archivo[:-3]}.out", solucion, conjuntos)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")
