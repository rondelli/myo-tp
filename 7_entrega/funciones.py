import csv
import os

def guardar_prueba(datos):
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

def leer_configuracion():
    ruta_archivo = os.path.join(os.path.dirname(__file__), 'archivo.cfg')
    configuraciones = {}

    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            if '=' in linea:
                clave, valor = linea.strip().split('=', 1)
                valor = valor.strip().strip('\'"')
                configuraciones[clave] = valor
    
    return configuraciones

def leer_archivo(nombre_archivo):
    capacidad_disco = 0
    nombres_archivos = []
    tamaños_archivos = []

    ruta_in = os.path.join(os.path.dirname(__file__), "IN", nombre_archivo)
    with open(ruta_in, "r") as f:
        lineas = f.readlines()
        capacidad_disco = int(lineas[1].strip())

        for i in range(7, len(lineas)):
            if lineas[i].strip():
                archivo = lineas[i].split()
                nombres_archivos.append(archivo[0])
                tamaños_archivos.append(int(archivo[1]))
    return capacidad_disco, nombres_archivos, tamaños_archivos

def datos_modelo(model):
    try:
        #_, mejor = model_part_1.obtener_solucion_primal_1(model)
        mejor = model.getObjVal() # esto es lo mimso que lo de arriba --> si no encuentra el optimo da 0 :c
    except TypeError:
        var, mejor = None, None
    var = model.getNVars()
    tiempo = model.getSolvingTime()
    cota_dual = dual_bound = model.getDualbound()
    return cota_dual, mejor, var, tiempo
