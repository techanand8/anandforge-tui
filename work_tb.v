`timescale 1ns/1ps

module full_adder_tb;
    logic a, b, cin;
    logic sum, cout;

    full_adder uut (.*); // SystemVerilog dot-star connection

    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, full_adder_tb);

        $display("\nFull Adder Simulation Started");
        $display("A B Cin | Sum Cout");
        
        for (int i = 0; i < 8; i++) begin
            {a, b, cin} = i;
            #10;
            $display("%b %b  %b  |  %b    %b", a, b, cin, sum, cout);
        end
        
        $display("Simulation Finished\n");
        $finish;
    end
endmodule