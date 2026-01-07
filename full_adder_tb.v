// Mayank Design - Full Adder Testbench
module full_adder_tb();
    reg a, b, cin;
    wire sum, cout;

    // Instantiate the Unit Under Test (UUT)
    full_adder uut (
        .a(a), 
        .b(b), 
        .cin(cin), 
        .sum(sum), 
        .cout(cout)
    );

    initial begin
        // Setup waveform dumping
        $dumpfile("dump.vcd"); 
        $dumpvars(0, full_adder_tb);

        // --- Table Header ---
        $display("\n-------------------------------");
        $display(" TIME | A B Cin | SUM COUT ");
        $display("-------------------------------");

        // --- Tabular Monitor ---
        // %0t: time, %b: binary
        $monitor("%5t | %b %b  %b  |  %b    %b", $time, a, b, cin, sum, cout);

        // --- Test Vectors ---
        {a, b, cin} = 3'b000; #10;
        {a, b, cin} = 3'b001; #10;
        {a, b, cin} = 3'b010; #10;
        {a, b, cin} = 3'b011; #10;
        {a, b, cin} = 3'b100; #10;
        {a, b, cin} = 3'b101; #10;
        {a, b, cin} = 3'b110; #10;
        {a, b, cin} = 3'b111; #10;

        $display("-------------------------------");
        $display("Full Adder Simulation Finished");
        $finish;
    end
endmodule