#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, "./1_primera_parte")
sys.path.insert(0, "./4_cuarta_parte")
sys.path.insert(0, "./5_quinta_parte")
sys.path.insert(0, "./6_sexta_parte")

import model_part_1
import model_part_4
#import model_part_5
#import model_part_6

from funciones import *

# 1 - leer config
configuraciones = leer_configuracion()

sys.stderr.write(f"[Debugging] {configuraciones}\n")

inPath = configuraciones.get('inPath')
outPath = configuraciones.get('outPath')
threshold = int(configuraciones.get('threshold', 0))

archivos = os.listdir(inPath)
archivos = [f for f in archivos]

sys.stderr.write(f"[Debugging] {archivos}\n")

# prueba de modelos
for a in archivos:
    sys.stderr.write(f"[Debugging] {a}\n")
    d_t, F, s = leer_archivo(a)
    modelo_1 = model_part_1.crear_modelo_1(d_t, F, s, threshold*60)
    modelo_4 = model_part_4.distribuir_archivos_4(d_t, F, s, 11, threshold*60)
    #modelo_5 = model_part_3.crear_modelo_5(d_t, F, s, threshold*60)
    #modelo_6 = model_part_4.crear_modelo_6(d_t, F, s, threshold*60)
        
    caso = a
    cant = len(F)

    cota_dual_1, mejor_1, var_1, tiempo_1 = datos_modelo(modelo_1)
    cota_dual_4, mejor_4, var_4, tiempo_4 = datos_modelo(modelo_4)
    # cota_dual_5, mejor_5, var_5, tiempo_5 = datos_modelo(modelo_5)
    # cota_dual_6, mejor_6, var_6, tiempo_6 = datos_modelo(modelo_6)

    cota_dual = max([cota_dual_1, cota_dual_4])

    # guardar_prueba([[caso, cant, cota_dual, mejor_1, var_1, tiempo_1, mejor_4, var_4, tiempo_4, mejor_5, var_5, tiempo_5, mejor_6, var_6, tiempo_6]])
    guardar_prueba([[caso, cant, cota_dual, mejor_1, var_1, tiempo_1, mejor_4, var_4, tiempo_4, 0, 0, 0, 0, 0, 0]])
