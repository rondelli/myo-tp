import csv
import os
import math

def agregar_contenido_a_linea(caso, nuevos_datos):
    ruta_actual = os.path.dirname(os.path.abspath(__file__)) 
    nombre_archivo = "pruebas.csv" 
    ruta_archivo = os.path.join(ruta_actual, nombre_archivo)

    with open(ruta_archivo, 'r', newline='') as archivo:
        lector_csv = list(csv.reader(archivo))

    existe_caso = False
    for linea in lector_csv:
        if linea[0] == str(caso):
            linea.extend(nuevos_datos)  # Agrega los datos al final de la línea
            existe_caso = True
            break

    if not existe_caso:
        lector_csv.append([caso] + nuevos_datos)   # Agregar los datosa una nueva línea

    with open(ruta_archivo, 'w', newline='') as archivo:
        escritor_csv = csv.writer(archivo)
        escritor_csv.writerows(lector_csv)

def guardar_prueba(resultado):
    # resultado = [caso, cant, cota_dual, mejores, var, tiempos]
    # [caso, cant, cota dual, mejor, var, tiempo, mejor, var, tiempo, mejor, var, tiempo, mejor, var, tiempo]
    resultados = [[resultado[0], resultado[1], resultado[2], resultado[3][0], resultado[4][0], resultado[5][0], resultado[3][1], resultado[4][1], resultado[5][1], resultado[3][2], resultado[4][2], resultado[5][2], resultado[3][3], resultado[4][3], resultado[5][3]]]
    escribir_csv(resultados)


def escribir_csv(datos):
    headers = ["caso", "cant", "cota dual", "mejor1", "var1", "tiempo1", "mejor4", "var4", "tiempo4", "mejor5", "var5", "tiempo5", "mejor6", "var6", "tiempo6"]

    ruta_actual = os.path.dirname(os.path.abspath(__file__)) 
    nombre_archivo = "pruebas.csv" 
    ruta_archivo = os.path.join(ruta_actual, nombre_archivo)

    fue_generado = os.path.isfile(ruta_archivo)

    with open(ruta_archivo, 'a', newline='') as archivo:
        archivo_csv = csv.writer(archivo)

        if not fue_generado:
            archivo_csv.writerow(headers)
        
        archivo_csv.writerows(datos)

def datos_modelo(model):
    try:
        #_, mejor = model_part_1.obtener_solucion_primal_1(model)
        mejor = math.ceil(model.getObjVal()) # esto es lo mimso que lo de arriba --> si no encuentra el optimo da 0 :c
        var = math.ceil(model.getNVars())
        tiempo = model.getSolvingTime()
        cota_dual = math.ceil(model.getDualbound())
    except:
        mejor, var, tiempo, cota_dual = '-', '-', 420, '-'
    return cota_dual, mejor, var, tiempo