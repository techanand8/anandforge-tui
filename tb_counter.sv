`timescale 1ns/1ps

module full_adder_tb;
    // Internal signals (logic type replaces reg/wire)
    logic a, b, cin;
    logic sum, cout;

    // Instantiate the Full Adder using implicit port mapping
    full_adder uut (.*);

    initial begin
        // Waveform setup for Surfer/GTKWave in AnandForge
        $dumpfile("dump.vcd");
        $dumpvars(0, full_adder_tb);

        // Header for the console
        $display("Time\t A B Cin | Sum Cout");
        $monitor("%0t\t %b %b  %b  |  %b    %b", $time, a, b, cin, sum, cout);

        // Test all 8 binary combinations
        {a, b, cin} = 3'b000; #10;
        {a, b, cin} = 3'b001; #10;
        {a, b, cin} = 3'b010; #10;
        {a, b, cin} = 3'b011; #10;
        {a, b, cin} = 3'b100; #10;
        {a, b, cin} = 3'b101; #10;
        {a, b, cin} = 3'b110; #10;
        {a, b, cin} = 3'b111; #10;

        $display("Full Adder Test Complete, Mayank!");
        $finish;
    end

endmodule