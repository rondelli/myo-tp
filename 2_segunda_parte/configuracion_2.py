import os
import random

def leer_configuracion(ruta_archivo):
    configuraciones = {}

    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            if '=' in linea:
                clave, valor = linea.strip().split('=', 1)
                valor = valor.strip().strip('\'"')
                configuraciones[clave] = valor
    
    return configuraciones


def generar_input(ruta_archivo):
    capacidad_discos = random.randint(1, 100)
    cant_archivos = random.randint(1, 50)
    archivos = generar_archivos(cant_archivos)

    with open(ruta_archivo, "w") as f:

        f.write(f"# Capacidad de dicos en TB (= 1.000.000 MB)\n")
        f.write(str(capacidad_discos) + "\n")

        f.write(f"\n# Cantidad de archivos para backup\n")
        f.write(str(cant_archivos) + "\n")

        f.write(f"\n# Archivos: archivo_id, tamaño (MB), importancia\n")
        for archivo in archivos:
            f.write(archivo + " " + str(archivos[archivo][0]) + " " + str(archivos[archivo][1]) + "\n")


def leer_input(ruta_archivo):
    capacidad_disco = 0
    nombres_archivos = []
    tamaños_archivos = []
    importancias_archivos = []

    with open(ruta_archivo, "r") as f:
        lineas = f.readlines()
        capacidad_disco = int(lineas[1].strip())
        for i in range(7, len(lineas)):
            if lineas[i].strip():
                archivo = lineas[i].split()
                nombres_archivos.append(archivo[0])
                tamaños_archivos.append(int(archivo[1]))
                importancias_archivos.append(int(archivo[2]))
    return capacidad_disco, nombres_archivos, tamaños_archivos, importancias_archivos


def generar_archivos(cant_archivos):
    archivos = {}
    contador = 1
    for i in range(cant_archivos):
        # {nombreArchivo: [tamaño, importancia] }
        archivos["archivo" + str(contador)] = [
            random.randint(1000000, 10000000),
            random.randint(1, 10)
        ]
        contador += 1
    return archivos


def generar_output(nombre_archivo, solucion):
    # solución = [F, model, fake_x, I, s]
    F = solucion[0]
    model = solucion[1]
    x = solucion[2]
    I = solucion[3]
    s = solucion[4]

    cant_archivos = len(F)
    cant_archivos_elegidos = sum(1 for i in range(cant_archivos) if model.getVal(x[i]) > 0.5)
    archivos_elegidos = []
    importancia_total = 0

    with open(nombre_archivo, "w") as f:
        f.write(f"Para la configuracion del archivo, se han elegido {cant_archivos_elegidos} archivos.\n")

        for i in range(cant_archivos):
            if model.getVal(x[i]) > 0.5:
                archivos_elegidos.append(f"{F[i]}  {s[i]} {I[i]}")
                importancia_total += I[i]

        for archivo in archivos_elegidos:
            f.write(archivo + "\n")

        f.write(f"\nLa suma de sus indicadores de importancia da {importancia_total}.")


def generar_output_fallido(nombre_archivo):
    with open(nombre_archivo, "w") as f:
        f.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")