#!/usr/bin/env python3

from funciones import *
import sys
import os

sys.path.insert(0, "./1-primera-parte")
import model_part_1

# 1 - leer config
configuraciones = leer_configuracion()
print(">>>", configuraciones)

inPath = configuraciones.get('inPath')
outPath = configuraciones.get('outPath')
threshold = int(configuraciones.get('threshold', 0))

archivos = os.listdir(inPath)
archivos = [f for f in archivos]

print(archivos)

for archivo in archivos:
    print(archivo)
    d_t, F, s = leer_archivo(archivo)
    modelo_1 = model_part_1.crear_modelo_1(d_t, F, s, threshold*60)
        
    caso = archivo
    cota_dual = "?"
    cant = len(F)

    mejor_1, var_1, tiempo_1 = datos_modelo(modelo_1)
    # mejor_4, var_4, tiempo_4 = datos_modelo(modelo_4)
    # mejor_5, var_5, tiempo_5 = datos_modelo(modelo_5)
    # mejor_6, var_6, tiempo_6 = datos_modelo(modelo_6)

    # guardar_prueba([[caso, cant, cota_dual, mejor_1, var_1, tiempo_1, mejor_4, var_4, tiempo_4, mejor_5, var_5, tiempo_5, mejor_6, var_6, tiempo_6]])
    guardar_prueba([[caso, cant, cota_dual, mejor_1, var_1, tiempo_1, mejor_1, var_1, tiempo_1, mejor_1, var_1, tiempo_1, mejor_1, var_1, tiempo_1]])

# 3 - OJO CON LA COTA generar csv