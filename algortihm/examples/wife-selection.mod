var x, integer, >=0;
var y, integer, >=0;
var z, integer, >=0;

maximize houses:
  2*x + 3*y + 0*z;

s.t. hair:
  y = 0;
s.t. wedding_1:
  100*(1-x) + 1000*x >= 10;
s.t. wedding_2:
  100*(1-y) + 6*y    >= 10;
s.t. wedding_3:
  100*(1-z) + 0*z    >= 10;
s.t. one_wife:
  x + y + z = 1;

solve;

printf "Number of houses: %d\n", houses;
printf "x = %d\n", x;
printf "y = %d\n", y;
printf "z = %d\n", z;

end;
