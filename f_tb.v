module f_tb;

reg a, b, cin;
wire sum, cout;

f uut (
    .a(a),
    .b(b),
    .cin(cin),
    .sum(sum),
    .cout(cout)
);

initial begin
    // GTKWave dump file
    $dumpfile("dump.vcd");
    $dumpvars(0, f_tb);
end

initial begin
    $display("A B Cin | Sum Cout");
    $display("------------------");

    a=0; b=0; cin=0; #10;
    a=0; b=0; cin=1; #10;
    a=0; b=1; cin=0; #10;
    a=0; b=1; cin=1; #10;
    a=1; b=0; cin=0; #10;
    a=1; b=0; cin=1; #10;
    a=1; b=1; cin=0; #10;
    a=1; b=1; cin=1; #10;

    $finish;
end

initial begin
    $monitor("%b %b  %b  |  %b    %b", a, b, cin, sum, cout);
end

endmodule
