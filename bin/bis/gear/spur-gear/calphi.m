%algorithm: Calculate phi for tolerance on the adjacent pitch
%author: Atharv Darekar
function phi = calphi (m,z) %function to calculate phi for tolerance on the adjacent pitch
  phi=m+0.25*sqrt(m*z);
endfunction
