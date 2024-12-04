import os

def generar_output(outPath, nombre_archivo, solucion):
    _ = solucion[0]
    _ = solucion[1]
    x = solucion[2]
    ordenamiento = solucion[3]
    c = solucion[4]
    file_sizes = solucion[5]

    # Obtener los patrones seleccionados
    patrones_seleccionados = [
            (p, int(x[p].getLPSol())) for p in range(len(x)) if x[p].getLPSol() > 0]

    path_out = os.path.join(
        os.path.dirname(__file__), ".", outPath, "OUT4", nombre_archivo
    )
    with open(path_out, "w") as f:
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

def generar_output_fallido(outPath, nombre_archivo):
    path_out = os.path.join(
        os.path.dirname(__file__), ".", outPath, "OUT4", nombre_archivo
    )
    with open(path_out, "w") as f:
        f.write(
            f"No se ha encontrado solucion para la configuracion del archivo.\n"
        )
