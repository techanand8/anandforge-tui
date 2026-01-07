#!/usr/bin/env python3
"""
MAVENIK ARENA - Professional Open-Source VLSI Development Environment
Created by: MAYANK ANAND
Offline Alternative to EDA Playground
"""

import os
import subprocess
import asyncio
from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    TextArea,
    DirectoryTree,
    Input,
    Label,
    Select,
)
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen
from textual.binding import Binding
from textual.reactive import reactive

# -------------------------------------------------
# THEMES
# -------------------------------------------------
try:
    from themes import THEMES
except ImportError:
    THEMES = {
        "Monokai": {
            "ace": "monokai",
            "bg": "#272822",
            "txt": "#F8F8F2",
            "acc": "#66D9EF",
            "con": "#1E1E1E",
            "accent2": "#A6E22E",
        }
    }

# -------------------------------------------------
# TOOL PATHS
# -------------------------------------------------
TOOL_PATHS = {
    "iverilog": "/usr/bin/iverilog",
    "vvp": "/usr/bin/vvp",
    "verilator": "/usr/bin/verilator",
    "yosys": "/usr/bin/yosys",
    "gtkwave": "/usr/bin/gtkwave",
}


# -------------------------------------------------
# BOOT SCREEN
# -------------------------------------------------
class BootScreen(Screen):
    BINDINGS = [("enter", "start", "Start"), ("escape", "start", "Start")]

    LOGO = """
 ███▄ ▄███▓ ▄▄▄    ██▒   █▓▓█████  ███▄    █  ██▓ ██ ▄█▀
▓██▒▀█▀ ██▒▒████▄ ▓██░   █▒▓█   ▀  ██ ▀█   █ ▓██▒ ██▄█▒ 
▓██    ▓██░▒██  ▀█▄▓██  █▒░▒███    ▓██  ▀█ ██▒▒██▒▓███▄░ 
▒██    ▒██ ░██▄▄▄▄██▒██ █░░▒▓█  ▄  ▓██▒  ▐▌██▒░██░▓██ █▄ 
▒██▒   ░██▒ ▓█   ▓██▒▒▀█░  ░▒████▒ ▒██░   ▓██░░██░▒██▒ █▄
░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▐░  ░░ ▒░ ░ ░ ▒░   ▒ ▒ ░▓  ▒ ▒▒ ▓▒
░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ░  ░ ░ ░░   ░ ▒░ ▒ ░░ ░▒ ▒░
░      ░     ░   ▒     ░░     ░       ░   ░ ░  ▒ ░░ ░▒ ░
       ░         ░  ░   ░     ░  ░          ░  ░  ░ ░
"""

    def compose(self) -> ComposeResult:
        with Container():
            yield Static(self.LOGO)

    def action_start(self) -> None:
        self.app.pop_screen()


# -------------------------------------------------
# MAIN APPLICATION
# -------------------------------------------------
class MavenikArena(App):
    TITLE = "MAVENIK ARENA - VLSI Development Environment"

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+t", "theme_selector", "Themes"),
        Binding("ctrl+r", "run_design", "Run"),
    ]

    # ✅ FIXED: no conflict with Textual
    user_theme = reactive("Monokai")
    design_file = reactive("")
    testbench_file = reactive("")

    def __init__(self):
        super().__init__()
        self.workspace = Path.cwd() / "mavenik_workspace"
        self.workspace.mkdir(exist_ok=True)
        self.design_path = None
        self.testbench_path = None

    # -------------------------------------------------
    # UI LAYOUT (THIS IS WHY IDE NOW SHOWS)
    # -------------------------------------------------
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal():
            # LEFT: FILE TREE
            yield DirectoryTree(self.workspace, id="file_tree")

            # CENTER: EDITOR + CONSOLE
            with Vertical():
                yield Label("🧠 Verilog / SystemVerilog Editor")
                yield TextArea(id="editor", language="verilog")

                yield Label("🖥 Console Output")
                yield TextArea(id="console", read_only=True)

        yield Footer()

    def on_mount(self) -> None:
        self.push_screen(BootScreen())

    # -------------------------------------------------
    # THEME HANDLING (SAFE)
    # -------------------------------------------------
    def action_theme_selector(self) -> None:
        if THEMES:
            self.apply_theme(list(THEMES.keys())[0])

    def apply_theme(self, theme_name: str) -> None:
        if theme_name in THEMES:
            self.user_theme = theme_name
            self.log_console(f"🎨 Applied theme: {theme_name}", "success")
        else:
            self.log_console(f"⚠ Theme not found: {theme_name}", "warning")

    # -------------------------------------------------
    # RUN DESIGN (PLACEHOLDER)
    # -------------------------------------------------
    def action_run_design(self) -> None:
        self.log_console("▶ Running design (integration pending)...", "info")

    # -------------------------------------------------
    # CONSOLE LOGGER
    # -------------------------------------------------
    def log_console(self, message: str, level: str = "info") -> None:
        console = self.query_one("#console", TextArea)
        console.insert(f"{message}\n")


# -------------------------------------------------
# ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    app = MavenikArena()
    app.run()
