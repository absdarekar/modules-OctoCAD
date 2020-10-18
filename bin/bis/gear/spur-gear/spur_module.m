%algorithm: Finds module of spur gear from preferred series by iteration
%author: Atharv Darekar
function [Fd, Fap, Fag, Fw, BHN, m, FOS, zp, zg] = spur_module (Sutp,Sutg,Ep,Eg,zp,zg,grade,y,P,Np,Q,FOSr,cs) %function to finds module of spur gear from preferred series by iteration
  mi=[1,1.125,1.25,1.375,1.5,1.75,2,2.25,2.5,2.75,3,3.5,4,4.5,5,5.5,6,6.5,7,8,9,10,11,12,14,16,18,20,22,25,28,32,36,40,45,50]; %specified values of module
  %Sutp=ultimate tensile strength of pinion N.mm^-2
  %Sutg=ultimate tensile strength of gear N.mm^-2
  %Ep=modulus of elasticity of pinion N.mm^-2
  %Eg=modulus of elasticity of gear N.mm^-2
  %zp=pinion teeth
  %zg=gear teeth
  %grade=grade of gear
  %y=Lewis form factor
  %P=power transmitted by gear W
  %Np=speed of pinion rpm
  %Q=type of gearing
  %FOSr=factor of safety required
  %cs=service factor
  switch (Q)
    case 1
    Q=(2*(zg/zp))/((zg/zp)-1);
    case 2
    Q=(2*(zg/zp))/((zg/zp)+1);
  endswitch
  sigmabp=1/3*Sutp; %allowable bendig stress of pinion N.mm^-2
  sigmabg=1/3*Sutg; %allowable bendig stress of gear N.mm^-2
  switch (y)
    case 1
      yp=0.124-(0.684/zp);
      yg=0.124-(0.684/zg);
      alpha=14.5; %pressure angle degree
      k=0.107;
    case 2
      yp=0.154-(0.912/zp);
      yg=0.154-(0.912/zg);
      alpha=20; %pressure angle degree
      k=0.111;
    case 3
      yp=0.175-(0.95/zp);
      yg=0.175-(0.95/zg);
      alpha=20; %pressure angle degree
      k=0.115;
  endswitch
  c=k/((1/Ep)+(1/Eg)); %deformation factor
  FOS=0; %factor of safety available
  i=1; %counter variable for module row matrix
  while (FOSr>=FOS)
    [Fap, Fag, FOS, Fd]=spur_load(mi(i),sigmabp,sigmabg,yp,yg,zp,zg,Np,P,grade,c,cs); %function call to calculate bendig load and effective load iteratively for each module in preferred series
    i++;
  endwhile
  [Fap, Fag, FOS, Fd]=spur_load(mi(i-1),sigmabp,sigmabg,yp,yg,zp,zg,Np,P,grade,c,cs); %function call to calculate bendig load and effective load for the required module
  Fw=Fd*FOSr;
  sigmab=sqrt((Fw/(10*zp*(mi(i-1)^2)*Q))*(1.4/(sind(alpha)*cosd(alpha)*((1/Ep)+(1/Eg)))));
  BHN=sigmab/2.65;
  m=mi(i-1);
endfunction
