import csv
import os

# EL NOMBRE DE ESTO ES MUY IP pero no se me ocurre algo mejor

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

