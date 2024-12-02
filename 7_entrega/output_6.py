import os


def generar_output(outPath, nombre_archivo, solucion, conjuntos):
    path_out = os.path.join(
        os.path.dirname(__file__), ".", outPath, "OUT6", nombre_archivo
    )
    with open(path_out, "w") as f:
        f.write(
            f"Para la configuracion del archivo, se han elegido {len(solucion)} de los {len(conjuntos)} conjuntos de H:\n\n"
        )
        for i in range(len(solucion)):
            f.write(f"Conjunto H_{solucion[i]}: {conjuntos[solucion[i]]}.\n")


def generar_output_fallido(outPath, nombre_archivo):
    path_out = os.path.join(
        os.path.dirname(__file__), ".", outPath, "OUT6", nombre_archivo
    )
    with open(path_out, "w") as f:
        f.write(
            f"No se ha encontrado solucion para la configuracion del archivo.\n"
        )
