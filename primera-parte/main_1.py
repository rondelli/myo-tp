#!/usr/bin/env python3
from configuracion_1 import *
from big_data import distribuir_archivos

nombre_archivo_config = "a_1.in"
generar_configuracion(nombre_archivo_config)
capacidad_disco, nombres_archivos, tamaños_archivos = leer_configuracion(f"./{nombre_archivo_config}")
distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos)

