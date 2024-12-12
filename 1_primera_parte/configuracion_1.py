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
    capacidad_discos = random.randint(1, 300)
    cant_archivos = random.randint(400, 550)
    archivos = _generar_archivos(cant_archivos)

    with open(ruta_archivo, "w") as f:

        f.write(f"# Capacidad de dicos en TB (= 1.000.000 MB)\n")
        f.write(str(capacidad_discos) + "\n")

        f.write(f"\n# Cantidad de archivos para backup\n")
        f.write(str(cant_archivos) + "\n")

        f.write(f"\n# Archivos: archivo_id, tamaño (MB) \n")
        for archivo in archivos:
            f.write(archivo + " " + str(archivos[archivo]) + "\n")


def leer_input(ruta_archivo):
    capacidad_disco = 0
    nombres_archivos = []
    tamaños_archivos = []

    with open(ruta_archivo, "r") as f:
        lineas = f.readlines()
        capacidad_disco = int(lineas[1].strip())

        for i in range(7, len(lineas)):
            if lineas[i].strip():
                archivo = lineas[i].split()
                nombres_archivos.append(archivo[0])
                tamaños_archivos.append(int(archivo[1]))
    return capacidad_disco, nombres_archivos, tamaños_archivos


def _generar_archivos(cant_archivos):
    archivos = {}
    contador = 1
    for i in range(cant_archivos):
        archivos["archivo" + str(contador)] = random.randint(1000000, 10000000)
        contador += 1
    return archivos


def generar_output(ruta_archivo, solucion):  
    # solucion = [F, model, y, x, s]
    F = solucion[0]
    model = solucion[1]
    y = solucion[2]
    x = solucion[3]
    s = solucion[4]

    cant_archivos = len(F)
    cant_discos = round(float(model.getObjVal()))
    max_discos = cant_archivos

    with open(ruta_archivo, "w") as f:
        f.write(
            f"Para la configuración del archivo, {cant_discos} discos son suficientes.\n"
        )
        for j in range(max_discos):
            if model.getVal(y[j]) == 0:
                continue

            archivos_en_disco = []
            espacio_ocupado = 0

            for i in range(cant_archivos):
                if model.getVal(x[i, j]) == 0:
                    continue
                archivos_en_disco.append(f"{F[i]}  {s[i]}")
                espacio_ocupado = espacio_ocupado + s[i]

            f.write(f"\nDisco {j+1}: {espacio_ocupado} MB\n")

            for archivo in archivos_en_disco:
                f.write(archivo + "\n")


def generar_output_fallido(nombre_archivo):
    ruta_out = os.path.join(os.path.dirname(__file__), ".", "OUT",
                            nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")