/*---------------------------------------------------*/
/* partition a graph into a given number of clusters,
   to minimize inter-cluster communication           */
/*---------------------------------------------------*/

set VERTS;
set CLUSTERS;
set EDGES within {VERTS, VERTS};

/*-----------------------------------------------------------*/
/* decision variables are which cluster a vertex is assigned */
/*-----------------------------------------------------------*/
var x{VERTS,CLUSTERS} binary;
var y{EDGES} binary;

/*-------------------------------------------*/
/* objective: to minimize inter-cluster cost */
/*-------------------------------------------*/
minimize InterCost: 
  sum{(i,j) in EDGES} y[i,j];

/*----------------------------------*/
/* a node only belongs to a cluster */
/*----------------------------------*/
s.t. SOS{i in VERTS}:
  sum{c in CLUSTERS} x[i,c] = 1;

/*------------------------------------------------------------------------------*/
/* logic implication: if node i, j not the same cluster, there is inter-cluster */
/*------------------------------------------------------------------------------*/
s.t. InterCluster1{c in CLUSTERS, (i,j) in EDGES}:
  x[i,c] - x[j,c] <= y[i,j];
s.t. InterCluster2{c in CLUSTERS, (i,j) in EDGES}:
  x[j,c] - x[i,c] <= y[i,j];

/*--------------------------*/
/* cluster size constraints */
/*--------------------------*/
s.t. MinSize{c in CLUSTERS}:
  sum{i in VERTS} x[i,c] >= 2;
s.t. MaxSize{c in CLUSTERS}:
  sum{i in VERTS} x[i,c] <= 3;

/*-----------------*/
/* solve the model */
/*-----------------*/
solve;

/*------------------*/
/* print the report */
/*------------------*/
printf 'Graph partitioning result\n';
printf{i in VERTS, c in CLUSTERS: x[i,c] != 0}: 'Node %s is in cluster %s\n', i, c;
printf{(i,j) in EDGES: y[i,j] != 0}: '(%s,%s) is an inter-cluster edge\n', i, j;
printf 'Optimal inter-cluster cost: %s\n', InterCost;

/*--------------------*/
/* data for the model */
/*--------------------*/
data;

set CLUSTERS :=
  A
  B
  C;

set VERTS :=
  1
  2
  3
  4
  5
  6
  7
  8;

set EDGES :=
  1 2
  2 3
  2 5
  3 4
  3 5
  4 8
  5 6
  5 8
  6 7;

end;
