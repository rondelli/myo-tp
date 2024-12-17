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

    # obtengo los tamaños sin repetidos, y los ordeno de mayor a menor para que los indices de los tamaños coincidan con los usados en los patrones
    tamaños_existentes = sorted(list(dict.fromkeys(tamaños_nombres)), reverse=True)

    archivos_almacenados = {tamaño: [] for tamaño in dict.fromkeys(tamaños_nombres)}

    # cuantas veces se uso cada patron {numero de patron, cantidad de usos}
    patrones_seleccionados = [(p, int(x[p].getLPSol())) for p in range(len(x)) if x[p].getLPSol() > 0]
    patrones_seleccionados = [i for i, cantidad in patrones_seleccionados for _ in range(cantidad)]

    # print("PATRONES GENERADOS", len(c), "-->", c)
    # print("PATRONES SELECCIONADOS:", patrones_seleccionados)
        
    cont_discos = 0
    with open(ruta_archivo, "w") as f:
        f.write(f"Para la configuracion del archivo, {len(patrones_seleccionados)} discos son suficientes.\n")
        for indice_patron in patrones_seleccionados:
            cont_discos += 1
            archivos_cubiertos_patron = []
            espacio_ocupado = 0
            patron = c[indice_patron]
            # print("\n", cont_discos, "PATRON NRO", indice_patron, "-->", patron)
            # Revisar qué tamaños cubre este patrón
            for i in range(len(patron)): # revisamos cada posicion del patron
                if patron[i] > 0: # se utiliza al menos un tamaño de la posicion i del patron
                    tamaño_i = tamaños_existentes[i] # recuperamos el tamaño de la posicion i del patron
                    cont_usos = 0
                    for archivo in tamaños_nombres[tamaño_i]:
                        # filtramos: queremos la cantidad suficiente de archivos de ese tamaño que todavia no hayan sido usados en otro patron anterior
                        if archivo not in archivos_almacenados[tamaño_i] and cont_usos < patron[i]:
                            archivos_almacenados[tamaño_i].append(archivo)
                            archivos_cubiertos_patron.append(f"{archivo}  {tamaño_i}")
                            espacio_ocupado = espacio_ocupado + tamaño_i
                            cont_usos += 1
                            # print("   TAMAÑO:", tamaño_i, "NOMBRE:", archivo, "CONT USOS:", cont_usos, "USOS:", patron[i])
                            
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