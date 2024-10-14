from configuracion_2 import *
from importance import distribuir_archivos

nombre_archivo_config = "b_1.in"
generar_configuracion(nombre_archivo_config)
capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos = leer_configuracion(f"./{nombre_archivo_config}")
distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos)