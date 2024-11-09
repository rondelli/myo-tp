import time
from pyscipopt import Model, Eventhdlr, SCIP_EVENTTYPE

class FeasibleSolutionCollector(Eventhdlr):
    def _init_(self):
        super()._init_()
        self.solutions = []

    def eventinit(self):
        self.model.catchEvent(self.model.EVENTTYPE.BESTSOLFOUND, self)
    
    def eventexit(self):
        self.model.dropEvent(self.model.EVENTTYPE.BESTSOLFOUND, self)

    def eventeexec(self, event):
        print("hola")

def distribuir_archivos(d_t, F, s, time_limit=60):
    """
    Distribuye archivos entre discos minimizando el número de discos utilizados.
    
    Parámetros:
    - d_t: Capacidad total de cada disco en MB.
    - F: Lista de nombres de archivos.
    - s: Lista de tamaños de archivos correspondientes a cada archivo en MB.
    - time_limit: Tiempo límite en segundos para encontrar la mejor solución posible.

    Retorna:
    - Una lista con la mejor solución encontrada dentro del tiempo límite o None si no se encontró ninguna.
    """
    model = Model("big_data")
    collector = FeasibleSolutionCollector()
    model.includeEventhdlr(collector, "FeasibleSolutionCollector", "")

    d = d_t * 10**6
    if d < 0 or any(s_i < 0 for s_i in s):
        return None

    n = len(F)
    m = n  # no se puede tener más discos que archivos

    # y_{j} = 1 si se elige el disco j, 0 si no
    y = [model.addVar(f"y_{j}", vtype="BINARY") for j in range(m)]
    model.setObjective(sum(y), sense="minimize")

    # x_{i, j} = 1 si se elige el archivo i para el disco j, 0 si no
    x = {}
    for i in range(m):
        for j in range(m):
            x[i, j] = model.addVar(f"x_{i}_{j}", vtype="BINARY")

    # Que los archivos se elijan solo para un disco
    for i in range(n):
        model.addCons(sum(x[i, j] for j in range(m)) == 1)

    # Que no se pasen de capacidad los discos
    for j in range(m):
        model.addCons(sum(x[i, j] * s[i] for i in range(n)) <= d * y[j])



    # Configurar el límite de tiempo en el solver
    model.setParam("limits/time", time_limit)
    
    # Registrar el tiempo de inicio
    start_time = time.time()

    model.setParam("display/freq", 1)
    model.setParam("display/verblevel", 4)

    model.optimize()
    print(f"Time: {model.getSolvingTime()}")

    print(f"Cant sols: {model.getNSols()}")

    # Obtener la mejor solución encontrada
    sol = model.getBestSol()
    if sol is not None and (model.getStatus() == "optimal" or model.getStatus() == "feasible"):
        return [F, model, y, x, s]
    else:
        return None
