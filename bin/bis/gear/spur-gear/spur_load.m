%algorithm: Calculate bendig load and effective load on spur gear
%author: Atharv Darekar
function [Fap, Fag, FOS, Fd] = spur_load (m,sigmabp,sigmabg,yp,yg,zp,zg,Np,P,grade,c,cs) %function to calculate bendig load and effective load on spur gear
  b=10*m; %face width mm
  Pc=3.1416*m; %circular pitch of pinion mm
  Fap=sigmabp*b*yp*Pc; %bendig load capacity of pinion
  Fag=sigmabg*b*yg*Pc; %bendig load capacity of gear
  if(Fap<Fag) %lowest bendig load capacity
    Fa=Fap;
  else
    Fa=Fag;
  endif
  v=3.1416*zp*m*Np/(60*1000); %pitch line velocity m.s^-1
  Ft=P/v; %tangential load
  switch (grade) %tolerance on the adjacent pitch
    case 1
      ep=0.8+0.06*calphi(m,zp);
      eg=0.8+0.06*calphi(m,zg);
      e=(ep+eg)*10^-3;
    case 2
      ep=1.25+0.10*calphi(m,zp);
      eg=1.25+0.10*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 3
      ep=2.00+0.16*calphi(m,zp);
      eg=2.00+0.16*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 4
      ep=3.20+0.25*calphi(m,zp);
      eg=3.20+0.25*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 5
      ep=5.00+0.40*calphi(m,zp);
      eg=5.00+0.40*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 6
      ep=8.00+0.63*calphi(m,zp);
      eg=8.00+0.63*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 7
      ep=11.00+0.90*calphi(m,zp);
      eg=11.00+0.90*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 8
      ep=16.00+1.25*calphi(m,zp);
      eg=16.00+1.25*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 9
      ep=22.00+1.80*calphi(m,zp);
      eg=22.00+1.80*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 10
      ep=32.00+2.50*calphi(m,zp);
      eg=32.00+2.50*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 11
      ep=45.00+3.55*calphi(m,zp);
      eg=45.00+3.55*calphi(m,zg);
      e=(ep+eg)*10^-3;
     case 12
      ep=63.00+5.00*calphi(m,zp);
      eg=63.00+5.00*calphi(m,zg);
      e=(ep+eg)*10^-3;
  endswitch
  Fd=cs*Ft+((21*v*(c*e*b+Ft))/(21*v+sqrt(c*e*b+Ft)));
  FOS=Fa/Fd;
endfunction