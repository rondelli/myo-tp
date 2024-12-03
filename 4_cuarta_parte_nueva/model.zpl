# Path del archivo de input
param input := "IN/a_1.in";

# Tamaño del disco en terabytes
param d_t := read input as "1n" use 1 comment "#";
param d := d_t * 10**6;

# Conjunto de archivos f_{i} \forall i \in \{1, \ldots, n\}
set F := { read input as "<1s>" skip 2 comment "#" };

# Cantidad de archivos
param n := read input as "1n" skip 1 use 1 comment "#";

# Cantidad de discos, a lo sumo, un archivo por disco
param m := n;

# Conjunto de discos
set D := { 1 .. m };

# Conjunto de tamaños de archivos
set S := { read input as "<1s>" skip 2 comment "#" };
param q := card(S);

# Tamaños de los archivos f_{i} \forall i \in \{1, \ldots, n\}
param s[F] := read input as "<1s> 2n" skip 2 comment "#";

# Cantidad de archivos de tamaño $i$ en el disco $j$
var c[<i, j> in S * D] integer;

# 1 si se usa el disco $j$, 0 en caso contrario
var y[D] binary;

minimize disks: sum<j> in D: y[j];

# No puede haber discos usados con cero cantidad de archivos
subto c1:
	forall <i> in S:
		sum<j> in D: c[i, j] >= 1;

# La cantidad de archivos de tamaño $i$ que entran en el disco $j$
subto c2:
	forall <j> in D:
		sum<i> in S: s[i] * c[i, j] <= d * y[j];

subto c4:
	forall <i, j> in S * D:
		c[i, j] >= 0;
