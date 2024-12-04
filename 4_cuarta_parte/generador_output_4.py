import os

def generar_output(output_file, solucion):
    _ = solucion[0]
    _ = solucion[1]
    x = solucion[2]
    ordenamiento = solucion[3]
    c = solucion[4]
    file_sizes = solucion[5]

    # Obtener los patrones seleccionados
    patrones_seleccionados = [
        (p, int(x[p].getLPSol())) for p in range(len(x)) if x[p].getLPSol() > 0]

    ruta_out = os.path.join(os.path.dirname(__file__), ".", "OUT", output_file)
    with open(ruta_out, "w") as f:
        f.write(f"Para la configuración del archivo, {len(patrones_seleccionados)} discos/patrones son suficientes.\n")

        # Iterar sobre los patrones seleccionados
        for p, veces in patrones_seleccionados:
            f.write(f"Patrón {p} (usado {veces} veces):\n")
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

            # Escribir la información del patrón
            # f.write(f"Tamaños cubiertos: {list(list(set(file_sizes))[k] for k, v in enumerate(c[p]) if v > 0)}\n")
            f.write(f"Archivos cubiertos: {', '.join(archivos_cubiertos)}\n\n")


# def generar_output(nombre_archivo, solucion): # solucion = [F, model, y, x, s, q] 
#     F = solucion[0]
#     model = solucion[1]
#     x = solucion[2]
#     s = solucion[3]
#     ordenamiento = solucion[4]
#     c = solucion[5]

#     ordenamiento = sorted(list(zip(s, F)), reverse=True)
#     tamaños_archivos, nombres_archivos = zip(*ordenamiento)

#     cant_discos = round(float(model.getObjVal()))

#     ruta_out = os.path.join(os.path.dirname(__file__), "OUT", nombre_archivo)
#     with open(ruta_out, "w") as f:
#         f.write(f"Para la configuración del archivo, {cant_discos} discos son suficientes.\n")
        
#         for p in range(len(c)):
#             if model.getVal(x[p]) == 0:
#                 continue

#             archivos_en_patron = []
#             espacio_ocupado = 0
            

#             # for i in range(len(file_sizes)):
#             #     tamaño_archivo = file_sizes[i]
#             #     indice = s.index(tamaño_archivo)

#             #     if c[j][indice] > 0:
#             #         archivos_en_patron.append(f"{F[i]}  {tamaño_archivo}")
#             #         espacio_ocupado = espacio_ocupado + tamaño_archivo

#             f.write(f"\nDisco {p + 1}: {espacio_ocupado} MB\n")

#             for archivo in archivos_en_patron:
#                 f.write(archivo + "\n")


def generar_output_fallido(nombre_archivo):
    ruta_out = os.path.join(os.path.dirname(__file__), "OUT", nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")
