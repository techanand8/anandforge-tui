# 🛠️ AnandForge-TUI
**A Modular Terminal Workstation for VLSI Design & Verification**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tools: iVerilog | Yosys](https://img.shields.io/badge/Tools-iVerilog%20%7C%20Yosys-blue)](https://github.com/techanand8/anandforge-tui)

AnandForge-TUI is a high-performance terminal cockpit designed to bridge the gap between RTL coding and hardware verification. It unifies simulation, synthesis, and signal monitoring into a single, keyboard-driven interface.

---

## 🚀 Key Features

* **Integrated EDA Flow:** Execute **iVerilog** simulations and **Yosys** gate-level synthesis with a single keystroke.
* **Tabular Monitor System:** A custom verification dashboard that displays real-time signal states for components like 4-bit counters and full adders.
* **Zero-Switching Workflow:** Monitor synthesis logs and simulation results in side-by-side TUI panes.
* **Extensible Architecture:** Modular backend designed to scale. **Verilator** and **OpenROAD** integration coming soon.

## 🖥️ TUI Layout Preview

```text
+-------------------------------------------------------------+
| AnandForge-TUI v1.0                     [Status: Synthesis] |
+---------------------------+---------------------------------+
| [ File: counter_4bit.v ]  |      [ Tabular Monitor ]        |
|                           |                                 |
| 1: module counter(        |  TIME  | CLK | RST | EN | COUNT | |
| 2:   input clk, rst,      |  00ns  |  0  |  1  | 0  |  0000 | |
| 3:   output [3:0] out     |  10ns  |  1  |  0  | 1  |  0001 | |
| 4: );                     |  20ns  |  0  |  0  | 1  |  0001 | |
+---------------------------+---------------------------------+
| [ Log: Yosys Synthesis ]                                    |
|  Generating RTLIL representation for module `\counter'.     |
|  Finished mapping to gate-level cells.                      |
+-------------------------------------------------------------+
| [S] Synthesis  [V] Simulate  [M] Monitor  [Q] Quit          |
+-------------------------------------------------------------+
```

## 📂 Directory Structure

```text
anandforge-tui/
├── src/                # Core TUI logic and integration engines
├── examples/           # Pre-built VLSI designs (Counter, Adder)
├── scripts/            # Automation wrappers for Yosys/iVerilog
├── LICENSE             # MIT License
└── main.py             # Entry point
```

## 🛠️ Getting Started

### Prerequisites
Ensure you have **iVerilog** and **Yosys** installed in your `$PATH`.

### Installation
```bash
git clone https://github.com/techanand8/anandforge-tui.git
cd anandforge-tui
python3 mavenik_gem.py
```

## 📅 Roadmap
- [x] iVerilog & Yosys Integration
- [x] Tabular Signal Monitor
- [ ] **Verilator** High-Speed Simulation Support
- [ ] **GTKWave** TUI Overlay Integration
- [ ] ASCII Schematic Export

---
Developed by [techanand8](https://github.com/techanand8)
