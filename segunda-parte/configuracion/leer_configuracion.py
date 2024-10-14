def leer_configuracion(nombre_archivo):
    capacidad_disco = 0
    nombres_archivos = []
    tamaños_archivos = []
    importancias_archivos = []
    with open(nombre_archivo, "r") as f:
        lineas = f.readlines()
        capacidad_disco = int(lineas[1].strip())
        # Los archivos empiezan en la linea 8:
        for i in range(7, len(lineas)):
            # Saltear las lineas vacias
            if lineas[i].strip():
                archivo = lineas[i].split()
                nombres_archivos.append(archivo[0])
                tamaños_archivos.append(int(archivo[1]))
                importancias_archivos.append(int(archivo[2]))
    return capacidad_disco, nombres_archivos, tamaños_archivos, importancias_archivos


print(leer_configuracion("./prueba.in"))