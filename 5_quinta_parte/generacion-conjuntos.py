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

# FUNCION DE AGUS
def generar_subconjuntos(peso_disco, nombres_archivos, pesos_archivos, tiempo_inicio, tiempo_limite_total):
            H = []
            archivos = list(zip(nombres_archivos, pesos_archivos))
            print ("Generando subconjuntos")
            if not chequear_existe_tiempo_ejecucion(tiempo_inicio, tiempo_limite_total):
                print("Se terminó el tiempo generando los conjuntos.")
                return None
            # También generamos subconjuntos de archivos de forma más interdependiente para agregar variedad
            for i in range(len(archivos)):
                for j in range(i + 1, len(archivos)):
                    # Intentamos agregar combinaciones de diferentes pares de archivos
                    combo = [archivos[i], archivos[j]]
                    total_size = sum(peso for _, peso in combo)
                    if not chequear_existe_tiempo_ejecucion(tiempo_inicio, tiempo_limite_total):
                        print("Se terminó el tiempo generando los subconjuntos.")
                        return []
                    if total_size <= peso_disco:
                        H.append([nombre for nombre, _ in combo])
            if not chequear_existe_tiempo_ejecucion(tiempo_inicio, tiempo_limite_total):
                        print("Se terminó el tiempo generando los subconjuntos.")
                        return []
            print ("Termino de generar subconjuntos")
            return H




