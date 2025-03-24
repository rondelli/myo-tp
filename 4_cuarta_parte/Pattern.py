import time

def obtener_patrones(capacidad_maxima, tamaños_cantidades, time_limit = -1):
    tiempo_inicio = time.time()
    tamaños = []
    cantidades = []

    for tamaño, cantidad in tamaños_cantidades.items():
        tamaños.append(tamaño)
        cantidades.append(cantidad)

    if capacidad_maxima == 0:
        return [[0] * len(tamaños)]

    patrones = []
    minimo = min(tamaños)

    def obtener_patron(espacio_disponible, indice, patron_actual, minimo):
        if indice == len(tamaños):
            patrones.append(patron_actual[:])
            return
        
        cantidad = cantidades[indice]
        tamaño = tamaños[indice]
        maximo = espacio_disponible // tamaño

        limite = maximo if maximo < cantidad else cantidad
        
        for cont in range(limite, -1, -1):
            patron_actual[indice] = cont
            obtener_patron(espacio_disponible - cont * tamaño, indice + 1, patron_actual, minimo)
            patron_actual[indice] = 0
    
    tiempo_transcurrido = time_limit - (time.time() - tiempo_inicio)
    if tiempo_transcurrido < time_limit:
        obtener_patron(capacidad_maxima, 0, [0] * len(tamaños), minimo)

    return patrones
