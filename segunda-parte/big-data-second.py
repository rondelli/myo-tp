'''
d = capacidad del disco CONSTANTE
a_{i} = tamaño del archivo i CONSTANTE (input) - n archivos
b_{i} = importancia del archivo i
x_{i}= 1 si se elige el archivo i


maximize b_{1} * x_{1} + ... + b_{n} * x_{n}
s.t 
    1. que no se pasen de capacidad
        a_{1}* x_{1} + a_{2}* x_{2}  + .. a_{n}* x_{n} <= d

    2. generales
        x_{i} pert {0, 1}
        a_{i}, b_{i} >= 0

'''