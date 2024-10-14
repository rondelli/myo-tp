from configuracion.generador_configuracion import generar_configuracion
from configuracion.leer_configuracion import leer_configuracion
import distribuidor_archivos

nombre_archivo_config = "a_2.in"
generar_configuracion(nombre_archivo_config)
capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos = leer_configuracion(f"./{nombre_archivo_config}")
distribuidor_archivos.distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos, importancia_archivos)

