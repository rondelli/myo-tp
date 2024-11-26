from pyscipopt import Model
from pyscipopt import quicksum
from pyscipopt import SCIP_PARAMSETTING
from itertools import product
from math import floor, ceil

sys.path.insert(0, "../3_segunda_parte")
from model_part_3 import *

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
