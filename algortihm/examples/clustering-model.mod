set POINTS;
param X{POINTS};
param Y{POINTS};
table data IN "CSV" "test.csv" :
  POINTS <- [RECNO], X~x, Y~y;
param d{i in POINTS, j in POINTS} := sqrt( (X[i]-X[j])*(X[i]-X[j]) + (Y[i]-Y[j])*(Y[i]-Y[j]) );

set CLUSTERS := {1..3};

var y{POINTS,POINTS,CLUSTERS}, binary;
var x{POINTS,CLUSTERS}, binary;

minimize intracost:
  sum{i in POINTS, j in POINTS: j >= i+1} sum{k in CLUSTERS} y[i,j,k]*d[i,j];

s.t. intrarel{i in POINTS, j in POINTS, k in CLUSTERS: i != j}:
  x[i,k] + x[j,k] - y[i,j,k] <= 1;
s.t. C1{i in POINTS, j in POINTS, k in CLUSTERS}:
  y[i,j,k] - x[i,k] <= 0;
s.t. C2{i in POINTS, j in POINTS, k in CLUSTERS}:
  y[i,j,k] - x[j,k] <= 0;
s.t. setpart{i in POINTS}:
  sum{k in CLUSTERS} x[i,k] = 1;

solve;

printf 'Intra cost: %.2f\n', intracost;
printf {i in POINTS, k in CLUSTERS: x[i,k] != 0}: 'Point %d (%.2f,%.2f) in %d (x=%.2f)\n', 
  i, X[i], Y[i], k, x[i,k];
printf {k in CLUSTERS}: '%.2f\t%.2f\n',
  (sum{i in POINTS: x[i,k] != 0} X[i]) / (sum{i in POINTS} x[i,k]),
  (sum{i in POINTS: x[i,k] != 0} Y[i]) / (sum{i in POINTS} x[i,k]);
end;
