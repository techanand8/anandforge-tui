// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vcounter.h for the primary calling header

#include "Vcounter__pch.h"
#include "Vcounter__Syms.h"
#include "Vcounter___024root.h"

VL_INLINE_OPT VlCoroutine Vcounter___024root___eval_initial__TOP__Vtiming__0(Vcounter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcounter___024root___eval_initial__TOP__Vtiming__0\n"); );
    Vcounter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSymsp->_vm_contextp__->dumpfile(std::string{"dump.vcd"});
    vlSymsp->_traceDumpOpen();
    VL_WRITEF_NX("\nFull Adder Simulation Started\nA B Cin | Sum Cout\n",0);
    vlSelfRef.full_adder_tb__DOT__a = 0U;
    vlSelfRef.full_adder_tb__DOT__b = 0U;
    vlSelfRef.full_adder_tb__DOT__cin = 0U;
    co_await vlSelfRef.__VdlySched.delay(0x2710ULL, 
                                         nullptr, "my_design_tb.v", 
                                         18);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    VL_WRITEF_NX("%b %b  %b  |  %b    %b\n",0,1,vlSelfRef.full_adder_tb__DOT__a,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__b),
                 1,vlSelfRef.full_adder_tb__DOT__cin,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__sum),
                 1,vlSelfRef.full_adder_tb__DOT__cout);
    vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i = 1U;
    vlSelfRef.full_adder_tb__DOT__a = 0U;
    vlSelfRef.full_adder_tb__DOT__b = 0U;
    vlSelfRef.full_adder_tb__DOT__cin = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x2710ULL, 
                                         nullptr, "my_design_tb.v", 
                                         18);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    VL_WRITEF_NX("%b %b  %b  |  %b    %b\n",0,1,vlSelfRef.full_adder_tb__DOT__a,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__b),
                 1,vlSelfRef.full_adder_tb__DOT__cin,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__sum),
                 1,vlSelfRef.full_adder_tb__DOT__cout);
    vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i = 2U;
    vlSelfRef.full_adder_tb__DOT__a = 0U;
    vlSelfRef.full_adder_tb__DOT__b = 1U;
    vlSelfRef.full_adder_tb__DOT__cin = 0U;
    co_await vlSelfRef.__VdlySched.delay(0x2710ULL, 
                                         nullptr, "my_design_tb.v", 
                                         18);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    VL_WRITEF_NX("%b %b  %b  |  %b    %b\n",0,1,vlSelfRef.full_adder_tb__DOT__a,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__b),
                 1,vlSelfRef.full_adder_tb__DOT__cin,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__sum),
                 1,vlSelfRef.full_adder_tb__DOT__cout);
    vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i = 3U;
    vlSelfRef.full_adder_tb__DOT__a = 0U;
    vlSelfRef.full_adder_tb__DOT__b = 1U;
    vlSelfRef.full_adder_tb__DOT__cin = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x2710ULL, 
                                         nullptr, "my_design_tb.v", 
                                         18);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    VL_WRITEF_NX("%b %b  %b  |  %b    %b\n",0,1,vlSelfRef.full_adder_tb__DOT__a,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__b),
                 1,vlSelfRef.full_adder_tb__DOT__cin,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__sum),
                 1,vlSelfRef.full_adder_tb__DOT__cout);
    vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i = 4U;
    vlSelfRef.full_adder_tb__DOT__a = 1U;
    vlSelfRef.full_adder_tb__DOT__b = 0U;
    vlSelfRef.full_adder_tb__DOT__cin = 0U;
    co_await vlSelfRef.__VdlySched.delay(0x2710ULL, 
                                         nullptr, "my_design_tb.v", 
                                         18);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    VL_WRITEF_NX("%b %b  %b  |  %b    %b\n",0,1,vlSelfRef.full_adder_tb__DOT__a,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__b),
                 1,vlSelfRef.full_adder_tb__DOT__cin,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__sum),
                 1,vlSelfRef.full_adder_tb__DOT__cout);
    vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i = 5U;
    vlSelfRef.full_adder_tb__DOT__a = 1U;
    vlSelfRef.full_adder_tb__DOT__b = 0U;
    vlSelfRef.full_adder_tb__DOT__cin = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x2710ULL, 
                                         nullptr, "my_design_tb.v", 
                                         18);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    VL_WRITEF_NX("%b %b  %b  |  %b    %b\n",0,1,vlSelfRef.full_adder_tb__DOT__a,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__b),
                 1,vlSelfRef.full_adder_tb__DOT__cin,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__sum),
                 1,vlSelfRef.full_adder_tb__DOT__cout);
    vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i = 6U;
    vlSelfRef.full_adder_tb__DOT__a = 1U;
    vlSelfRef.full_adder_tb__DOT__b = 1U;
    vlSelfRef.full_adder_tb__DOT__cin = 0U;
    co_await vlSelfRef.__VdlySched.delay(0x2710ULL, 
                                         nullptr, "my_design_tb.v", 
                                         18);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    VL_WRITEF_NX("%b %b  %b  |  %b    %b\n",0,1,vlSelfRef.full_adder_tb__DOT__a,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__b),
                 1,vlSelfRef.full_adder_tb__DOT__cin,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__sum),
                 1,vlSelfRef.full_adder_tb__DOT__cout);
    vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i = 7U;
    vlSelfRef.full_adder_tb__DOT__a = 1U;
    vlSelfRef.full_adder_tb__DOT__b = 1U;
    vlSelfRef.full_adder_tb__DOT__cin = 1U;
    co_await vlSelfRef.__VdlySched.delay(0x2710ULL, 
                                         nullptr, "my_design_tb.v", 
                                         18);
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
    VL_WRITEF_NX("%b %b  %b  |  %b    %b\n",0,1,vlSelfRef.full_adder_tb__DOT__a,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__b),
                 1,vlSelfRef.full_adder_tb__DOT__cin,
                 1,(IData)(vlSelfRef.full_adder_tb__DOT__sum),
                 1,vlSelfRef.full_adder_tb__DOT__cout);
    vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i = 8U;
    VL_WRITEF_NX("Simulation Finished\n\n",0);
    VL_FINISH_MT("my_design_tb.v", 23, "");
    vlSelfRef.__Vm_traceActivity[2U] = 1U;
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vcounter___024root___dump_triggers__act(Vcounter___024root* vlSelf);
#endif  // VL_DEBUG

void Vcounter___024root___eval_triggers__act(Vcounter___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcounter___024root___eval_triggers__act\n"); );
    Vcounter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered.setBit(0U, vlSelfRef.__VdlySched.awaitingCurrentTime());
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vcounter___024root___dump_triggers__act(vlSelf);
    }
#endif
}
