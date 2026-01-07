`timescale 1ns/1ps

// New Module
// 4-bit Synchronous Up/Down Counter
// Design by Mayank Anand
module counter (
    input clk,
    input reset,
    input mode,       // 1: Up, 0: Down
    output reg [3:0] q
);

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            q <= 4'b0000;
        end else begin
            if (mode)
                q <= q + 1;
            else
                q <= q - 1;
        end
    end

endmodule

// New Module
