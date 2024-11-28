import sys
import time
from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING
from itertools import product
from math import floor, ceil

import configuracion_6
import model_part_2
import model_part_3

def obtener_conjuntos(archivo, threshold: int = float('inf')) -> None:
    capacidad_disco, nombres_archivos, tamaños_archivos = configuracion_6.leer_configuracion(f"{archivo}")

    # PASO 1
    conjuntos = configuracion_6.generar_conjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)

    duracion = threshold * 60
    tiempo_inicio = time.time()
    encontro = True

    while True:
        modelo = model_part_3.crear_modelo_3(nombres_archivos, conjuntos)
        
        x, obj_x = model_part_3.obtener_solucion_primal_3(modelo)
        y, obj_y = model_part_3.obtener_solucion_dual_3(modelo)

        sys.stderr.write(f"[Debugging] obj x {obj_x}\n")
        sys.stderr.write(f"[Debugging] obj y {obj_y}\n")

        optimo = es_optimo(modelo, x)
        sys.stderr.write(f"[Debugging] es óptimo: {optimo}")

        # PASO 4
        distribucion = model_part_2.distribuir_archivos_2(capacidad_disco, nombres_archivos, tamaños_archivos, y)
        solucion_modelo_2 = configuracion_6.generar_output_modelo_2(distribucion)

        # PASO 5
        # copy_of_model = Model(sourceModel=modelo_3)
        if time.time() - tiempo_inicio > duracion:
            encontro = False
            break
        elif sum(solucion_modelo_2[1]) > 1:
            conjuntos.append(set(solucion_modelo_2[0]))
        else:
            encontro = True
            break
    
    conjuntos_seleccionados = []
    if encontro:
        print(f"solucion optima encontrada en {time.time() - tiempo_inicio}")
        conjuntos_seleccionados = obtener_conjuntos_seleccionados(x)
    else:
        print("no se encontraron soluciones optimas")
        
    return [conjuntos_seleccionados, modelo, conjuntos]

def obtener_conjuntos_seleccionados(solucion):
    conjuntos_seleccionados = [i for i in range(len(solucion)) if solucion[i] == 1]
    return conjuntos_seleccionados

# Esta función supone que el model es `optimal`
def es_optimo(model, solucion):
    variables = model.getVars() 

    sol = model.getBestSol()

    for var, val in zip(variables, solucion):
        model.setSolVal(sol, var, val)

    return model.checkSol(sol)

def obtener_solucion_entera(model, solucion_continua):
    print("CONTINUA:", solucion_continua)
    variables = model.getVars()
    sol = model.getBestSol()
    mejor_combinacion = None
    mejor_solucion = float('inf')
    # model = Model()

    for i in range(1, 10):
        umbral = i/10
        redondeos = [1 if valor >= umbral else 0 for valor in solucion_continua]
        if es_optimo_rapido(model, variables, redondeos, sol):
        # if es_optimo(model, redondeos):
            valor_objetivo = model.getSolObjVal(sol)
            model.hideOutput()
            if valor_objetivo < mejor_solucion:
                mejor_solucion = valor_objetivo
                mejor_combinacion = redondeos
    print("ENTERA:", mejor_combinacion)
    # print("SOL:", mejor_solucion)
    return mejor_combinacion

def es_optimo_rapido(model, variables, solucion, sol):
    for var, val in zip(variables, solucion):
        model.setSolVal(sol, var, val)
    
    return model.checkSol(sol)
