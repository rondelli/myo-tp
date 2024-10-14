import random

def generar_archivos(cant_archivos):
    archivos = {}
    contador = 1
    for i in range(cant_archivos):
        archivos["archivo" + str(contador)] = random.randint(1000000, 10000000)
        contador += 1
    return archivos


def generar_archivo_input(nombre_archivo):
    capacidad_discos = random.randint(1, 100)
    cant_archivos = random.randint(1, 10)
    archivos = generar_archivos(cant_archivos)
    with open(nombre_archivo, 'w') as f:
        # capacidad aleatoria
        f.write(f"# disk capacities in TB (= 1.000.000 MB)\n")
        f.write(str(capacidad_discos) + "\n")
        
        # cantidad de archivos
        f.write(f"\n# number of files to backup\n")
        f.write(str(cant_archivos) + "\n")

        # listado de archivos
        f.write(f"\n# files: file_id, size (in MB)\n")
        for archivo in archivos:
            f.write(archivo + " " + str(archivos[archivo]) + "\n")

