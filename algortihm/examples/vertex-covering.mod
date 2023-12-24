var xa, binary;
var xb, binary;
var xc, binary;
var xd, binary;
var xe, binary;
var xf, binary;
var xg, binary;
var xh, binary;
var xk, binary;

minimize Card:
  xa + xb + xc + xd + xe + xf + xg + xh + xk;
  
s.t. VertexCover_ab:
 xa + xb >= 1;
s.t. VertexCover_bd:
 xb + xd >= 1;
s.t. VertexCover_de:
 xd + xe >= 1;
s.t. VertexCover_dk:
 xd + xk >= 1;
s.t. VertexCover_ec:
 xe + xc >= 1;
s.t. VertexCover_ef:
 xe + xf >= 1;
s.t. VertexCover_eg:
 xe + xg >= 1;
s.t. VertexCover_eh:
 xe + xh >= 1;
s.t. VertexCover_kh:
 xk + xh >= 1;

solve;

display xa, xb, xc, xd, xe, xf, xg, xh, xk;

end;
