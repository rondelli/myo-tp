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
disks_capacity, file_names, file_sizes = leer_configuracion.leer_configuracion(f"./{file}")

print(f"Params:\n"
      f"Disks capacity: {disks_capacity} TB\n"
      f"Amount of disks: {len(file_names)}\n"
      f"Files: \n" + "\n".join([f"    {nombre}: {tamaño}" for nombre, tamaño in zip(file_names, file_sizes)]))
print()

big_data.distribuir_archivos(disks_capacity, file_names, file_sizes)
