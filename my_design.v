`timescale 1ns/1ps

module full_adder (
    input  logic a,
    input  logic b,
    input  logic cin,
    output logic sum,
    output logic cout
);

    // Sum = A XOR B XOR Cin
    // Cout = (A & B) | (Cin & (A ^ B))
    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));

endmodule