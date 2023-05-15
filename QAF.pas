program
        Adaptive_rejection_part;

        uses
             Crt, math;

const   m=0.0008;
        n_step=2000;
        f_discr=1.0e+6;
        t_step=1/f_discr;
        f_noise1=50.0;
        f_noise2=100.0;
        f_noise3=150.0;
        two_pi=2*pi;
        rpt=1;

var
x, n, b :array [1..n_step] of real;
t : real;
s_data, s, c, y : real;
i, j, k, cycle :Integer;


data_file, source_file  :text;

Begin

        assign (source_file, '/home/gamma-dna/Pascal_programs/source.txt');
        assign (data_file, '/home/gamma-dna/Pascal_programs/data.txt');
        rewrite (data_file);
        reset (source_file);
        t:=0.0;
   for i:=1 to n_step do
                begin
                      n[i]:=cos(two_pi*f_noise1*t)
                      +sin(two_pi*f_noise2*t)+sin(two_pi*f_noise3*t);
                end;

      for i:=1 to n_step do b[i]:=0.0;
   for i:=1 to n_step do x[i]:=0.0;

        for cycle:=1 to rpt do begin
        rewrite (data_file);
        reset (source_file) ;

   i:=1; j:=1; k:=1; t:=0.0;

        while Not Eof(source_file) do
   begin
        s:=0;
             y:=0;

             for k:= n_step downto 2 do x[k]:=x[k-1];
             x[1]:=n[j];
             readln(source_file, s_data);

        for k:= 1 to n_step do y:=y+x[k]*b[k];

                if y>1.0 then y:= 1.0;
                if y<-1.0 then y:=-1.0;

                writeln(data_file, t, ' ', s);
                t:=t+t_step;
                c:=2*m*s;
                for k:= 1 to n_step do b[k]:=b[k]+x[k]*c;
                i:=i+1;
                if j=n_step then j:=1 else j:=j+1;
   end;
      end;


      Close(source_file);
      Close(data_file);
End.
