import os


# solucion = [F, model, y, x, s]
def generar_output(nombre_archivo, solucion):
    F = solucion[0]
    model = solucion[1]
    y = solucion[2]
    x = solucion[3]
    s = solucion[4]

    cant_archivos = len(F)
    cant_discos = round(float(model.getObjVal()))
    number_of_disks = cant_archivos  # La cantidad de discos disponibles es a lo sumo la cantidad de archivos

    ruta_out = os.path.join(os.path.dirname(__file__), ".", "OUT",
                            nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(
            f"Para la configuracion del archivo, {cant_discos} discos son suficientes.\n"
        )
        for j in range(number_of_disks):
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


def generar_output_fallido(nombre_archivo):
    ruta_out = os.path.join(os.path.dirname(__file__), ".", "OUT",
                            nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(
            f"No se ha encontrado solucion para la configuracion del archivo.\n"
        )
