import os
import random


def generar_conjuntos(capacidad_disco, nombres_archivos, tamaños_archivos):

    conjuntos = []
    archivos_alegidos = set()
    while len(archivos_alegidos) < len(nombres_archivos):
        conjunto = dict()
        conjunto = set()
        tamaño_conjunto = 0
        # elegido = 0
        while tamaño_conjunto <= capacidad_disco:
            elegido = random.randint(0, len(nombres_archivos)-1)
            if tamaños_archivos[elegido] + tamaño_conjunto <= capacidad_disco:
                conjunto.add(nombres_archivos[elegido])
                tamaño_conjunto += tamaños_archivos[elegido]                
                
                if nombres_archivos[elegido] not in archivos_alegidos:
                    archivos_alegidos.add(nombres_archivos[elegido])
            else: 
            # Medio feo. Podría pasar que en el conjunto no entren mas archivos y aún no se haya alcanzado el limite del disco.
            # En este caso, si resulta que un archivo elegido no entra, dejamos de agregar archivos en el conjunto.
                break
            conjuntos.append(conjunto)

    return conjuntos


