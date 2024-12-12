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


def generar_input(nombre_archivo, num_archivos=None, num_conjuntos=None):
    if num_archivos is None:
        num_archivos = random.randint(400, 550)
    if num_conjuntos is None:
        num_conjuntos = random.randint(10, 300)

    C = [f"archivo_{i+1}" for i in range(num_archivos)]
    H = [set() for _ in range(num_conjuntos)]

    for i in range(num_archivos):
        for _ in range(random.randint(1, num_conjuntos)):
            H[random.randrange(num_conjuntos)].add(C[i])

    escribir_input(nombre_archivo, C, H)


def escribir_input(nombre_archivo, C, H):
    with open(nombre_archivo, 'w') as f:
        f.write("Archivos en el conjunto C: " + " ".join(C) + "\n\n")
        f.write(f"Cantidad de conjuntos H en C: {len(H)}\n\n")
        for i, conjunto in enumerate(H):
            f.write(f"Conjunto H_{i+1}: " + " ".join(conjunto) + "\n")


def leer_input(nombre_archivo):
    archivos = []
    conjuntos = []

    with open(nombre_archivo, "r") as f:
        lineas = f.readlines()
        archivos = lineas[0].strip().split(": ")[1].split()
        for linea in lineas[4:]:
            conjunto = linea.strip().split(": ")
            if len(conjunto) > 1:
                conjuntos.append(set(conjunto[1].split()))
            else:
                conjuntos.append(set())

    return archivos, conjuntos


def generar_output(nombre_archivo, solucion, conjuntos):
    # solucion --> conjuntos_seleccionados
    # conjuntos --> todos los conjuntos
    with open(nombre_archivo, "w") as f:
        f.write(f"Para la configuracion del archivo, se han elegido {len(solucion)} de {len(conjuntos)} conjuntos de H:\n\n")
        for i in range(len(solucion)):
            f.write(f"Conjunto H_{solucion[i]}: {conjuntos[solucion[i]]}.\n")


def generar_output_fallido(nombre_archivo):
    with open(nombre_archivo, "w") as f:
        f.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")
