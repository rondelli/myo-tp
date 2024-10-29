import os


def generar_output(nombre_archivo, solucion, conjuntos):
    ruta_out = os.path.join(os.path.dirname(__file__), ".", "OUT",
                            nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(
            f"Para la configuracion del archivo, se han elegido {len(solucion)} conjuntos de H:\n\n"
        )
        for i in range(len(solucion)):
            f.write(f"Conjunto H_{solucion[i]}: {conjuntos[solucion[i]]}.\n")


def generar_output_fallido(nombre_archivo):
    with open(nombre_archivo, "w") as f:
        f.write(
            f"No se ha encontrado solucion para la configuracion del archivo.\n"
        )
