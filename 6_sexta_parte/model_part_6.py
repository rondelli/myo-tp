import sys
import time
from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING
from itertools import product
from math import floor, ceil

import configuracion_6
import model_part_2_6
import model_part_3_6

def obtener_conjuntos(archivo, threshold: int = float('inf')) -> None:
    capacidad_disco, nombres_archivos, tamaños_archivos = configuracion_6.leer_configuracion(f"{archivo}")

    tiempo_inicio = time.time()
    conjuntos = configuracion_6.generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)
    encontro_solucion = True

    while True:
        inicio_ciclo = time.time()
        if inicio_ciclo - tiempo_inicio >= threshold:
            encontro_solucion = False
            break
        
        modelo = model_part_3_6.crear_modelo_3(nombres_archivos, conjuntos, threshold - (inicio_ciclo - tiempo_inicio))
        
        x, _ = model_part_3_6.obtener_solucion_primal_3(modelo)
        y, _ = model_part_3_6.obtener_solucion_dual_3(modelo)

        distribucion = model_part_2_6.distribuir_archivos_2(capacidad_disco, nombres_archivos, tamaños_archivos, y, threshold - (inicio_ciclo - tiempo_inicio))
        solucion_modelo_2 = configuracion_6.generar_output_modelo_2(distribucion)

        if solucion_modelo_2 is None:
            encontro_solucion = False
            break
        elif sum(solucion_modelo_2[1]) > 1:
            conjuntos.append(set(solucion_modelo_2[0]))
        else:
            encontro_solucion = True
            break
    
    conjuntos_seleccionados = []
    tiempo = time.time() - tiempo_inicio
    if encontro_solucion:
        conjuntos_seleccionados = obtener_conjuntos_seleccionados(obtener_solucion_entera(modelo, x))
        return [conjuntos_seleccionados, modelo, conjuntos, tiempo]
    return None

def obtener_conjuntos_seleccionados(solucion):
    conjuntos_seleccionados = [i for i in range(len(solucion)) if solucion[i] == 1]
    return conjuntos_seleccionados

def es_optimo(model, solucion):
    variables = model.getVars() 

    sol = model.getBestSol()

    for var, val in zip(variables, solucion):
        model.setSolVal(sol, var, val)

    return model.checkSol(sol)

def obtener_solucion_entera(model, solucion_continua):
    variables = model.getVars()
    sol = model.getBestSol()
    mejor_combinacion = None
    mejor_solucion = float('inf')

    for i in range(1, 10):
        umbral = i/10
        redondeos = [1 if valor >= umbral else 0 for valor in solucion_continua]

        if es_optimo_rapido(model, variables, redondeos, sol):
            valor_objetivo = model.getSolObjVal(sol)
            model.hideOutput()

            if valor_objetivo < mejor_solucion:
                mejor_solucion = valor_objetivo
                mejor_combinacion = redondeos

    return mejor_combinacion

def es_optimo_rapido(model, variables, solucion, sol):
    for var, val in zip(variables, solucion):
        model.setSolVal(sol, var, val)
    
    return model.checkSol(sol)
