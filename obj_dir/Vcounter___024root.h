// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vcounter.h for the primary calling header

#ifndef VERILATED_VCOUNTER___024ROOT_H_
#define VERILATED_VCOUNTER___024ROOT_H_  // guard

#include "verilated.h"
#include "verilated_timing.h"


class Vcounter__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vcounter___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    CData/*0:0*/ full_adder_tb__DOT__a;
    CData/*0:0*/ full_adder_tb__DOT__b;
    CData/*0:0*/ full_adder_tb__DOT__cin;
    CData/*0:0*/ full_adder_tb__DOT__sum;
    CData/*0:0*/ full_adder_tb__DOT__cout;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __VactContinue;
    IData/*31:0*/ full_adder_tb__DOT__unnamedblk1__DOT__i;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<CData/*0:0*/, 3> __Vm_traceActivity;
    VlDelayScheduler __VdlySched;
    VlTriggerVec<1> __VstlTriggered;
    VlTriggerVec<1> __VactTriggered;
    VlTriggerVec<1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vcounter__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vcounter___024root(Vcounter__Syms* symsp, const char* v__name);
    ~Vcounter___024root();
    VL_UNCOPYABLE(Vcounter___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
