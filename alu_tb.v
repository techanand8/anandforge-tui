// New Module
`timescale 1ns / 1ps

module alu_tb;
    // Inputs
    reg [3:0] A, B;
    reg [2:0] Sel;
    // Outputs
    wire [7:0] Out;
    wire Carry;

    // Instantiate the Unit Under Test (UUT)
    alu uut (
        .A(A), 
        .B(B), 
        .ALU_Sel(Sel), 
        .ALU_Out(Out), 
        .CarryOut(Carry)
    );

    initial begin
        // Required for GTKWave visualization
        $dumpfile("dump.vcd");
        $dumpvars(0, alu_tb);

        // Test Addition
        A = 4'd10; B = 4'd5; Sel = 3'b000; #10;
        
        // Test Subtraction
        A = 4'd15; B = 4'd5; Sel = 3'b001; #10;
        
        // Test Multiplication
        A = 4'd3; B = 4'd4; Sel = 3'b010; #10;
        
        // Test Logical AND
        A = 4'b1010; B = 4'b1100; Sel = 3'b100; #10;
        
        // Test Logical XOR
        A = 4'b1010; B = 4'b1100; Sel = 3'b111; #10;

        $display("ALU Testing Finished");
        $finish;
    end
endmodule