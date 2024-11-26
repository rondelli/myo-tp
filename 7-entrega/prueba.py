#!/usr/bin/env python3

from funciones import *
import glob

# 1 - leer config
configuraciones = leer_configuracion()
print(configuraciones)

inPath = configuraciones.get('inPath')
outPath = configuraciones.get('outPath')
threshold = int(configuraciones.get('threshold', 0))

archivos = os.listdir(inPath)
archivos = [f for f in archivos if os.path.isfile(f)]

# Imprimir los nombres de los archivos
#for archivo in archivos:
    # for model in models:
    #   x = obtener_solucion_entera(model)
    #   guardar_prueba(...)


# 2 - para todo archivo dentro del directorio, ejecutar los 4 modelos

# 3 - OJO CON LA COTA generar csv

