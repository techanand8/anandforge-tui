// New Module
// 4-bit ALU Design by Mayank Anand
module alu (
    input  [3:0] A, B,      // 4-bit Inputs
    input  [2:0] ALU_Sel,   // 3-bit Operation Select
    output reg [7:0] ALU_Out, // 8-bit Output (to handle multiplication)
    output CarryOut         // Carry Flag
);
    always @(*) begin
        case(ALU_Sel)
            3'b000: ALU_Out = A + B;        // Addition
            3'b001: ALU_Out = A - B;        // Subtraction
            3'b010: ALU_Out = A * B;        // Multiplication
            3'b011: ALU_Out = A / B;        // Division
            3'b100: ALU_Out = A & B;        // Logical AND
            3'b101: ALU_Out = A | B;        // Logical OR
            3'b110: ALU_Out = ~(A & B);     // Logical NAND
            3'b111: ALU_Out = A ^ B;        // Logical XOR
            default: ALU_Out = A + B;
        endcase
    end
    // CarryOut logic for addition
    assign CarryOut = (ALU_Sel == 3'b000) ? (A + B > 15) : 1'b0;
endmodule