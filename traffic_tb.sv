`timescale 1ns / 1ps

module traffic_tb;
    logic clk;
    logic reset;
    logic [2:0] lights;

    // Instantiate Design
    traffic_fsm uut (.*);

    // Clock Generation
    always #5 clk = ~clk;

    initial begin
        $display("\n-------------------------------------------");
        $display(" TIME | RESET | LIGHTS (R Y G) | STATE ");
        $display("-------------------------------------------");
        
        // Monitor the outputs
        $monitor("%5t |   %b   |      %b       | %s", 
                 $time, reset, lights, uut.current_state.name());

        clk = 0; reset = 1;
        $dumpfile("dump.vcd");
        $dumpvars(0, traffic_tb);

        #15 reset = 0;
        
        // Run long enough to see multiple cycles (10 cycles per state * 3 states * 10ns)
        #400;

        $display("-------------------------------------------");
        $display("FSM Simulation Finished");
        $finish;
    end
endmodule