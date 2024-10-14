# Tamaño del disco
param d_t := read "a_1.in" as "1n" use 1 comment "#";
param d := d_t * 10**6;

# Conjunto de archivos f_{i} \forall i \in \{1, \ldots, n\}
set F := { read "a_1.in" as "<1s>" skip 2 comment "#" };

# Cantidad de archivos
param n := card(F);

# Cantidad de discos, a lo sumo, un disco por archivo
param m := n;

# Conjunto de discos
set D := { 1 .. m };

# Tamaños de los archivos f_{i} \forall i \in \{1, \ldots, n\}
param s[F] := read "a_1.in" as "<1s> 2n" skip 2 comment "#";

# 1 si el archivo $i$ está en el disco $j$, 0 en caso contrario
var x[<i, j> in F * D] binary;

# 1 si se usa el disco $j$, 0 en caso contrario
var y[D] binary;

minimize disks: sum<j> in D: y[j];

# Cada archivo debe estar en un solo disco
subto c1:
	forall <i> in F:
		sum<j> in D: x[i, j] == 1;

# Suma de los tamaños de los archivos que entran en el disco $j$
subto c2:
	forall <j> in D:
		sum<i> in F: s[i] * x[i, j] <= d * y[j];
