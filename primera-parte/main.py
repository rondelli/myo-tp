# pensar un mejor nombre ;)

import generador_input
import cargar_configuracion
import distribuidor_archivos

# esto deberia recibirlo por parametro? desde linea de comandos
nombre_archivo_config = "a1.in"
generador_input.generar_archivo_input(nombre_archivo_config)
capacidad_disco, nombres_archivos, tamaños_archivos = cargar_configuracion.leer_configuracion(f"./{nombre_archivo_config}")
distribuidor_archivos.distribuir_archivos(capacidad_disco, nombres_archivos, tamaños_archivos)

