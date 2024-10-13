param d := read "a1.in" as "1n" use 1 skip 1; #d disk capacity

param n := read "a1.in" as "1n" use 1 skip 4; #n number of files

set files := { read "a1.in" as "<1s>" skip 7 };
param size[files] := read "a1.in" as "<1s> 2n" skip 7;

set I := {1..n};  
set J := {1..n};  

var F[I][J] binary; #1 si el archivo i esta en el disco j

var D[J] binary; #1 si se esta usando el disco j

minimize discos: sum <j> in J : D[j];

subto c1: 
	forall <i> in I: 
		(sum <j> in J: F[i][j]) = 1; #cada archivo debe estar en un solo disco

subto c2: 
	forall <j> in J:
		sum <i> in I: size[i] * F[i][j] <= d * D[J];
