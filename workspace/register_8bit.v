// Mayank Anand's VLSI IDE - Sample Design
// 8-bit Register with Async Reset

module register_8bit (
    input wire clk,
    input wire rst_n,
    input wire [7:0] data_in,
    output reg [7:0] data_out
);
    
    // Register with asynchronous active-low reset
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            data_out <= 8'b0000_0000;
        end else begin
            data_out <= data_in;
        end
    end
    
endmodule
