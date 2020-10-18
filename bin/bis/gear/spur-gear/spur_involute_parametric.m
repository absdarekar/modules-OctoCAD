clear;
clc;
m=4; %module
z=18; %number of teeth
precision=0.01; %precision
alpha=20*pi/180; %pressure angle
r_b=m*z*cos(alpha)/2; %base circle radius
r_a=(m*z+2*m)/2; %addendum circle radius
r_f=(m*z-2*(1.157*m))/2; %dedendum circle radius
beta=pi/z;
c=r_a/r_b;
flag1=0;
x_m=0;
y=inline("c-cos(x)-x*sin(x)"); %equation to find intersection of involute curve and addendum circle
x_u=1;
x_l=0;
n=0.0000001; %required precision of solution
%bisection algorithm
if((y(c,x_u)*y(c,x_l))<0)
  flag1=1;
  x_m=(x_u+x_l)/2;
  while (abs(y(c,x_m))>=n)
    x_m=(x_u+x_l)/2;
    if ((y(c,x_l)*y(c,x_m))<=0)
      x_u=x_m;
    else
      x_l=x_m;
    endif
  endwhile
endif
t=0:precision:x_m; %parameters of involute curve
t=horzcat(t,x_m);
i=0;
k=1;
vectors_f=fopen("/home/ubuntu/.OctoCAD/spur-gear/vectors.py","w");
fprintf(vectors_f,"profile_involute_dedendum=[");
profile_addendum=[]; %initialising vector to store addendum end points
%involute profile
while(k<=z)
  points=length(t); %number of points calculated on the involute curve
  j=1;
  xR=r_b.*(cos(t-i*beta)+t.*sin(t-i*beta));
  yR=r_b.*(sin(t-i*beta)-t.*cos(t-i*beta));
  profile_addendum=vertcat(profile_addendum,horzcat(xR(points),yR(points)));
  while(j<=points)
    fprintf(vectors_f,"[%d,%d,0],",xR(j),yR(j));
    j++;
  endwhile
  fprintf(vectors_f,"[],");
  j=1;
  xL=r_b.*(cos(-t-(i+0.5)*beta)-t.*sin(-t-(i+0.5)*beta));
  yL=r_b.*(sin(-t-(i+0.5)*beta)+t.*cos(-t-(i+0.5)*beta));
  profile_addendum=vertcat(profile_addendum,horzcat(xL(points),yL(points)));
  while(j<=points)
    fprintf(vectors_f,"[%d,%d,0],",xL(j),yL(j));
    j++;
  endwhile
  fprintf(vectors_f,"[],");
  j=1;
  xD=xL(1):precision:xR(1);
  xD=horzcat(xD,xR(1));
  points=length(xD); %number of points calculated on the dedendum
  yD=(xD.-xR(1))*((yL(1)-yR(1))/(xL(1)-xR(1)))+yR(1);
  while(j<=points)
    if(points>1)
      fprintf(vectors_f,"[%d,%d,0],",xD(j),yD(j));
    endif
    j++;
  endwhile
  fprintf(vectors_f,"[],");
  j=1;
  xD=xR(1):precision:xL(1);
  xD=horzcat(xD,xL(1));
  points=length(xD); %number of points calculated on the dedendum
  yD=(xD.-xR(1))*((yL(1)-yR(1))/(xL(1)-xR(1)))+yR(1);
  while(j<=points)
    if(points>1)
      fprintf(vectors_f,"[%d,%d,0],",xD(j),yD(j));
    endif
    j++;
  endwhile
  fprintf(vectors_f,"[],");
  i+=2;
  k++;
endwhile
fprintf(vectors_f,"[]];");
fprintf(vectors_f,"\nprofile_addendum=[");
j=1;
while(j<=length(profile_addendum))
  fprintf(vectors_f,"[%d,%d,0],",profile_addendum(j,1),profile_addendum(j,2));
  j++;
endwhile
fprintf(vectors_f,"[]];");
fclose(vectors_f);
