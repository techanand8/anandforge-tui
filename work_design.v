module full_adder_sv (
    input  logic a,
    input  logic b,
    input  logic cin,
    output logic sum,
    output logic cout
);
    // Dataflow modeling using logic types
    always_comb begin
        {cout, sum} = a + b + cin;
    end

endmodule