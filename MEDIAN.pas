program
	 Median_Data_filtration;


	uses
		Crt, math;
const
        sfreq=10000000;
        h=1/sfreq;
        window=5000;
        L=533542;

var
i, j                            :longint;
t, x                               :real;
s                               :array [1..L] of Real;
data_file, source_file          :text;


Begin
        assign (source_file, 'e:\science\drift\drift_ch1.dat');
        assign (data_file, 'e:\science\drift\nodrift_ch1.dat');
        reset(source_file);
        rewrite (data_file);

        t:=0.0;
        x:=0;

        for i:=1 to L do
	begin
                read(source_file, s[i]);
        end;

        for i:=0 to L-window do
	begin
             for j:=1 to window do
                begin
                       x:=x+s[i+j];
                end;
                x:=x/window;
                s[i+1]:=s[i+1]-x;
                writeln (data_file, t, ' ', s[i+1]);
                x:=0;
                t:=t+h;
        end;


        Close(source_file);
        Close(data_file);
End.
