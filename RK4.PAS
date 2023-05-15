const	NSmax	=	1;{number of equations} {x[number of value][order of deivative]}

type	RealType= {double} extended;

type	vectorX = array[1..NSmax,0..1] of RealType;
	ProcType = procedure(var x: vectorX; var t: RealType);

procedure	RK4(var x:vectorX; var t:RealType; h:RealType; NS:integer;syst:ProcType);
	type	vectorK = array[1..NSmax] of RealType;
	var	k1,k2,k3,k4,xk: vectorK;
	var	iNS: integer;
begin
	for iNS:=1 to NS do
		xk[iNS]:= x[iNS][0];

	syst(x,t);
	for iNS:=1 to NS do
	begin
		k1[iNS]:=x[iNS][1] * h;
		x[iNS][0]:= xk[iNS]+k1[iNS]*0.5;
	end;

	t:=t+0.5*h;
	syst(x,t);
	for iNS:=1 to NS do
	begin
		k2[iNS]:=x[iNS][1] * h;
		x[iNS][0]:= xk[iNS]+k2[iNS]*0.5;
	end;

	syst(x,t);
	for iNS:=1 to NS do
	begin
		k3[iNS]:=x[iNS][1] * h;
		x[iNS][0]:= xk[iNS]+k3[iNS];
	end;

	t:=t+0.5*h;
	syst(x,t);
	for iNS:=1 to NS do
	begin
		k4[iNS]:=x[iNS][1] * h;
		x[iNS][0]:= xk[iNS]+(k1[iNS]+2*k2[iNS]+2*k3[iNS]+k4[iNS])/6;
	end;
end;