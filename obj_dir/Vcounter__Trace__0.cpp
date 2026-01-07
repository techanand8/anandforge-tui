// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Tracing implementation internals
#include "verilated_vcd_c.h"
#include "Vcounter__Syms.h"


void Vcounter___024root__trace_chg_0_sub_0(Vcounter___024root* vlSelf, VerilatedVcd::Buffer* bufp);

void Vcounter___024root__trace_chg_0(void* voidSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcounter___024root__trace_chg_0\n"); );
    // Init
    Vcounter___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vcounter___024root*>(voidSelf);
    Vcounter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    if (VL_UNLIKELY(!vlSymsp->__Vm_activity)) return;
    // Body
    Vcounter___024root__trace_chg_0_sub_0((&vlSymsp->TOP), bufp);
}

void Vcounter___024root__trace_chg_0_sub_0(Vcounter___024root* vlSelf, VerilatedVcd::Buffer* bufp) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcounter___024root__trace_chg_0_sub_0\n"); );
    Vcounter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Init
    uint32_t* const oldp VL_ATTR_UNUSED = bufp->oldp(vlSymsp->__Vm_baseCode + 1);
    // Body
    if (VL_UNLIKELY(((vlSelfRef.__Vm_traceActivity[1U] 
                      | vlSelfRef.__Vm_traceActivity
                      [2U])))) {
        bufp->chgBit(oldp+0,(vlSelfRef.full_adder_tb__DOT__a));
        bufp->chgBit(oldp+1,(vlSelfRef.full_adder_tb__DOT__b));
        bufp->chgBit(oldp+2,(vlSelfRef.full_adder_tb__DOT__cin));
        bufp->chgBit(oldp+3,((1U & (((IData)(vlSelfRef.full_adder_tb__DOT__a) 
                                     + (IData)(vlSelfRef.full_adder_tb__DOT__b)) 
                                    + (IData)(vlSelfRef.full_adder_tb__DOT__cin)))));
        bufp->chgBit(oldp+4,((1U & ((((IData)(vlSelfRef.full_adder_tb__DOT__a) 
                                      + (IData)(vlSelfRef.full_adder_tb__DOT__b)) 
                                     + (IData)(vlSelfRef.full_adder_tb__DOT__cin)) 
                                    >> 1U))));
        bufp->chgIData(oldp+5,(vlSelfRef.full_adder_tb__DOT__unnamedblk1__DOT__i),32);
    }
}

void Vcounter___024root__trace_cleanup(void* voidSelf, VerilatedVcd* /*unused*/) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vcounter___024root__trace_cleanup\n"); );
    // Init
    Vcounter___024root* const __restrict vlSelf VL_ATTR_UNUSED = static_cast<Vcounter___024root*>(voidSelf);
    Vcounter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    // Body
    vlSymsp->__Vm_activity = false;
    vlSymsp->TOP.__Vm_traceActivity[0U] = 0U;
    vlSymsp->TOP.__Vm_traceActivity[1U] = 0U;
    vlSymsp->TOP.__Vm_traceActivity[2U] = 0U;
}
