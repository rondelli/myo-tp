class Pattern:
    def __init__(self, capacidad_maxima, tamaños):
        self.capacidad_maxima = capacidad_maxima
        self.tamaños = tamaños
        self.ultimo_patron = []
        self.disponible = capacidad_maxima
        # self.patrones = []
        for t in range(len(self.tamaños)):
            self.ultimo_patron.append(0)
    
    def obtener_patrones(self):
        patrones = []
        patrones.append(self.obtener_primer_patron()[:])
        # print("patron", patron)
        while True:
            patron = self.obtener_siguiente_patron()
            if patron is not None:
                # print("patron", patron)
                patrones.append(patron[:])
                self.disponible = self.capacidad_maxima
            else:
                break
        return patrones

    def obtener_siguiente_patron(self):
        for t in range(len(self.tamaños)):
            if self.ultimo_patron[t] > 0:
                self.ultimo_patron[t] = self.ultimo_patron[t] - 1
                self.disponible -= self.tamaños[t]
                break
        
        if t < len(self.tamaños) - 1: # si no es el ultimo tamaño
            self.actualizar_tamaños(t + 1)
            return self.ultimo_patron
        else:
            return None
    
    def actualizar_tamaños(self, indice_tamaño):
        if indice_tamaño == len(self.tamaños) or self.disponible <= 0:
            return self.ultimo_patron
        
        tamaño = self.tamaños[indice_tamaño]
        entran = self.disponible // tamaño
        if entran > 0:
            self.ultimo_patron[indice_tamaño] = entran
            self.disponible -= entran * tamaño

        self.actualizar_tamaños(indice_tamaño + 1)
    
    def obtener_primer_patron(self):
        self.actualizar_tamaños(indice_tamaño=0)
        return self.ultimo_patron