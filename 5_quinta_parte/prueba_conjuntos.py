#!/usr/bin/env python3
import os
import sys
import time
import helpers

# from configuracion_5 import *

sys.path.insert(0, "../utils")

import inputs
import configs
import outputs
import model_part_5

if len(sys.argv) != 3:
    print(f'Uso: {sys.argv[0]} OPTION archivo')
    print(f'      OPTIONS: -g | -u | -c')
    print(f'      -g generar archivo')
    print(f'      -u usar archivo ya generado')
    print(f'      -c usar configuración')
    sys.exit(1)

archivo = sys.argv[2]
archivos = []
threshold = 7
out_path = 'OUT'

if sys.argv[1] == '-g':
    print(f'Generando {archivo}\n')
    inputs.generar_input_5(os.path.dirname(__file__) + '/IN/' + archivo)
    archivos.append(archivo)
    
elif sys.argv[1] == '-u':
    print(f'Usando {archivo}\n')
    archivos.append(archivo)
    
elif sys.argv[1] == '-c':
    print(f'Leyendo configuración {archivo}\n')
    configuraciones = configs.leer_configuracion(os.path.join(os.path.dirname(__file__), archivo))
    out_path = configuraciones.get('outPath')[:-1]
    threshold = int(configuraciones.get('threshold', 0))
    archivos = [f for f in os.listdir(configuraciones.get('inPath'))]
    archivos.remove('.gitkeep')


for archivo in archivos:
    capacidad_disco, nombres_archivos, tamaños_archivos = inputs.leer_input_5(os.path.dirname(__file__) + '/IN/' + archivo)
    
    H1 = helpers.generar_subconjuntos(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)
    print(H1)

    H2 = helpers.generar_subconjuntos_5(capacidad_disco * 10**6, nombres_archivos, tamaños_archivos)
    print(H2)
    