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

def generar_output_4(ruta_archivo, solucion):
    x = solucion[2] 
    c = solucion[4] 
    tamaños_nombres = solucion[5]

    # Ordena los tamaños de mayor a menor
    tamaños_existentes = sorted(list(dict.fromkeys(tamaños_nombres)), reverse=True)

    # Asignamos archivos disponibles a cada tamaño
    archivos_disponibles = {tamaño: list(tamaños_nombres[tamaño]) for tamaño in tamaños_existentes}

    patrones_seleccionados = [(p, int(x[p].getLPSol())) for p in range(len(x)) if x[p].getLPSol() > 0]

    cont_discos = 0
    with open(ruta_archivo, "w") as f:
        f.write(f"Para la configuracion del archivo, {sum(cantidad for _, cantidad in patrones_seleccionados)} discos son suficientes.\n")

        for indice_patron, cantidad_usos in patrones_seleccionados:
            patron = c[indice_patron]
            for _ in range(cantidad_usos):
                cont_discos += 1
                espacio_ocupado = 0
                archivos_cubiertos_patron = []

                # Procesa cada tamaño en el patrón
                for i in range(len(patron)):
                    if patron[i] > 0:  # Si este tamaño está siendo usado
                        tamaño = tamaños_existentes[i]
                        for _ in range(patron[i]):  # Asigna archivos según la cantidad del patrón
                            if archivos_disponibles[tamaño]:
                                archivo = archivos_disponibles[tamaño].pop(0)
                                archivos_cubiertos_patron.append(f"{archivo}  {tamaño}")
                                espacio_ocupado += tamaño

                # Escribe el disco al archivo de salida
                f.write(f"\nDisco {cont_discos}: {espacio_ocupado} MB\n")
                for archivo in archivos_cubiertos_patron:
                    f.write(archivo + "\n")

            
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
            # print(patrones[i])
            for j in range(len(patrones[i])):
                # print(f"tamaño {j} {tamaños[j]}:  cantidad {i, j} {patrones[i][j]}    ")
                f.write(f" {tamaños[j]}: {patrones[i][j]}\n")
        
            f.write(f"\n\n") 