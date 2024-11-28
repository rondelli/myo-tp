#!/usr/bin/env python3

import sys

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

datos = model_part_6.obtener_conjuntos(archivo, 7)
