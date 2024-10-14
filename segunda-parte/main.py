#!/usr/bin/env python3

import sys
from configuracion_2 import *
from importance import *

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]
print(f"Utilizando {archivo}\n")

generar_configuracion(archivo)
capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos = leer_configuracion(f"./{archivo}")

print(f"Params:\n"
      f"Disks capacity: {capacidad_disco} TB\n"
      f"Amount of disks: {len(nombres_archivos)}\n"
      f"Files: \n" + "\n".join([f"    {nombre}: {tamaño}, {importancia}" for nombre, tamaño, importancia in zip(nombres_archivos, tamaños_archivos, importancia_archivos)]))
print()

distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos)

