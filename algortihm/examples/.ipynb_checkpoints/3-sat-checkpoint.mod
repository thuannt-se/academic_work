set I := {1,2,3,4};
var x{I} binary;

minimize dummy:
  sum{i in I} x[i];

s.t. clause_1:
  x[1] + x[2] + (1-x[3]) >= 1;

s.t. clause_2:
  x[1] + (1-x[2]) + (1-x[4]) >= 1;
s.t. clause_3:
  (1-x[1]) + x[3] + (1-x[4]) >= 1;
s.t. clause_4:
  x[2] + x[3] + x[4] >= 1;

solve;

printf{i in I} "x[%s] = %d\n", i, x[i];

end;
