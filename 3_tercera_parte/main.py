#!/usr/bin/env python3

import sys
from configuracion_3 import *
from generador_output_3 import *
from model_part_3 import *

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
    
archivos, conjuntos = leer_configuracion(f"./{archivo}")

solucion = elegir_conjuntos(archivos, conjuntos)

if solucion is not None:
    generar_output(f"{archivo[:-3]}.out", solucion, conjuntos)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")
