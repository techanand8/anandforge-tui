// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vcounter.h for the primary calling header

#include "Vcounter__pch.h"
#include "Vcounter___024unit.h"

VL_ATTR_COLD void Vcounter___024unit___ctor_var_reset(Vcounter___024unit* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+  Vcounter___024unit___ctor_var_reset\n"); );
    Vcounter__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelf->__VmonitorNum = VL_RAND_RESET_Q(64);
    vlSelf->__VmonitorOff = VL_RAND_RESET_I(1);
}
