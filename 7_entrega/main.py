#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, "../1_primera_parte")
sys.path.insert(0, "../2_segunda_parte")
sys.path.insert(0, "../3_tercera_parte")
sys.path.insert(0, "../2_segunda_parte")
sys.path.insert(0, "../4_cuarta_parte")
sys.path.insert(0, "../5_quinta_parte")
sys.path.insert(0, "../6_sexta_parte")

import model_part_1
# import model_part_2
# import model_part_3
import model_part_4
import model_part_5
import model_part_6

from funciones import *

import output_1
import output_4
import output_5
import output_6

configuraciones = leer_configuracion()

sys.stderr.write(f"[Debugging] {configuraciones}\n")

inPath = configuraciones.get('inPath')
outPath = configuraciones.get('outPath')[:-1]
threshold = int(configuraciones.get('threshold', 0))

archivos = os.listdir(inPath)
archivos = [f for f in archivos]
sys.stderr.write(f"[Debugging] {archivos}\n")

# prueba de modelos
for a in archivos:
# a = archivos[0]
    sys.stderr.write(f"[Debugging] {a}\n")
    d_t, F, s = leer_archivo(a)

    cota_dual_1 = 98237428978
    cota_dual_4 = 98237428978
    cota_dual_5 = 98237428978
    cota_dual_6 = 98237428978

    mejor_1 = "inf"
    var_1 = "variable1"
    tiempo_1 = 480
    mejor_4 = "inf"
    var_4 = "variable4"
    tiempo_4 = 480
    mejor_5 = "inf"
    var_5 = 480
    tiempo_5 = 480
    mejor_6 = "inf"
    var_6 = 480
    tiempo_6 = 480

    # datos = model_part_1.distribuir_archivos_1(d_t, F, s, threshold * 60)
    # if datos is not None:
    #     cota_dual_1, mejor_1, var_1, tiempo_1 = datos_modelo(datos[1])
    #     output_1.generar_output(outPath, a + "_file.out", datos)
    # else:
    #     output_1.generar_output_fallido(outPath, a + "_file.out")

    # modelo_4 = model_part_4.distribuir_archivos_4(d_t, F, s, 11, threshold * 60)
    # if modelo_4 is not None:
    #     cota_dual_4, mejor_4, var_4, tiempo_4 = datos_modelo(modelo_4[1])
    #     output_4.generar_output(outPath, a + "_file.out", modelo_4)
    # else:
    #     output_4.generar_output_fallido(outPath, a + "_file.out")

    data_5  = model_part_5.obtener_conjuntos(a, threshold * 60)
    if data_5 is not None:
        conjuntos_seleccionados_5 = data_5[0]
        mejor_5 = len(conjuntos_seleccionados_5)
        modelo_5 = data_5[1]
        conjuntos_5 = data_5[2]
        cota_dual_5, _, var_5, _ = datos_modelo(modelo_5)
        tiempo_5 = data_5[3]
        output_5.generar_output(outPath, a + "_file.out", conjuntos_seleccionados_5, conjuntos_5)
    else:
        output_5.generar_output_fallido(outPath, a + "_file.out")

    data_6  = model_part_6.obtener_conjuntos(a, threshold * 60)
    if data_6 is not None:
        conjuntos_seleccionados_6 = data_6[0]
        mejor_6 = len(conjuntos_seleccionados_6)
        modelo_6 = data_6[1]
        conjuntos_6 = data_6[2]
        cota_dual_6, _, var_6, _ = datos_modelo(modelo_6)
        tiempo_6 = data_6[3]
        output_6.generar_output(outPath, a + "_file.out", conjuntos_seleccionados_6, conjuntos_6)
    else:
        output_6.generar_output_fallido(outPath, a + "_file.out")

    caso = a
    cant = len(F)

    cotas = [cota_dual_1, cota_dual_4, cota_dual_5, cota_dual_6]
    cotas_validas = [c for c in cotas if c is not None]

    if cotas_validas:
        cota_dual = min(cotas_validas)
    else:
        cota_dual = "inf"

    guardar_prueba([[caso, cant, cota_dual, mejor_1, var_1, tiempo_1, mejor_4, var_4, tiempo_4, mejor_5, var_5, tiempo_5, mejor_6, var_6, tiempo_6]])
