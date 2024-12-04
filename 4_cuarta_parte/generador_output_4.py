import os

########################################################################
# Este archivo es igual a generador_output_1.py
########################################################################

# [F, model, y, x, s, q]
# nombres, model, discos_elegidos, 

def generar_output(nombre_archivo, solucion): # solucion = [F, model, y, x, s, q] 
    F = solucion[0]
    model = solucion[1]
    x = solucion[2]
    s = solucion[3]
    ordenamiento = solucion[4]
    c = solucion[5]

    file_sizes, F = zip(*ordenamiento)

    cant_archivos = len(F)
    cant_discos = round(float(model.getObjVal()))

    # La cantidad de discos disponibles es a lo sumo la cantidad de archivos
    number_of_disks = cant_archivos

    ruta_out = os.path.join(os.path.dirname(__file__), "OUT", nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(f"Para la configuración del archivo, {cant_discos} discos son suficientes.\n")
        
        for j in range(len(c)):
            if model.getVal(x[j]) == 0:
                continue

            archivos_en_disco = []
            espacio_ocupado = 0

            # print("PATRÓN:", j)

            for i in range(len(file_sizes)):
                tamaño_archivo = file_sizes[i]
                indice = s.index(tamaño_archivo)

                if c[j][indice] > 0:
                    archivos_en_disco.append(f"{F[i]}  {tamaño_archivo}")
                    espacio_ocupado = espacio_ocupado + tamaño_archivo

            f.write(f"\nDisco {j+1}: {espacio_ocupado} MB\n")

            for archivo in archivos_en_disco:
                f.write(archivo + "\n")


def generar_output_fallido(nombre_archivo):
    ruta_out = os.path.join(os.path.dirname(__file__), "OUT", nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")
