param input := "IN/b_1.in"; # Path del archivo de input

# Tamaño del disco en terabytes
param d_t := read input as "1n" use 1 comment "#";
param d := d_t * 10**6;

# Conjunto de archivos f_{i} \forall i \in \{1, \ldots, n\}
set F := { read input as "<1s>" skip 2 comment "#" };

param n := card(F); # Cantidad de archivos

# Tamaños de los archivos f_{i} \forall i \in \{1, \ldots, n\}
param s[F] := read input as "<1s> 2n" skip 2 comment "#";

# Importancias de los archivos
param importance[F] := read input as "<1s> 3n" skip 2 comment "#";

# 1 si el archivo $i$ está en el disco, 0 en caso contrario
var x[F] binary;

maximize importances: sum<i> in F: importance[i] * x[i];

# Los archivos $i$ que entran en el disco
subto c1:
	sum<i> in F: s[i] * x[i] <= d;
