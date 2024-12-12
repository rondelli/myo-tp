import generador_output_patrones
class Pattern:

    def __init__(self, capacidad_maxima, tamaños):
        self.capacidad_maxima = capacidad_maxima
        self.tamaños = tamaños
        self.ultimo_patron = [0] * len(tamaños)
        self.disponible = capacidad_maxima
        self.indice_actual = 0

    def obtener_patrones(self):
        patrones = []
        patrones.append(self.obtener_primer_patron()[:])
   
        while True:
            patron = self.obtener_siguiente_patron()

            if patron is None:
                break
            patrones.append(patron[:])
        generador_output_patrones.generar_output_patrones("patrones.out", patrones, self.tamaños)
        return patrones

    def obtener_siguiente_patron(self):
        for i in range(self.indice_actual, len(self.tamaños)):
            if self.ultimo_patron[i] > 0:
                self.ultimo_patron[i] -= 1
                self.disponible += self.tamaños[i]
                self.actualizar_tamaños(i + 1)
                if self.ultimo_patron[i] == 0:
                    self.indice_actual += 1
                return self.ultimo_patron
            
            else:
                self.disponible = self.capacidad_maxima
                self.actualizar_tamaños(i)
                return self.ultimo_patron
        return None

    def actualizar_tamaños(self, indice_tamaño):
        for i in range(indice_tamaño, len(self.tamaños)):
            max_cantidad = self.disponible // self.tamaños[i]
            if max_cantidad >= 0:
                self.ultimo_patron[i] = max_cantidad
                self.disponible -= max_cantidad * self.tamaños[i]

    def obtener_primer_patron(self):
        self.actualizar_tamaños(0)
        return self.ultimo_patron