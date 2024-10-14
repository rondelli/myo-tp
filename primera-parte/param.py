#!/usr/bin/env python3

import sys
from configuracion import generador_configuracion
from configuracion import leer_configuracion
import big_data

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} filename")
    sys.exit(1)

file = sys.argv[1]
print(f"Using {file}\n")

generador_configuracion.generar_configuracion(sys.argv[1])
capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion.leer_configuracion(f"./{file}")

print(f"Params:\n"
      f"Disks capacity: {capacidad_disco} TB\n"
      f"Amount of disks: {len(nombres_archivos)}\n"
      f"Files: \n" + "\n".join([f"    {nombre}: {tamaño}" for nombre, tamaño in zip(nombres_archivos, tamaños_archivos)]))
print()

big_data.distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos)
