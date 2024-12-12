#!/usr/bin/env python3

import sys
import configuracion_2
from model_part_2 import *

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
    configuracion_2.generar_input(os.path.dirname(__file__) + '/IN/' + archivo)
    archivos.append(archivo)
    
elif sys.argv[1] == '-u':
    print(f'Usando {archivo}\n')
    archivos.append(archivo)
    
elif sys.argv[1] == '-c':
    print(f'Leyendo configuración {archivo}\n')
    configuraciones = configuracion_2.leer_configuracion(os.path.join(os.path.dirname(__file__), archivo))

    out_path = configuraciones.get('outPath')[:-1]
    threshold = int(configuraciones.get('threshold', 0))
    archivos = [f for f in os.listdir(configuraciones.get('inPath'))]
    archivos.remove('.gitkeep')


for archivo in archivos:
    capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos = configuracion_2.leer_input(os.path.dirname(__file__) + '/IN/' + archivo)
    solucion = distribuir_archivos_2(capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos, threshold * 60)

    archivo_out = os.path.join(os.path.dirname(__file__), out_path, f'{archivo[:-3]}.out')
    
    if solucion is not None:
        configuracion_2.generar_output(archivo_out, solucion)
    else:
        configuracion_2.generar_output_fallido(archivo_out)