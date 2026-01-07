// Traffic Light Controller FSM by Mayank Anand (Fixed Version)
module traffic_fsm (
    input  logic clk,
    input  logic reset,
    output logic [2:0] lights // [Red, Yellow, Green]
);

    // Define States
    typedef enum logic [1:0] {
        GREEN  = 2'b00,
        YELLOW = 2'b01,
        RED    = 2'b10
    } state_t;

    state_t current_state, next_state;
    logic [3:0] timer;

    // State Transition Logic
    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            current_state <= RED;
            timer <= 0;
        end else begin
            if (timer == 4'd10) begin 
                current_state <= next_state;
                timer <= 0;
            end else begin
                timer <= timer + 1;
            end
        end
    end

    // Next State Logic
    always_comb begin
        case (current_state)
            GREEN:  next_state = YELLOW;
            YELLOW: next_state = RED;
            RED:    next_state = GREEN;
            default: next_state = RED;
        endcase
    end

    // Output Logic - FIXED BIT WIDTHS
    always_comb begin
        case (current_state)
            GREEN:  lights = 3'b001; // Green ON
            YELLOW: lights = 3'b010; // Yellow ON
            RED:    lights = 3'b100; // Red ON (Binary 4)
            default: lights = 3'b100;
        endcase
    end

endmodule
// Ensure there is a blank line here at the end!
