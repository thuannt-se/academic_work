/* shortest path problem */
set VERTS;
set EDGES within {VERTS,VERTS};
param weight{EDGES};
param SOURCE in VERTS;
param DESTINATION in VERTS;

/* decision variables to be on path or not */
var x{EDGES} binary;

/* objective as shortest length */
minimize length:
  sum{(i,j) in EDGES} weight[i,j] * x[i,j];

/* constraints */
s.t. Conservative{ v in VERTS: v != SOURCE && v != DESTINATION }:
  (sum{(i,j) in EDGES: j == v} x[i,j]) - (sum{(i,j) in EDGES: i == v} x[i,j]) = 0;

s.t. SourceOut:
  sum{(i,j) in EDGES: i == SOURCE} x[i,j] = 1;

s.t. DestinationIn:
  sum{(i,j) in EDGES: j == DESTINATION} - x[i,j] = -1;

s.t. NoHops:
  sum{(i,j) in EDGES} x[i,j] <= 3;

/* solve the problem */
solve;

/* print report */
printf 'Shortest path length: %s\n', length;
printf{ (i,j) in EDGES: x[i,j] != 0 }: '\tEdge (%s,%s) in shortest path\n', i, j;

/* data for the model */
data;

set VERTS :=
  1
  2
  3
  4
  5
  6
  7
  8;
param SOURCE := 1;
param DESTINATION := 8;

set EDGES :=
  1 2
  1 3
  2 5
  2 6
  3 4
  3 5
  4 5
  4 7
  5 7
  6 7
  6 8
  7 8;

param: weight :=
  1 2 100
  1 3 151
  2 5 75
  2 6 150
  3 4 67
  3 5 42
  4 5 22
  4 7 89
  5 7 11
  6 7 25
  6 8 71
  7 8 52;

end;
