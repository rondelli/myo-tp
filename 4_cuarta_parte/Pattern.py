def obtener_patrones(capacidad_maxima, tamaños):
    # Genera TODOS los patrones posibles, maximales o no
    if capacidad_maxima == 0:
        return [[0] * len(tamaños)]

    patrones = []
    minimo = min(tamaños)

    def obtener_patron(espacio_disponible, indice, patron_actual, minimo):
        if indice == len(tamaños):
            if espacio_disponible < minimo:
                patrones.append(patron_actual[:])
            return
        
        tamaño = tamaños[indice]
        maximo = espacio_disponible // tamaño
        
        # viendolo al revés ⟶ range(maximo, -1, -1),
        # quizás podamos hacer que busque maximales directamente
        # aunque una vez le pregunté si había que generar solo maximales
        # (a mano, en los ejercicios de patrones), y me dijo que no hacía falta
        for cont in range(maximo, -1, -1):
            patron_actual[indice] = cont
            obtener_patron(espacio_disponible - cont * tamaño, indice + 1, patron_actual, minimo)
            patron_actual[indice] = 0
    
    obtener_patron(capacidad_maxima, 0, [0] * len(tamaños), minimo)
    return patrones

capacidad_maxima = 10
tamaños = [1, 2, 3]

patrones_esperados = [[0, 2, 2],
                      [0, 5, 0],
                      [1, 0, 3],
                      [1, 3, 1],
                      [2, 1, 2],
                      [2, 4, 0],
                      [3, 2, 1],
                      [4, 0, 2],
                      [4, 3, 0],
                      [5, 1, 1],
                      [6, 2, 0],
                      [7, 0, 1],
                      [8, 1, 0],
                      [10, 0, 0]]

for patron in patrones_esperados:
    print(patron, sum(p * t for p, t in zip(patron, tamaños)))

patrones_obtenidos = obtener_patrones(capacidad_maxima, tamaños)
print(patrones_obtenidos)