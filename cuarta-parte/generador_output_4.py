import os

def generar_output(output_file_name, solution):
    F = solution[0]
    model = solution[1]
    y = solution[2]
    c = solution[3]
    s = solution[4]

    number_of_files = len(F)
    number_of_disks = number_of_files  # La cantidad de discos disponibles es a lo sumo la cantidad de archivos
    number_of_used_disks = round(float(model.getObjVal()))

    path_out = os.path.join(os.path.dirname(__file__), ".", "OUT",
                            output_file_name)
    with open(path_out, "w") as f_out:
        f_out.write(
            f"Para la configuracion del archivo, {number_of_used_disks} discos son suficientes.\n"
        )
        for j in range(number_of_disks):
            if model.getVal(y[j]) == 0:
                continue

            archivos_en_disco = []
            used_space = 0

            for i in range(number_of_files):
                if (i, j) in c:
                    if model.getVal(c[i, j]) == 0:
                        continue
                    archivos_en_disco.append(f"{F[i]}  {s[i]}")
                    used_space += s[i]

            f_out.write(f"\nDisco {j+1}: {used_space} MB\n")

            for f in archivos_en_disco:
                f_out.write(f + "\n")


def generar_output_fallido(output_file_name):
    path_out = os.path.join(os.path.dirname(__file__), ".", "OUT", output_file_name)
    with open(path_out, "w") as f_out:
        f_out.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")