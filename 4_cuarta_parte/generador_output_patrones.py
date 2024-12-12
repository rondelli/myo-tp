import os

def generar_output_patrones(output_file, patrones, tamaños):
    ruta_out = os.path.join(os.path.dirname(__file__), ".", "OUT", output_file)
    with open(ruta_out, "w") as f:
        for i in range(len(patrones)):
            f.write(f"Patron {i + 1}: \n")
            
            for j in range(len(patrones[i])):
                f.write(f"{tamaños[j]}: {patrones[i][j]}    ")
        
            f.write(f"\n\n")
                

def generar_output_fallido(nombre_archivo):
    ruta_out = os.path.join(os.path.dirname(__file__), "OUT", nombre_archivo)
    with open(ruta_out, "w") as f:
        f.write(f"No se han podido generar los patrones.\n")
