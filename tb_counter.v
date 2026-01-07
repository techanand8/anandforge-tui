`timescale 1ns / 1ps

module counter_tb;
    reg clk;
    reg reset;
    reg load;
    reg [3:0] load_data;
    wire [3:0] count;

    // Instantiate the counter
    counter uut (
        .clk(clk),
        .reset(reset),
        .load(load),
        .load_data(load_data),
        .count(count)
    );

    // Clock generation (10ns period)
    always #5 clk = ~clk;

    initial begin
        // --- Tabular Header ---
        $display("\n-------------------------------------------");
        $display(" TIME | RESET | LOAD | LOAD_DATA | COUNT ");
        $display("-------------------------------------------");
        
        // --- Monitor Signal Changes ---
        $monitor("%5t |   %b   |  %b   |    %h     |   %h", 
                 $time, reset, load, load_data, count);

        // Initialize signals
        clk = 0; reset = 1; load = 0; load_data = 0;

        $dumpfile("dump.vcd");
        $dumpvars(0, counter_tb);

        #12 reset = 0;       // Release reset
        #50;                 // Let it count
        
        load_data = 4'b1101; // Data = D (13 in hex)
        load = 1; #10;       // Load it
        load = 0;            // Resume counting
        
        #40;
        $display("-------------------------------------------");
        $display("Counter Simulation Finished");
        $finish;
    end
endmodule