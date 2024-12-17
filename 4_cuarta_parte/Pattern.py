def obtener_patrones(capacidad_maxima, tamaños):
    # Genera TODOS los patrones posibles, maximales o no
    patrones = []

    def obtener_patron(espacio_disponible, indice, patron_actual):
        if indice == len(tamaños):
            patrones.append(patron_actual[:])
            return
        
        tamaño = tamaños[indice]
        maximo = espacio_disponible // tamaño
        
        for cont in range(maximo + 1):
            patron_actual[indice] = cont
            obtener_patron(espacio_disponible - cont * tamaño, indice + 1, patron_actual)
            patron_actual[indice] = 0
    
    obtener_patron(capacidad_maxima, 0, [0] * len(tamaños))
    return patrones