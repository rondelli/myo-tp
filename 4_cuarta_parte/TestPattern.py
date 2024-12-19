import unittest
import Pattern

class TestPattern(unittest.TestCase):
    def test_capacidad_0(self):
        capacidad_maxima = 0
        tamaños = range(10)
        patrones_esperados = [[0] * 10]

        patrones_obtenidos = Pattern.obtener_patrones(capacidad_maxima, tamaños)
        self.assertEqual(patrones_esperados, patrones_obtenidos, msg=None)
    
    def test_tamaños_0(self):
        capacidad_maxima = 2
        tamaños = [0] * 2

        # Acá esperamos que meta infinitas veces cada tamaño... no creo que haga falta
    
    def test_capacidad_y_tamaños_0(self):
        capacidad_maxima = 0
        tamaños = [0] * 2

        patrones_esperados = [[0] * 2]
        
        patrones_obtenidos = Pattern.obtener_patrones(capacidad_maxima, tamaños)
        self.assertEqual(patrones_esperados, patrones_obtenidos, msg=None)

    def test_capacidad_menor_a_tamaños(self):
        capacidad_maxima = 2
        tamaños = range(3, 10)
        patrones_esperados = [[0] * 7]
        
        patrones_obtenidos = Pattern.obtener_patrones(capacidad_maxima, tamaños)
        self.assertEqual(patrones_esperados, patrones_obtenidos, msg=None)


    
    def test_tamaño_igual_que_capacidad(self):
        capacidad_maxima = 2
        tamaños = [2] * 2

        patrones_esperados = [[1, 0],
                              [0, 1]]
        
        patrones_obtenidos = Pattern.obtener_patrones(capacidad_maxima, tamaños)
        self.assertEqual(patrones_esperados, patrones_obtenidos, msg=None)

    def test_tamaños_redondos(self):    #jasashjasjas no se como ponerle
        capacidad_maxima = 10
        tamaños = [3, 7]

        patrones_esperados = [[1, 1]]
        
        patrones_obtenidos = Pattern.obtener_patrones(capacidad_maxima, tamaños)
        self.assertEqual(patrones_esperados, patrones_obtenidos, msg=None)
    
    def test_tamaños_diferencia(self):    #jasashjasjas no se como ponerle
        capacidad_maxima = 10
        tamaños = [3, 5]

        patrones_esperados = [[0, 2],
                              [1, 1],
                              [3, 0]]
        
        patrones_obtenidos = Pattern.obtener_patrones(capacidad_maxima, tamaños)
        self.assertEqual(patrones_esperados, patrones_obtenidos, msg=None)

    def test_tres_tamaños(self):
        capacidad_maxima = 10
        tamaños = [1, 2, 3]

        patrones_esperados = [[1, 0, 3],
                              [2, 1, 2],
                              [4, 0, 2],
                              [1, 3, 1],
                              [3, 2, 1],
                              [5, 1, 1],
                              [7, 0, 1],
                              [0, 5, 0],
                              [2, 4, 0],
                              [4, 3, 0],
                              [6, 2, 0],
                              [8, 1, 0],
                              [10, 0, 0]]

        patrones_obtenidos = Pattern.obtener_patrones(capacidad_maxima, tamaños)

        # la idea es que haga solo los que necesita
        patrones_esperados_set = set(map(tuple, patrones_esperados))
        patrones_obtenidos_set = set(map(tuple, patrones_obtenidos))

        self.assertTrue(patrones_esperados_set.issubset(patrones_obtenidos_set), "No todos los patrones están en 'patrones_obtenidos_set'.")

        # self.assertEqual(patrones_esperados, patrones_obtenidos, msg=None)

unittest.TextTestRunner().run(unittest.makeSuite(TestPattern))
