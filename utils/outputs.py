import os

######################################################################
# Generar output 1
######################################################################

def generar_output_1(ruta_archivo, solucion):  
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
        f.write(f"Para la configuracion del archivo, {cant_discos} discos son suficientes.\n")
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

######################################################################
# Generar output 2
######################################################################

def generar_output_2(nombre_archivo, solucion):
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


def obtener_solucion_2(solucion):
    # solucion = F, model, x, I, s
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
        if model.getVal(x[i]) > 0.5:
            archivos_elegidos.append(F[i])
            importancia_archivos.append(I[i])
    
    return archivos_elegidos, importancia_archivos

######################################################################
# Generar output 3
######################################################################

def generar_output_3(nombre_archivo, solucion, conjuntos):
    # solucion --> conjuntos_seleccionados
    # conjuntos --> todos los conjuntos
    with open(nombre_archivo, "w") as f:
        f.write(f"Para la configuracion del archivo, se han elegido {len(solucion)} de {len(conjuntos)} conjuntos de H:\n\n")
        for i in range(len(solucion)):
            f.write(f"Conjunto H_{solucion[i]}: {conjuntos[solucion[i]]}.\n")

######################################################################
# Generar output 4
######################################################################

# TODO: Hay que ver que los nombres de los archivos no se repitan - Esto solo funciona cuando no hay tamaños repetidos!
def generar_output_4(ruta_archivo, solucion):
    # solucion = [model, F, x, ordenamiento, c, file_sizes]
    _ = solucion[0]
    _ = solucion[1]
    x = solucion[2]
    ordenamiento = solucion[3]
    c = solucion[4]
    file_sizes = solucion[5]

    patrones_seleccionados = [
        (p, int(x[p].getLPSol())) for p in range(len(x)) if x[p].getLPSol() > 0]
    
    with open(ruta_archivo, "w") as f:
        f.write(f"Para la configuracion del archivo, {len(patrones_seleccionados)} discos/patrones son suficientes.\n")

        # Iterar sobre los patrones seleccionados
        for p, veces in patrones_seleccionados:
            f.write(f"Patron {p} (usado {veces} veces):\n")
            archivos_cubiertos = []

            # Revisar qué tamaños cubre este patrón
            for k, cantidad in enumerate(c[p]):
                if cantidad > 0:
                    # Buscar archivos con este tamaño
                    archivos_cubiertos += [
                        archivo
                        for size, archivo in ordenamiento
                        if size == list(set(file_sizes))[k]
                    ]

            # f.write(f"Tamaños cubiertos: {list(list(set(file_sizes))[k] for k, v in enumerate(c[p]) if v > 0)}\n")
            f.write(f"Archivos cubiertos: {', '.join(archivos_cubiertos)}\n\n")

######################################################################
# Generar outputs 5 y 6
######################################################################

def generar_output_5(nombre_archivo, solucion):
    # solucion = [conjuntos_seleccionados, modelo, conjuntos, nombres_archivos, tamaños_archivos, tiempo]
    conjuntos_seleccionados = solucion[0]
    conjuntos = solucion[2]
    nombres_archivos = solucion[3]
    tamaños_archivos = solucion[4]

    with open(nombre_archivo, "w") as f:
        f.write(f"Para la configuracion del archivo, {len(conjuntos_seleccionados)} discos son suficientes.\n")
        
        for i in range(len(conjuntos_seleccionados)):
            archivos_en_disco = []
            espacio_ocupado = 0
            espacio_ocupado = 0

            for archivo in conjuntos[conjuntos_seleccionados[i]]:
                tamaño = tamaños_archivos[nombres_archivos.index(archivo)]
                espacio_ocupado += tamaño
                archivos_en_disco.append(f"{archivo}  {tamaño}")

            f.write(f"\nDisco {i+1}: {espacio_ocupado} MB\n")
            for archivo in archivos_en_disco:
                f.write(archivo + "\n")


def generar_output_6(nombre_archivo, solucion):
    # solucion = [conjuntos_seleccionados, modelo, conjuntos, nombres_archivos, tamaños_archivos, tiempo]
    generar_output_5(nombre_archivo, solucion)

######################################################################
# Generar output fallido
######################################################################

def generar_output_fallido(nombre_archivo):
    with open(nombre_archivo, "w") as f:
        f.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")

######################################################################
# Generar output patrones
######################################################################

def generar_output_patrones(nombre_archivo, patrones, tamaños):
    with open(nombre_archivo, "w") as f:
        for i in range(len(patrones)):
            f.write(f"Patron {i + 1}: \n")
            
            for j in range(len(patrones[i])):
                f.write(f"{tamaños[j]}: {patrones[i][j]}    ")
        
            f.write(f"\n\n") 