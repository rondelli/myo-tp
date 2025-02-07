#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, "../utils")

import inputs
import configs
import outputs
import model_part_4

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
    inputs.generar_input_4(os.path.dirname(__file__) + '/IN/' + archivo)
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
    capacidad_disco, nombres_archivos, tamaños_archivos = inputs.leer_input_4(os.path.dirname(__file__) + '/IN/' + archivo)
    
    # ordenamos los tamaños (junto con los nombres) de mayor a menor
    ordenamiento = sorted(list(zip(tamaños_archivos, nombres_archivos)), reverse=True)
    tamaños_archivos, nombres_archivos = zip(*ordenamiento)
    solucion = model_part_4.distribuir_archivos_4(capacidad_disco, list(nombres_archivos), list(tamaños_archivos), threshold * 60)
    
    archivo_out = os.path.join(os.path.dirname(__file__), out_path, f'{archivo[:-3]}.out')
    
    if solucion is not None:
        outputs.generar_output_4(archivo_out, solucion)
        
        patrones_out = os.path.join(os.path.dirname(__file__), 'patrones', f'{archivo[:-3]}.out')
        # en solucion[4]= c, solucion[5] = {tamaño: [archivos]}
        # outputs.generar_output_patrones(patrones_out, solucion[4], sorted(list(dict.fromkeys(solucion[5])), reverse=True))
        
    else:
        outputs.generar_output_fallido(archivo_out)