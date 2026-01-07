// 4-bit Up-Counter by Mayank Anand
module counter (
    input clk,              // Clock signal
    input reset,            // Asynchronous reset (Active High)
    input load,             // Load enable
    input [3:0] load_data,  // Data to load
    output reg [3:0] count  // 4-bit output
);

    always @(posedge clk or posedge reset) begin
        if (reset) begin
            count <= 4'b0000;      // Reset count to zero
        end else if (load) begin
            count <= load_data;    // Load specific value
        end else begin
            count <= count + 1;    // Increment count
        end
    end

endmodule