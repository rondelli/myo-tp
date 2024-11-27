#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, "../1_primera_parte")
sys.path.insert(0, "../3_tercera_parte")
sys.path.insert(0, "../4_cuarta_parte")
sys.path.insert(0, "../5_quinta_parte")

import model_part_1
import model_part_3
import model_part_4
import model_part_5
from funciones import *

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
    _, modelo_1, _, _, _ = model_part_1.distribuir_archivos_1(d_t, F, s, threshold*60)
    modelo_4 = model_part_4.distribuir_archivos_4(d_t, F, s, 11, threshold*60)
    _, modelo_5, _, _, _  = model_part_5.obtener_conjuntos(a, threshold*60)
        
    caso = a
    cant = len(F)

    cota_dual_1, mejor_1, var_1, tiempo_1 = datos_modelo(modelo_1)
    cota_dual_4, mejor_4, var_4, tiempo_4 = datos_modelo(modelo_4)
    cota_dual_5, mejor_5, var_5, tiempo_5 = datos_modelo(modelo_5)

    cota_dual = max([cota_dual_1, cota_dual_4])

    guardar_prueba([[caso, cant, cota_dual, mejor_1, var_1, tiempo_1, mejor_4, var_4, tiempo_4, mejor_5, var_5, tiempo_5, 0, 0, 0]])
