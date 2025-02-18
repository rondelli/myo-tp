from collections import Counter

archivos = {'a1': 20, 'a2': 13, 'a3': 20}
tamaños_cantidades = dict(Counter(archivos.values()))

tamaño_discos = 50
patrones = []


# no recuerdo si ya hicimos algo así...
while sum(tamaños_cantidades.values()) > 0:
    tamaño_disco_actual = tamaño_discos
    patron = []

    for tamaño_archivo, cantidad_archivos in tamaños_cantidades.items():
        cantidad_utilizados = cantidad_archivos
        espacio_restante = tamaño_disco_actual - (tamaño_archivo * cantidad_utilizados)

        while espacio_restante < 0 and cantidad_utilizados > 0:
            cantidad_utilizados = cantidad_utilizados - 1
            espacio_restante = tamaño_disco_actual - (tamaño_archivo * cantidad_utilizados)
        
        patron.append({tamaño_archivo: cantidad_utilizados})
        tamaño_disco_actual = espacio_restante

        tamaños_cantidades[tamaño_archivo] = tamaños_cantidades[tamaño_archivo] - cantidad_utilizados

    patrones.append(patron)

print(patrones)




