`timescale 1ns/1ps

module full_adder (
    input  logic a,
    input  logic b,
    input  logic cin,
    output logic sum,
    output logic cout
);

    // Using SystemVerilog always_comb for synthesis-safe combinational logic
    always_comb begin
        // Concatenation operator allows calculating sum and carry in one line
        {cout, sum} = a + b + cin;
    end

endmodule