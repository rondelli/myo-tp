# Modelado y Optimización - Trabajo Práctico

## Descripción General

Este trabajo práctico aplica conceptos de modelado y optimización mediante técnicas de programación lineal entera. El proyecto aborda una serie de problemas relacionados con la gestión de archivos en una empresa de datos, diseñando soluciones eficientes que optimizan el uso de recursos como el almacenamiento en discos y la priorización de datos según su importancia.

La implementación se realiza utilizando distintas tecnologías y herramientas, incluyendo modelado directo en ZIMPL y desarrollo algorítmico en Python mediante la biblioteca PySCIPOpt. A lo largo del proyecto se consideran restricciones como la capacidad limitada de los discos, la importancia de los archivos y la necesidad de optimizar tanto la cantidad de recursos utilizados como la calidad de las soluciones obtenidas.

## Estructura del Proyecto

El repositorio está organizado en las siguientes secciones:

### Parte 1: Minimización de Discos para Backup

Se debe realizar el backup de n archivos en discos idénticos de capacidad d, sin dividir los archivos. El objetivo es determinar la cantidad mínima de discos necesarios para almacenar todos los archivos.

**Modelo Matemático:**

Definimos las siguientes variables:
- n: Cantidad de archivos
- s_i: Tamaño del archivo i en MB, para todo i en {1, ..., n}
- m: Cantidad de discos disponibles, con m = n
- d: Capacidad del disco en TB
- x_ij: Variable binaria donde x_ij = 1 indica que el archivo i está en el disco j
- y_j: Variable binaria donde y_j = 1 indica que se está usando el disco j

El modelo de optimización se formula como:

```
Minimizar: Σ(j=1 hasta m) y_j

Sujeto a:
  Σ(j=1 hasta m) x_ij = 1,  ∀i ∈ {1, ..., n}  (cada archivo en un solo disco)
  Σ(i=1 hasta n) s_i · x_ij ≤ d · y_j,  ∀j ∈ {1, ..., m}  (capacidad del disco)
  x_ij ∈ {0, 1},  ∀i, j
  y_j ∈ {0, 1},  ∀j
```

### Parte 2: Maximización de Importancia

Se asigna un indicador de importancia I a cada archivo según características como sensibilidad, frecuencia de uso y rareza. El objetivo es encontrar un subconjunto de archivos que quepan en un disco de tamaño d y que maximicen la suma de indicadores de importancia.

**Modelo Matemático:**

Definimos las siguientes variables:
- I_i: Importancia del archivo i
- x_i: Variable binaria donde x_i = 1 indica que el archivo i está en el disco

El modelo de optimización se formula como:

```
Maximizar: Σ(i=1 hasta n) I_i · x_i

Sujeto a:
  Σ(i=1 hasta n) s_i · x_i ≤ d  (capacidad del disco)
  x_i ∈ {0, 1},  ∀i
```

### Parte 3: Problema de Set Cover

Se busca resolver el problema de cobertura de conjuntos (Set Cover Problem), donde se debe encontrar la cantidad mínima de discos necesarios para cubrir todos los archivos, considerando subconjuntos predefinidos de archivos que pueden almacenarse juntos.

### Parte 4: Generación de Columnas

Implementación del algoritmo de generación de columnas (Column Generation) para resolver el problema de Set Cover de manera eficiente. Esta técnica permite generar dinámicamente las columnas (subconjuntos) más prometedoras durante el proceso de optimización.

### Parte 5: Heurística de Dantzig

Implementación de una heurística basada en el algoritmo de Dantzig para resolver el problema de distribución de archivos. Esta aproximación permite obtener soluciones de buena calidad en tiempos de ejecución reducidos.

### Parte 6: Variantes del Modelo

Exploración de variantes y extensiones de los modelos anteriores, combinando diferentes técnicas y restricciones para obtener soluciones más robustas y eficientes.

### Parte 7: Entrega Final

Integración de todos los modelos y técnicas desarrolladas en las partes anteriores. Incluye scripts de prueba y comparación de resultados entre los diferentes enfoques implementados.

## Requisitos del Sistema

### Dependencias de Software

- Python 3.x
- PySCIPOpt: Interfaz de Python para el solver SCIP
- SCIP: Solver de optimización para programación entera mixta
- ZIMPL: Lenguaje de modelado matemático (para las partes 1 y 2)

### Instalación de Dependencias

Para instalar las dependencias de Python:

```bash
pip install pyscipopt
```

Para la instalación de SCIP, consultar la documentación oficial en https://www.scipopt.org/

