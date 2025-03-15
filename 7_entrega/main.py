#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, '../1_primera_parte')
sys.path.insert(0, '../4_cuarta_parte')
sys.path.insert(0, '../5_quinta_parte')
sys.path.insert(0, '../6_sexta_parte')
sys.path.insert(0, '../utils')

import model_part_1
import model_part_4
import model_part_5
import model_part_6
import inputs
import outputs
import configs
import funciones

##################################    ########################################
## Archivos .in del profe:      ##    ## Archivos .in por modelo:           ##
## f0032.in                     ##    ## n_1 --> f0017.in                   ##
## f0512.in                     ##    ## n_4 --> f0074.in (f0082.in con >=) ##
## f2048.in                     ##    ## n_5 --> f0850.in (digamos)         ##
##################################    ## n_6 --> desconocido                ##
                                      ########################################

archivo_conf = os.path.join(os.path.dirname(__file__), 'archivo.cfg')
print(f'Leyendo configuración {archivo_conf}\n')

configuraciones = configs.leer_configuracion(archivo_conf)
out_path = configuraciones.get('outPath')[:-1]
threshold = int(configuraciones.get('threshold', 0))

archivos = [f for f in os.listdir(configuraciones.get('inPath'))]
archivos.remove('.gitkeep')
archivos.remove('f0017.in')
archivos.remove('f0032.in')
archivos.remove('f0074.in')

sys.stderr.write(f'[Debugging] {configuraciones}\n')
sys.stderr.write(f'[Debugging] {archivos}\n')

for archivo in archivos:
    sys.stderr.write(f'[Debugging] {archivo}\n')
    d_t, F, s  = inputs.leer_input_7(os.path.join(os.path.dirname(__file__), 'IN', archivo))
    caso = archivo
    cant = len(F)

    cotas = ['-', '-', '-', '-']
    mejores = ['-', '-', '-', '-']
    var = ['-', '-', '-', '-']
    tiempos = [420, 420, 420, 420]

    sys.stderr.write(f'[Debugging] MODELO 1\n')
    archivo_out = os.path.join(os.path.dirname(__file__), out_path, 'OUT1', f'{archivo[:-3]}.out')
    solucion_1 = model_part_1.distribuir_archivos_1(d_t, F, s, threshold * 60) 
    
    # [F, model, y, x, s]
    if solucion_1 is not None:
        cotas[0], mejores[0], var[0], tiempos[0] = funciones.datos_modelo(solucion_1[1])
        outputs.generar_output_1(archivo_out, solucion_1)
        # (caso, [cant, cota_dual, mejor, var, tiempo])
    else:
        outputs.generar_output_fallido(archivo_out)
    funciones.agregar_contenido_a_fila(caso, [cant, cotas[0], mejores[0], var[0], tiempos[0]])

    sys.stderr.write(f'[Debugging] MODELO 4\n')
    archivo_out = os.path.join(os.path.dirname(__file__), out_path, 'OUT4', f'{archivo[:-3]}.out')
    solucion_4 = model_part_4.distribuir_archivos_4(d_t, F, s, threshold * 60) 
    
    # [F, model, x, s, c, tamaños_nombres]
    if solucion_4 is not None: 
        cotas[1], mejores[1], var[1], tiempos[1] = funciones.datos_modelo(solucion_4[1])                
        outputs.generar_output_4(archivo_out, solucion_4)
    else:
        outputs.generar_output_fallido(archivo_out)
    funciones.agregar_contenido_a_fila(caso, [cant, cotas[1], mejores[1], var[1], tiempos[1]])

    sys.stderr.write(f'[Debugging] MODELO 5\n')
    archivo_out = os.path.join(os.path.dirname(__file__), out_path, 'OUT5', f'{archivo[:-3]}.out')
    solucion_5  = model_part_5.obtener_conjuntos(os.path.dirname(__file__) + '/IN/' + archivo, threshold * 60) 
    
    # [conjuntos_seleccionados, modelo, conjuntos, nombres_archivos, tamaños_archivos, tiempo]
    if solucion_5 is not None:        
        cotas[2], _, var[2], _ = funciones.datos_modelo(solucion_5[1])
        mejores[2] = len(solucion_5[0])
        tiempos[2] = solucion_5[-1]        
        outputs.generar_output_5(archivo_out, solucion_5)
    else:
        outputs.generar_output_fallido(archivo_out)
    funciones.agregar_contenido_a_fila(caso, [cant, cotas[2], mejores[2], var[2], tiempos[2]])

    sys.stderr.write(f'[Debugging] MODELO 6\n')
    archivo_out = os.path.join(os.path.dirname(__file__), out_path, 'OUT6', f'{archivo[:-3]}.out')
    solucion_6  = model_part_6.obtener_conjuntos(os.path.dirname(__file__) + '/IN/' + archivo, threshold * 60)
    
    # [conjuntos_seleccionados, modelo, conjuntos, nombres_archivos, tamaños_archivos, tiempo]
    if solucion_6 is not None:
        cotas[3], _, var[3], _ = funciones.datos_modelo(solucion_6[1])
        mejores[3] = len(solucion_6[0])
        tiempos[3] = solucion_6[-1]        
        outputs.generar_output_6(archivo_out, solucion_6)        
    else:
        outputs.generar_output_fallido(archivo_out)
    funciones.agregar_contenido_a_fila(caso, [cant, cotas[3], mejores[3], var[3], tiempos[3]])

    # FIXME
    cotas_validas = [c for c in cotas if c != '-']
    if cotas_validas:
        cota_dual = min(cotas_validas)
    else:
        cota_dual = '-'

    # funciones.guardar_prueba([[caso, cant, cota_dual, mejor_1, var_1, tiempo_1, mejor_4, var_4, tiempo_4, mejor_5, var_5, tiempo_5, mejor_6, var_6, tiempo_6]])
    # funciones.guardar_prueba([caso, cant, cota_dual, mejores, var, tiempos])
