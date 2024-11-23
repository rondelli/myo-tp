import sys
from configuracion_5 import *
from set_selector import *

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]
print(f"Utilizando {archivo}\n")

generar_configuracion(archivo)
capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{archivo}")

conjuntos = generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)

# cant = 0
# archivos = []

# for conjunto in conjuntos:
#     for archivo in conjunto:
#         if archivo not in archivos:
#             archivos.append(archivo)
#             cant += 1
# print(cant == len(nombres_archivos))