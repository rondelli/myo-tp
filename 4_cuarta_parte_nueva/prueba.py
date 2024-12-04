#!/usr/bin/env python3

import sys
from configuracion_4 import *
import model_part_4
import Pattern

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]

archivo = sys.argv[1]
# archivo = "f0018.in"

print(f"Utilizando {archivo}\n")

capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"{archivo}")

ordenamiento = sorted(list(zip(tamaños_archivos, nombres_archivos)), reverse=True)
file_sizes, F = zip(*ordenamiento)
F = list(F)

S = {size: file_sizes.count(size) for size in set(file_sizes)}
S = dict(sorted(S.items(), reverse=True))

file_sizes_2 = [key * S[key] for key in S]

patrones = Pattern.Pattern(capacidad_disco * 10**6, file_sizes_2)
patrones = patrones.obtener_patrones()

model_part_4.distribuir_archivos_4(capacidad_disco, nombres_archivos, tamaños_archivos, patrones, 1)


