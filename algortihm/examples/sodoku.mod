set ROWS := {1..9};
set COLS := {1..9};
set INDICATORS := {1..9};
var x{ROWS,COLS,INDICATORS} binary;
param KNOWN_VALUES{ROWS,COLS};

maximize somecost:
  sum{i in ROWS} sum{j in COLS} sum{k in INDICATORS} x[i,j,k];

s.t. one_value{i in ROWS, j in COLS}:
  sum{k in INDICATORS} x[i,j,k] = 1;

s.t. one_on_row{i in ROWS, k in INDICATORS}:
  sum{j in COLS} x[i,j,k] = 1;

s.t. one_on_columns{j in COLS, k in INDICATORS}:
  sum{i in ROWS} x[i,j,k] = 1;

s.t. one_on_block{i in {0,3,6}, j in {0,3,6}, k in INDICATORS}:
  sum{m in 1..3} sum{n in 1..3} x[i+m,j+n,k] = 1;

s.t. known_values{i in ROWS, j in COLS: KNOWN_VALUES[i,j] != -1}:
  x[i,j,KNOWN_VALUES[i,j]] = 1;

solve;

for{ i in ROWS }{
  for{ j in COLS }{
    printf "%s ", if ( KNOWN_VALUES[i,j] != -1 ) then '-' 
      else sum{k in INDICATORS} k*x[i,j,k];
  }
  printf "\n";
}

data;

param KNOWN_VALUES:  1  2  3  4  5  6  7  8  9 :=
                  1 -1 -1  8  6 -1 -1 -1 -1  3
                  2 -1  5 -1 -1  9 -1 -1  6 -1
                  3  9 -1 -1 -1 -1  4  7 -1 -1
                  4  4 -1 -1 -1 -1  3  1 -1 -1
                  5 -1  3 -1 -1  1 -1 -1  8 -1
                  6 -1 -1  1  8 -1 -1 -1 -1  9
                  7 -1 -1  7  3 -1 -1 -1 -1  6
                  8 -1  2 -1 -1  8 -1 -1  3 -1
                  9  8 -1 -1 -1 -1  9  5 -1 -1;

end;
