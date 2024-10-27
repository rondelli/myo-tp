import os
import random

def generar_configuracion(nombre_archivo, num_archivos, num_conjuntos):
    C = [f"archivo_{i+1}" for i in range(num_archivos)]
    H = [set() for _ in range(num_conjuntos)]

    # cada archivo debe estar en al menos un conjunto. Añadí una restriccion para que, a lo sumo, pueda estar en
    # la mitad de todos los conjuntos. Esto no es necesario, pero así cada archivo se repite pocas veces.
    for i in range(num_archivos):
        for _ in range(random.randint(1, num_conjuntos // 2)):
            H[random.randrange(num_conjuntos)].add(C[i])

    escribir_configuracion(nombre_archivo, C, H)
    
def escribir_configuracion(nombre_archivo, C, H):
    ruta_in = os.path.join(os.path.dirname(__file__), ".", "IN", nombre_archivo)
    with open(ruta_in, 'w') as f:    

        f.write("Archivos en el conjunto C: " + " ".join(C) + "\n\n")        

        f.write(f"Cantidad de conjuntos H en C: {len(H)}\n\n")        

        for i, conjunto in enumerate(H):
            f.write(f"Conjunto H_{i+1}: " + " ".join(conjunto) + "\n")

def leer_configuracion(nombre_archivo):
    archivos = []
    conjuntos = []

    ruta_in = os.path.join(os.path.dirname(__file__), ".", "IN", nombre_archivo)
    with open(ruta_in, "r") as f:
        
        lineas = f.readlines()

        archivos = lineas[0].strip().split(": ")[1].split()

        for linea in lineas[4:]:
            conjunto = linea.strip().split(": ") 
            if len(conjunto) > 1:
                conjuntos.append(set(conjunto[1].split()))
            else:
                conjuntos.append(set())

    return archivos, conjuntos
