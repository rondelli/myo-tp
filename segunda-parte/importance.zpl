# Tamaño del disco
param d_t := read "b_1.in" as "1n" use 1 comment "#";
param d := d_t * 10**6;

# Conjunto de archivos f_{i} \forall i \in \{1, \ldots, n\}
set F := { read "b_1.in" as "<1s>" skip 2 comment "#" };

# Cantidad de archivos
param n := card(F);

# Tamaños de los archivos f_{i} \forall i \in \{1, \ldots, n\}
param s[F] := read "b_1.in" as "<1s> 2n" skip 2 comment "#";

# Importancias de los archivos
param importance[F] := read "b_1.in" as "<1s> 3n" skip 2 comment "#";

# 1 si el archivo $i$ está en el disco, 0 en caso contrario
var x[F] binary;

maximize importances: sum<i> in F: importance[i] * x[i];

# Suma de los tamaños de los archivos que entran en el disco
subto c1:
	sum<i> in F: s[i] * x[i] <= d;
