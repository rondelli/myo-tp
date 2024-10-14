#!/usr/bin/env python3

from configuracion import generador_configuracion
from configuracion import leer_configuracion
import big_data

# esto deberia recibirlo por parametro? desde linea de comandos
nombre_archivo_config = "a_1.in"
generador_configuracion.generar_configuracion(nombre_archivo_config)
capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion.leer_configuracion(f"./{nombre_archivo_config}")
big_data.distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos)

