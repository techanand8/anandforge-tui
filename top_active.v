// Mayank Design
// SystemVerilog Full Adder 
// Designed by Mayank Anand
`timescale 1ns/1ps
module full_adder (
    input  logic a, b, cin,
    output logic sum, cout
);

    // Sum is the XOR of all inputs
    assign sum  = a ^ b ^ cin;
    
    // Carry out logic
    assign cout = (a & b) | (cin & (a ^ b));

endmodule