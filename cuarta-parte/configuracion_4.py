import random
import os

# Functions
# Kinda done, check numbers
def generar_archivos(number_of_files: int):
    sizes = []
    for i in range(random.randrange(10, 20)):
        sizes.append(random.randint(10, 70) * 10**6)

    files = {}
    k = 1
    for i in range(number_of_files):
        files["file_id_" + str(k)] = random.choice(sizes)
        k += 1
    return files


# Kinda done, check numbers
def escribir_configuracion(input_file_name):
    disk_size = random.randint(70, 100)
    number_of_files = random.randint(7, 70)
    files = generar_archivos(number_of_files)

    path_in = os.path.join(os.path.dirname(__file__), ".", "IN", input_file_name)
    with open(path_in, "w") as f_in:
        f_in.write(f"# disk capacities in TB (= 1.000.000 MB)\n")
        f_in.write(str(disk_size) + "\n\n")
        f_in.write(f"# number of files to backup\n")
        f_in.write(str(number_of_files) + "\n\n")
        f_in.write(f"# files: file_id, size (in MB)\n")
        
        for f in files:
            f_in.write(f + " " + str(files[f]) + "\n")


# FIXME:
# filen_names debería ser un map con
# <nombre-de-archivo><tamaño-del-archivo>
# para después en el output recomponer con distribuir_archivos()
# tipo ir sacando de F el nombre y tamaño, e ir restando de size_counts un 1 en la cantidad por cada tamaño
def leer_configuracion(input_file_name: str):
    disk_size = 0
    file_names = []
    file_sizes = []

    path_in = os.path.join(os.path.dirname(__file__), ".", "IN", input_file_name)
    with open(path_in, "r") as f_in:
        lines = f_in.readlines()
        disk_size = int(lines[1].strip())

        for i in range(7, len(lines)):
            if lines[i].strip():
                file = lines[i].split()
                file_names.append(file[0])
                file_sizes.append(int(file[1]))

    return disk_size, file_names_with_sizes, file_sizes
