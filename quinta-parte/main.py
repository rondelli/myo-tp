import sys
from configuracion_5 import *
from set_selector import *
from generador_output_5 import * 

if len(sys.argv) != 2:
    print(f"Uso: {sys.argv[0]} nombre_archivo")
    sys.exit(1)

archivo = sys.argv[1]
print(f"Utilizando {archivo}\n")

generar_configuracion(archivo)
capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{archivo}")
conjuntos = generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)

solucion = elegir_conjuntos(nombres_archivos, conjuntos)

if solucion is not None:
    generar_output(f"{archivo[:-3]}.out", solucion, conjuntos)
else:
    generar_output_fallido(f"{archivo[:-3]}.out")

#archivos = []
# for conjunto in conjuntos:
#     for archivo in conjunto:
#         if archivo not in archivos:
#             archivos.append(archivo)
# print(len(archivos) == len(nombres_archivos))