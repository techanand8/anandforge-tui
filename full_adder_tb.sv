// Mayank Design
`timescale 1ns/1ps

module full_adder_tb;
    // Signals for testing
    logic a, b, cin;
    logic sum, cout;

    // Instantiate the Full Adder using implicit port connection (.*)
    full_adder uut (.*);

    initial begin
        // Waveform stuffer setup
        $dumpfile("dump.vcd");
        $dumpvars(0, full_adder_tb);

        $display("A B Cin | Sum Cout");
        $display("------------------");

        // Test all 8 binary combinations (000 to 111)
        for (int i = 0; i < 8; i++) begin
            {a, b, cin} = i[2:0];
            #10; // Wait 10ns between steps
            $display("%b %b  %b  |  %b    %b", a, b, cin, sum, cout);
        end

        $display("------------------");
        $display("Verification Complete!");
        $finish;
    end
endmodule