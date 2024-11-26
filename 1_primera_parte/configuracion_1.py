import os
import random

def generar_archivos(cant_archivos):
    archivos = {}
    contador = 1
    for i in range(cant_archivos):
        archivos["archivo" + str(contador)] = random.randint(1000000, 10000000)
        contador += 1
    return archivos


def generar_configuracion(nombre_archivo):
    capacidad_discos = random.randint(1, 300)
    cant_archivos = random.randint(400, 550)
    archivos = generar_archivos(cant_archivos)

    # ruta_in = os.path.join(os.path.dirname(__file__), "IN", nombre_archivo)
    ruta_in = os.path.dirname(__file__) + "/IN/" + nombre_archivo
    with open(ruta_in, "w") as f:

        f.write(f"# Capacidad de dicos en TB (= 1.000.000 MB)\n")
        f.write(str(capacidad_discos) + "\n")

        f.write(f"\n# Cantidad de archivos para backup\n")
        f.write(str(cant_archivos) + "\n")

        f.write(f"\n# Archivos: archivo_id, tamaño (MB) \n")
        for archivo in archivos:
            f.write(archivo + " " + str(archivos[archivo]) + "\n")


def leer_configuracion(nombre_archivo):
    capacidad_disco = 0
    nombres_archivos = []
    tamaños_archivos = []

    # ruta_in = os.path.join(os.path.dirname(__file__), "IN", nombre_archivo)
    ruta_in = os.path.dirname(__file__) + "/IN/" + nombre_archivo
    with open(ruta_in, "r") as f:
        lineas = f.readlines()
        capacidad_disco = int(lineas[1].strip())

        for i in range(7, len(lineas)):
            if lineas[i].strip():
                archivo = lineas[i].split()
                nombres_archivos.append(archivo[0])
                tamaños_archivos.append(int(archivo[1]))
    return capacidad_disco, nombres_archivos, tamaños_archivos
