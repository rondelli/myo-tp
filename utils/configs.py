def leer_configuracion(ruta_archivo):
    configuraciones = {}

    with open(ruta_archivo, 'r') as archivo:
        for linea in archivo:
            if '=' in linea:
                clave, valor = linea.strip().split('=', 1)
                valor = valor.strip().strip('\'"')
                configuraciones[clave] = valor
    
    return configuraciones