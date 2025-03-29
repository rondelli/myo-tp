#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, "../utils")

import inputs
import configs
import outputs
import model_part_2

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
    inputs.generar_input_2(os.path.dirname(__file__) + '/IN/' + archivo)
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
    capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos = inputs.leer_input_2(os.path.dirname(__file__) + '/IN/' + archivo)
    solucion = model_part_2.distribuir_archivos_2(capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos, threshold * 60)

    archivo_out = os.path.join(os.path.dirname(__file__), out_path, f'{archivo[:-3]}.out')
    
    if solucion is not None:
        print(f'Se encontró solución. Generando {archivo_out}...')
        outputs.generar_output_2(archivo_out, solucion)
        print(f'Solución generada en {archivo_out}')
    else:
        print(f'No se encontró solución para {archivo}')
        outputs.generar_output_fallido(archivo_out)
        print(f'Solución fallida generada en {archivo_out}')