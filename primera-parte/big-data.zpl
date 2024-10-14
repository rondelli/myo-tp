# Disk size
param d_t := read "a_1.in" as "1n" use 1 comment "#";
param d := d_t * 10**6;

# Files f_{i} \forall i \in \{1, \ldots, n\}
set F := { read "a_1.in" as "<1s>" skip 2 comment "#" };

param n := card(F); # Number of files
param m := n; # Number of disks

# Disks
set D := { 1 .. m };

# File sizes of f_{i} \forall i \in \{1, \ldots, n\}
param s[F] := read "a_1.in" as "<1s> 2n" skip 2 comment "#";

var x[<i, j> in F * D] binary; #1 si el archivo i esta en el disco j
var y[D] binary; #1 si se esta usando el disco j

minimize number_of_disks: sum<j> in D: y[j];

subto c1:
	forall <i> in F:
		sum<j> in D: x[i, j] == 1; #cada archivo debe estar en un solo disco
subto c2:
	forall <j> in D:
		sum<i> in F: s[i] * x[i, j] <= d * y[j];
