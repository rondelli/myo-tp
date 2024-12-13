import random

######################################################################
# Generar inputs 1 (y 4 y 5) y 2
######################################################################

def generar_input_1(ruta_archivo: str):
    generar_input(ruta_archivo, False)

def generar_input_2(ruta_archivo: str):
    generar_input(ruta_archivo, True)

def generar_input_4(ruta_archivo: str):
    generar_input_1(ruta_archivo)

def generar_input_5(ruta_archivo: str):
    generar_input_1(ruta_archivo)

def generar_input(ruta_archivo: str, importancia: bool):
    capacidad_discos = random.randint(1, 300)
    cant_archivos = random.randint(400, 550)
    archivos = generar_archivos(cant_archivos, importancia)

    with open(ruta_archivo, "w") as f:

        f.write(f"# Capacidad de dicos en TB (= 1.000.000 MB)\n")
        f.write(str(capacidad_discos) + "\n")

        f.write(f"\n# Cantidad de archivos para backup\n")
        f.write(str(cant_archivos) + "\n")

        if not importancia:
            f.write(f"\n# Archivos: archivo_id, tamaño (MB) \n")
            for archivo in archivos:
                f.write(archivo + " " + str(archivos[archivo]) + "\n")
        else:
            f.write(f"\n# Archivos: archivo_id, tamaño (MB), importancia\n")
            for archivo in archivos:
                f.write(archivo + " " + str(archivos[archivo][0]) + " " + str(archivos[archivo][1]) + "\n")

def generar_archivos(cant_archivos: int, importancia: bool):
    archivos = {}
    contador = 1
    for i in range(cant_archivos):
        if not importancia:
            # {nombreArchivo: tamaño}
            archivos["archivo"  + str(contador)] = random.randint(1000000, 10000000)
        else:
            # {nombreArchivo: [tamaño, importancia] }
            archivos["archivo" + str(contador)] = [
            random.randint(1000000, 10000000),
            random.randint(1, 10)
        ]
        contador += 1
    return archivos

######################################################################
# Leer inputs 1 (y 4 y 5) y 2
######################################################################

def leer_input_1(ruta_archivo: str):
    return leer_input(ruta_archivo, False)

def leer_input_2(ruta_archivo: str):
    return leer_input(ruta_archivo, True)

def leer_input_4(ruta_archivo: str):
    return leer_input_1(ruta_archivo)

def leer_input_5(ruta_archivo: str):
    return leer_input_1(ruta_archivo)

def leer_input(ruta_archivo: str, importancia: bool):
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
                if importancia:
                    importancias_archivos.append(int(archivo[2]))

    if not importancia:
        return capacidad_disco, nombres_archivos, tamaños_archivos 
    else:
        return capacidad_disco, nombres_archivos, tamaños_archivos, importancias_archivos
    
######################################################################
# Generar input 3
######################################################################

def generar_input_3(nombre_archivo, num_archivos=None, num_conjuntos=None):
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

######################################################################
# Leer input 3
######################################################################

def leer_input_3(nombre_archivo):
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

######################################################################