## Estructura de Directorios

Cada parte del proyecto contiene la siguiente estructura:

```
N_parte/
├── IN/              # Archivos de entrada con casos de prueba
├── OUT/             # Archivos de salida con soluciones
├── main.py          # Script principal de ejecución
├── model_part_N.py  # Implementación del modelo en PySCIPOpt
└── archivo.cfg      # Archivo de configuración
```

El directorio `utils/` contiene módulos auxiliares:
- `inputs.py`: Funciones para lectura y generación de archivos de entrada
- `outputs.py`: Funciones para escritura de archivos de salida
- `configs.py`: Funciones para manejo de configuraciones

## Uso

### Ejecución General

Cada parte puede ejecutarse de manera independiente. El formato general es:

```bash
cd N_parte/
python main.py [OPCIÓN] [ARCHIVO]
```

Donde las opciones disponibles son:
- `-g`: Generar un nuevo archivo de entrada
- `-u`: Usar un archivo de entrada existente
- `-c`: Usar un archivo de configuración

### Ejemplos de Uso

**Generar y resolver un caso:**
```bash
cd 1_primera_parte/
python main.py -g caso_1.in
```

**Usar un archivo existente:**
```bash
cd 1_primera_parte/
python main.py -u caso_1.in
```

**Ejecutar con archivo de configuración:**
```bash
cd 1_primera_parte/
python main.py -c archivo.cfg
```

### Formato de Archivos de Entrada

Los archivos de entrada (.in) tienen el siguiente formato:

```
# Capacidad del disco en TB
<capacidad>
# Lista de archivos y sus tamaños en MB
<nombre_archivo_1> <tamaño_1>
<nombre_archivo_2> <tamaño_2>
...
```

Para las partes que incluyen importancia:

```
<capacidad>
<nombre_archivo_1> <tamaño_1> <importancia_1>
<nombre_archivo_2> <tamaño_2> <importancia_2>
...
```

### Formato de Archivos de Salida

Los archivos de salida (.out) contienen la solución óptima encontrada, incluyendo la asignación de archivos a discos y el valor de la función objetivo.

## Modelos de Optimización

### Técnicas Implementadas

1. **Programación Lineal Entera (ILP)**: Modelado directo del problema utilizando variables binarias y restricciones lineales.

2. **Generación de Columnas**: Técnica de descomposición que permite resolver problemas de gran escala generando dinámicamente las variables más prometedoras.

3. **Heurísticas**: Algoritmos aproximados que proporcionan soluciones de buena calidad en tiempos computacionales reducidos.

4. **Set Cover**: Formulación del problema como un problema de cobertura de conjuntos, un problema clásico en optimización combinatoria.

### Consideraciones de Complejidad

El problema de minimización de discos es una variante del problema de Bin Packing, conocido por ser NP-hard. Las soluciones implementadas buscan un balance entre optimalidad y eficiencia computacional mediante el uso de técnicas exactas y heurísticas.

## Documentación Técnica

El documento `doc.pdf` contiene la documentación completa del proyecto, incluyendo:
- Formulación matemática detallada de cada modelo
- Análisis de complejidad computacional
- Resultados experimentales y comparaciones
- Conclusiones y trabajo futuro

El código fuente LaTeX correspondiente se encuentra en `doc.tex`.

## Archivos Adicionales

- `notas.txt`: Notas de desarrollo y observaciones sobre el comportamiento de los modelos
- `.vscode/`: Configuración del entorno de desarrollo para Visual Studio Code
- `.gitignore`: Especificación de archivos excluidos del control de versiones

## Resultados y Análisis

El proyecto incluye análisis experimental de los diferentes modelos implementados, evaluando:
- Tiempo de ejecución
- Calidad de la solución
- Escalabilidad con respecto al tamaño del problema
- Consumo de memoria

Los resultados detallados se encuentran en el documento principal y en el archivo `7_entrega/pruebas.csv`.

## Referencias

- Korte, B., & Vygen, J. (2012). Combinatorial Optimization: Theory and Algorithms. Springer.
- Wolsey, L. A. (1998). Integer Programming. Wiley-Interscience.
- Documentación de SCIP: https://www.scipopt.org/
- Documentación de PySCIPOpt: https://github.com/scipopt/PySCIPOpt
- ZIMPL User Guide: http://zimpl.zib.de/

## Autores

Este proyecto fue desarrollado como parte del curso de Modelado y Optimización.

## Licencia

Este proyecto es material académico desarrollado con fines educativos.
