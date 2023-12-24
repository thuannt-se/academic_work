var x1, >= 0, integer;   /* Space Ray water gun */
var x2, >= 0, integer;   /* Zapper water fgun   */

maximize profit:
  8*x1 + 5*x2;

s.t. plastic:
  2*x1 + x2 <= 20;

s.t. production_time:
  3*x1 + 4*x2 <= 48;

s.t. total_production:
  x1 + x2 <= 14;

s.t. balanced_mix:
  x1 - x2 <= 7;

solve;

printf "\n------------------- Report ------------------\n";
printf "Profit           : %.2f\n", profit;
printf "\tSpace Ray: %.2f\n", x1;
printf "\tZapper   : %.2f\n", x2;
printf "Plastic          : %.2f\n", plastic;
printf "Production time  : %.2f\n", production_time;
printf "Total production : %.2f\n", total_production;
printf "Balanced mix     : %.2f\n", balanced_mix;
printf "---------------------------------------------\n";

end;
