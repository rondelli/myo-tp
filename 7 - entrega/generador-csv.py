import csv
import os

headers = ["caso", "cant", "cota dual", "mejor1", "var1", "tiempo1", "mejor4", "var4", "tiempo4", "mejor5", "var5", "tiempo5", "mejor6", "var6", "tiempo6"]
datos = []

ruta_actual = os.path.dirname(os.path.abspath(__file__)) 
nombre_archivo = "pruebas.csv" 
ruta_archivo = os.path.join(ruta_actual, nombre_archivo)

fue_generado = os.path.isfile(ruta_archivo)

# Abrir el archivo en modo escritura
with open(ruta_archivo, 'a', newline='') as archivo:
    archivo_csv = csv.writer(archivo)

    if not fue_generado:
        archivo_csv.writerow(headers)
    
    # Escribir las filas en el archivo CSV
    archivo_csv.writerows(datos)
