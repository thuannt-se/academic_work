/* variables (=literals) */
set I := {1, 2, 3, 4};
var x{I} binary;

/* dummy objective */
minimize dummy_obj:
  sum{i in I} x[i];

/* clauses */
s.t. clause_1:
  ( 1 - x[1] ) + x[2] >= 1;
s.t. clause_2:
  x[1] + x[2] >= 1;
s.t. clause_3:
  ( 1 - x[2] ) + x[3] >= 1;
s.t. clause_4:
  x[3] + ( 1 - x[4] ) >= 1;
s.t. clause_5:
  x[1] + ( 1 - x[2] ) >= 1;

/* find a valuation of being satisfiable */
solve;

/* print the valuation */
printf{i in I} "x_%s = %d\n", i, x[i];

end; 
