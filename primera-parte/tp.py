#!/usr/bin/env python3

from pyscipopt import Model, quicksum
import sys
import os
import random

# Functions
def generate_files(number_of_files : int):
    files = {}
    k = 1
    for i in range(number_of_files):
        files["file_id_" + str(k)] = random.randint(1000000, 10000000)
        k += 1
    return files

def generate_input_file(input_file_name):
    disk_size = random.randint(1, 100)
    number_of_files = random.randint(1, 50)
    files = generate_files(number_of_files)

    path_in = os.path.join(os.path.dirname(__file__), ".", "IN", input_file_name)
    with open(path_in, "w") as f_in:
        f_in.write(f"# disk capacities in TB (= 1.000.000 MB)\n")
        f_in.write(str(disk_size) + "\n\n")
        f_in.write(f"# number of files to backup\n")
        f_in.write(str(number_of_files) + "\n\n")
        f_in.write(f"# files: file_id, size (in MB)\n")
        for f in files:
            f_in.write(f + " " + str(files[f]) + "\n")

def read_input_file(input_file_name : str):
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

    return disk_size, file_names, file_sizes

# d_t: disk size in TB
# F: file names
# s: File sizes in MB
def solve(d_t : int, F : list[str], s : list[int]):
    if d_t < 0 or any(i < 0 for i in s):
        return

    # Tamaño del disco en MB
    d = d_t * 10**6;

    # Cantidad de archivos
    n = len(F)

    # Cantidad de discos, a lo sumo, un disco por archivo
    m = n

    # Define model
    model = Model("big_data")

    # x[<i, j> in F * D] binary: 1 si el archivo $i$ está en el disco $j$, 0 en caso contrario
    x = {}
    for i in range(n):
        for j in range(m):
            x[i, j] = model.addVar(vtype='B', name = f"x_{i}_{j}")

    # y[D] binary: 1 si se usa el disco $j$, 0 en caso contrario
    y = [model.addVar(vtype='B', name = f"y_{j}") for j in range(m)]

    # minimize disks:
    model.setObjective(quicksum(y), sense = "minimize")

    # Cada archivo debe estar en un solo disco
    for i in range(n):
        model.addCons(quicksum(x[i, j] for j in range(m)) == 1) #, name = "c1_{i}_{j}")

    # Los archivos $i$ que entran en el disco $j$
    for j in range(m):
        model.addCons(quicksum(s[i] * x[i, j] for i in range(n)) <= d * y[j]) #, name = "c2_{i}_{j}")

    # Esta restricción no es necesaria.
    # No se puede elegir un disco vacío
    # for j in range(m):
        # model.addCons(quicksum(x[i, j] for i in range(n)) <= n * y[j]) #, name = "c3_{i}_{j}")

    model.optimize()
    objective_value = model.getObjVal()
    solution = model.getBestSol()

    if solution is not None and model.getStatus() == "optimal" or model.getStatus() == "feasible":
        return [F, model, y, x, s]
    else:
        return None

def generate_file_output(output_file_name, solution):
    F = solution[0]
    model = solution[1]
    y = solution[2]
    x = solution[3]
    s = solution[4]

    number_of_files = len(F)
    number_of_disks = number_of_files # La cantidad de discos disponibles es a lo sumo la cantidad de archivos
    number_of_used_disks = round(float(model.getObjVal()))

    path_out = os.path.join(os.path.dirname(__file__), ".", "OUT", output_file_name)
    with open(path_out, "w") as f_out:
        f_out.write(f"Para la configuracion del archivo, {number_of_used_disks} discos son suficientes.\n")
        for j in range(number_of_disks):
            if model.getVal(y[j]) == 0:
                continue

            archivos_en_disco = []
            used_space = 0
            
            for i in range(number_of_files):
                if model.getVal(x[i, j]) == 0:
                    continue
                archivos_en_disco.append(f"{F[i]}  {s[i]}")
                used_space += s[i]

            f_out.write(f"\nDisco {j+1}: {used_space} MB\n")

            for f in archivos_en_disco:
                f_out.write(f + "\n")

def generate_output_file_failed(output_file_name):
    path_out = os.path.join(os.path.dirname(__file__), ".", "OUT", output_file_name)
    with open(path_out, "w") as f_out:
        f_out.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")

# Main
# ----

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} input_file_name_to_generate")
    sys.exit(1)

input_file_name = sys.argv[1]
print(f"Input file name to generate: {input_file_name}\n")

generate_input_file(input_file_name)

disk_size, file_names, file_sizes = read_input_file(f"./{input_file_name}")

solution = solve(disk_size, file_names, file_sizes)

if solution is not None:
    generate_file_output(f"{input_file_name[:-3]}.out", solution)
else:
    generate_output_file_failed(f"{input_file_name[:-3]}.out")
