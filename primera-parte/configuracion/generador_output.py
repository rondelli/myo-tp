from pyscipopt import Model

def generar_output(nombre_archivo, nombres_archivos, model, y_j, x_ij, f_i):
    cant_archivos = len(nombres_archivos)
    cant_discos = sum(1 for j in range(cant_archivos) if model.getVal(y_j[j]) > 0.5)

    with open(nombre_archivo, 'w') as f:
        
        f.write(f"Para la configuracion del archivo, {cant_discos} discos son suficientes.\n")
        
        for j in range(cant_discos):
            archivos_en_disco = []
            espacio_ocupado = 0
            
            for i in range(cant_archivos):
                if model.getVal(x_ij[i, j]) > 0.5: # se eligio el archivo
                    archivos_en_disco.append(f"{nombres_archivos[i]}  {f_i[i]}")
                    espacio_ocupado = espacio_ocupado + f_i[i]

            f.write(f"\nDisco {j+1}: {espacio_ocupado} MB\n")

            for archivo in archivos_en_disco:
                f.write(archivo + "\n")

def generar_output_fallido(nombre_archivo):
    with open(nombre_archivo, 'w') as f:
        f.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")