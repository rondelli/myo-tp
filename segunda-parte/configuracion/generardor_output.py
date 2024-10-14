from pyscipopt import Model

def generar_output(nombre_archivo, nombres_archivos, model, x_i, b_i, f_i):
    cant_archivos = len(nombres_archivos)
    cant_archivos_elegidos = sum(1 for i in range(cant_archivos) if model.getVal(x_i[i]) > 0.5)
    archivos_elegidos = []
    importancia_total = 0

    with open(nombre_archivo, 'w') as f:
        
        f.write(f"Para la configuracion del archivo, se han elegido {cant_archivos_elegidos} archivos.\n")

        for i in range(cant_archivos):
            if model.getVal(x_i[i]) > 0.5: # se eligio el archivo
                archivos_elegidos.append(f"{nombres_archivos[i]}  {f_i[i]} {b_i[i]}")
                importancia_total += b_i[i]

        for archivo in archivos_elegidos:
            f.write(archivo + "\n")
        
        f.write(f"La suma de sus indicadores de importancia da {importancia_total}.")

def generar_output_fallido(nombre_archivo):
    with open(nombre_archivo, 'w') as f:
        f.write(f"No se ha encontrado solucion para la configuracion del archivo.\n")