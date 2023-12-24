set O;
param v{O};
param w{O};
param MaxW;

var x{O}, binary;

maximize value:
  sum{o in O} v[o]*x[o];

s.t. weight:
  sum{o in O} w[o]*x[o] <= MaxW;

solve;

printf{o in O}: "object %s = %d\n", o, x[o];
printf "Objective: %s\n", value;

data;

set O := a b c d;
param v := [a] 10 [b] 4 [c] 6 [d] 3;
param w := [a] 2 [b] 10 [c] 7 [d] 12;
param MaxW := 15;

end;
