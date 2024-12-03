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

    ruta_in = os.path.join(os.path.dirname(__file__), "IN", nombre_archivo)
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

def generar_conjuntos(capacidad_disco, nombres_archivos, tamaños_archivos):
    conjuntos = []
    archivos_alegidos = set()
    while len(archivos_alegidos) < len(nombres_archivos):
        #conjunto = dict()
        conjunto = set()
        tamaño_conjunto = 0
        while tamaño_conjunto <= capacidad_disco:
            elegido = random.randint(0, len(nombres_archivos)-1)

            if tamaños_archivos[elegido] + tamaño_conjunto <= capacidad_disco:
                #conjunto[nombres_archivos[elegido]] = tamaños_archivos[elegido]
                conjunto.add(nombres_archivos[elegido])
                tamaño_conjunto += tamaños_archivos[elegido]
                
                if nombres_archivos[elegido] not in archivos_alegidos:
                    archivos_alegidos.add(nombres_archivos[elegido])
            else: 
            # Medio feo. Podría pasar que en el conjunto no entren mas archivos y aún no se haya alcanzado el limite del disco.
            # En este caso, si resulta que un archivo elegido no entra, dejamos de agregar archivos en el conjunto.
                break
        conjuntos.append(conjunto)

    return conjuntos

# solucion = F, model, x, I, s
def generar_output_modelo_2(solucion):
    if solucion is None:
        return None

    F = solucion[0]
    model = solucion[1]
    x = solucion[2]
    I = solucion[3]

    cant_archivos = len(F)
    archivos_elegidos = []
    importancia_archivos = []

    for i in range(cant_archivos):
        if model.getVal(x[i]) > 0.5:  # se eligio el archivo
            archivos_elegidos.append(F[i])
            importancia_archivos.append(I[i])
    
    return archivos_elegidos, importancia_archivos
