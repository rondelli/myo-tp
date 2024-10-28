#!/usr/bin/env python3

from pyscipopt import Model, quicksum
import sys
from configuracion_4 import *
from generador_output_4 import *
from model import *

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} input_file_name_to_generate")
    sys.exit(1)

input_file_name = sys.argv[1]
print(f"Input file name to generate: {input_file_name}\n")

escribir_configuracion(input_file_name)

disk_size, file_names_with_sizes, file_sizes = leer_configuracion(f"./{input_file_name}")

print(f"d: {disk_size}\nnames: {file_names}\nsizes: {file_sizes}")

solution = distribuir_archivos(disk_size, file_names_with_sizes, file_sizes)

if solution is not None:
    generar_output(f"{input_file_name[:-3]}.out", solution)
else:
    generar_output_fallido(f"{input_file_name[:-3]}.out")
