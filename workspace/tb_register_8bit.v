`timescale 1ns/1ps

// Testbench for 8-bit Register
module tb_register_8bit;
    
    // Test signals
    reg clk = 0;
    reg rst_n = 0;
    reg [7:0] data_in = 8'h00;
    wire [7:0] data_out;
    
    // Clock generation (100 MHz)
    always #5 clk = ~clk;
    
    // Instantiate DUT
    register_8bit dut (
        .clk(clk),
        .rst_n(rst_n),
        .data_in(data_in),
        .data_out(data_out)
    );
    
    // Initialize waveform dump
    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, tb_register_8bit);
        $display("[%0t] Starting simulation...", $time);
    end
    
    // Test sequence
    initial begin
        // Initial reset
        rst_n = 0;
        data_in = 8'h00;
        #20;
        
        // Release reset
        rst_n = 1;
        $display("[%0t] Reset released", $time);
        
        // Test data sequence
        for (int i = 1; i <= 10; i = i + 1) begin
            data_in = i * 8'h11;
            @(posedge clk);
            #1; // Small delay for display
            $display("[%0t] data_in=0x%02h, data_out=0x%02h", 
                     $time, data_in, data_out);
            #19;
        end
        
        // End simulation
        #100;
        $display("[%0t] Simulation completed successfully!", $time);
        $finish;
    end
    
endmodule
