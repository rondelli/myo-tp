#!/usr/bin/env python3

import sys
from configuracion_4 import *
import Pattern

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]

archivo = sys.argv[1]
# archivo = "f0018.in"

print(f"Utilizando {archivo}\n")

capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"{archivo}")

patrones = Pattern.Pattern(capacidad_disco * 10**6, tamaños_archivos)

print(patrones.obtener_patrones())
