set WOMEN;
var x{WOMEN}, binary;

param houses{WOMEN}, integer, >= 0;  /* number of houses         */
param weddingtime{WOMEN}, >= 0;      /* maximum month to wedding */
set hairs{WOMEN};
set lovedhairs;
param maxwives;
param minweddingtime;

maximize maxhouses:
  sum{w in WOMEN} houses[w] * x[w];

s.t. c_lovedhairs{w in WOMEN: card( hairs[w] inter lovedhairs ) == 0 }:
  x[w] = 0;
s.t. c_minweddingtime{w in WOMEN}:
  100*(1-x[w]) + weddingtime[w]*x[w] >= minweddingtime;
s.t. c_maxwives:
  sum{w in WOMEN} x[w] <= maxwives;

solve;

printf "Number of houses: %d\n", maxhouses;
printf{w in WOMEN: x[w] != 0}: "\tmarry: %s\n", w;

data;

set WOMEN :=
  A B C D E F G H I J K;
param maxwives := 4;
param minweddingtime := 1;
param: houses :=
  A  2
  B  3
  C  0
  D  3
  E  2
  F  8
  G  1
  H  7
  I  3
  J  5
  K  4;
param: weddingtime :=
  A  1000
  B  6
  C  0
  D  12
  E  13
  F  4
  G  11
  H  9
  I  10
  J  7
  K  15;

set lovedhairs := red yellow;
set hairs[A] := green yellow;
set hairs[B] := yellow;
set hairs[C] := red;
set hairs[D] := blue;
set hairs[E] := green;
set hairs[F] := yellow;
set hairs[G] := green yellow blue;
set hairs[H] := brown pink red;
set hairs[I] := green;
set hairs[J] := yellow;
set hairs[K] := violet;

end;
