import os

# solucion = F, model, x, I, s
def generar_output(nombre_archivo, solucion):
    F = solucion[0]
    model = solucion[1]
    x = solucion[2]
    I = solucion[3]
    s = solucion[4]

    cant_archivos = len(F)
    cant_archivos_elegidos = sum(1 for i in range(cant_archivos)
                                 if model.getVal(x[i]) > 0.5)
    archivos_elegidos = []
    importancia_total = 0

    ruta_out = os.path.join(os.path.dirname(__file__), ".", "OUT",
                            nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(
            f"Para la configuracion del archivo, se han elegido {cant_archivos_elegidos} archivos.\n"
        )

        for i in range(cant_archivos):
            if model.getVal(x[i]) > 0.5:  # se eligio el archivo
                archivos_elegidos.append(f"{F[i]}  {s[i]} {I[i]}")
                importancia_total += I[i]

        for archivo in archivos_elegidos:
            f.write(archivo + "\n")

        f.write(
            f"\nLa suma de sus indicadores de importancia da {importancia_total}."
        )

def generar_output_fallido(nombre_archivo):
    with open(nombre_archivo, "w") as f:
        f.write(
            f"No se ha encontrado solucion para la configuracion del archivo.\n"
        )
