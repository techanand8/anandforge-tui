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
    Header, Footer, Static, Button, TextArea, 
    DirectoryTree, Input, Label, Select
)
from textual.containers import Horizontal, Vertical, Container, ScrollableContainer
from textual.screen import Screen, ModalScreen
from textual.binding import Binding
from textual.reactive import reactive

# Import themes
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
            "accent2": "#A6E22E"
        }
    }

# Tool paths
TOOL_PATHS = {
    "iverilog": "/usr/bin/iverilog",
    "vvp": "/usr/bin/vvp",
    "verilator": "/usr/bin/verilator",
    "yosys": "/usr/bin/yosys",
    "gtkwave": "/usr/bin/gtkwave",
    "surfer": "/usr/local/bin/surfer",
}

# --- BOOT SCREEN ---
class BootScreen(Screen):
    """Animated intro screen with MAVENIK ARENA logo"""
    
    BINDINGS = [("enter", "start", "Start"), ("escape", "start", "Start")]
    
    LOGOS = [
        """
 ▄▄▄▄███▄▄▄▄      ▄████████ ▄██   ▄      ▄████████ ███▄▄▄▄      ▄█   ▄█▄    
▄██▀▀▀███▀▀▀██▄   ███    ███ ███   ██▄   ███    ███ ███▀▀▀██▄   ███ ▄███▀    
███   ███   ███   ███    ███ ███▄▄▄███   ███    ███ ███   ███   ███▐██▀      
███   ███   ███   ███    ███ ▀▀▀▀▀▀███   ███    ███ ███   ███  ▄█████▀       
███   ███   ███ ▀███████████ ▄██   ███ ▀███████████ ███   ███ ▀▀█████▄       
███   ███   ███   ███    ███ ███   ███   ███    ███ ███   ███   ███▐██▄      
███   ███   ███   ███    ███ ███   ███   ███    ███ ███   ███   ███ ▀███▄    
 ▀█   ███   █▀    ███    █▀   ▀█████▀    ███    █▀   ▀█   █▀    ███   ▀█▀    
                                                                ▀             
     ▄████████ ███▄▄▄▄      ▄████████ ███▄▄▄▄   ████████▄                    
    ███    ███ ███▀▀▀██▄   ███    ███ ███▀▀▀██▄ ███   ▀███                   
    ███    ███ ███   ███   ███    ███ ███   ███ ███    ███                   
    ███    ███ ███   ███   ███    ███ ███   ███ ███    ███                   
  ▀███████████ ███   ███ ▀███████████ ███   ███ ███    ███                   
    ███    ███ ███   ███   ███    ███ ███   ███ ███    ███                   
    ███    ███ ███   ███   ███    ███ ███   ███ ███   ▄███                   
    ███    █▀   ▀█   █▀    ███    █▀   ▀█   █▀  ████████▀                    
        """,
        """
███╗   ███╗ █████╗ ██╗   ██╗ █████╗ ███╗   ██╗██╗  ██╗                      
████╗ ████║██╔══██╗╚██╗ ██╔╝██╔══██╗████╗  ██║██║ ██╔╝                      
██╔████╔██║███████║ ╚████╔╝ ███████║██╔██╗ ██║█████╔╝                       
██║╚██╔╝██║██╔══██║  ╚██╔╝  ██╔══██║██║╚██╗██║██╔═██╗                       
██║ ╚═╝ ██║██║  ██║   ██║   ██║  ██║██║ ╚████║██║  ██╗                      
╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝                      
 █████╗ ███╗   ██╗ █████╗ ███╗   ██╗██████╗                                  
██╔══██╗████╗  ██║██╔══██╗████╗  ██║██╔══██╗                                 
███████║██╔██╗ ██║███████║██╔██╗ ██║██║  ██║                                 
██╔══██║██║╚██╗██║██╔══██║██║╚██╗██║██║  ██║                                 
██║  ██║██║ ╚████║██║  ██║██║ ╚████║██████╔╝                                 
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝                                  
        """
    ]
    
    CSS = """
    BootScreen {
        align: center middle;
        background: #000000;
    }
    
    #boot_container {
        width: 100%;
        height: 100%;
        align: center middle;
        background: #000000;
    }
    
    #boot_logo {
        color: #00FF41;
        text-align: center;
        width: 100%;
        content-align: center middle;
    }
    
    #boot_subtitle {
        color: #FFD700;
        text-align: center;
        text-style: bold italic;
        margin-top: 2;
    }
    
    #boot_creator {
        color: #00FF41;
        text-align: center;
        text-style: bold;
        margin-top: 1;
    }
    
    #boot_prompt {
        color: #000000;
        background: #00FF41;
        text-align: center;
        text-style: bold;
        margin-top: 3;
        padding: 1 4;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="boot_container"):
            yield Static(self.LOGOS[0], id="boot_logo")
            yield Static("Professional Open-Source VLSI Development Environment", id="boot_subtitle")
            yield Static("BY MAYANK ANAND", id="boot_creator")
            yield Static("PRESS [ENTER] TO START FORGING", id="boot_prompt")
    
    def on_mount(self) -> None:
        self.logo_index = 0
        self.set_interval(1.0, self.cycle_logo)
    
    def cycle_logo(self) -> None:
        self.logo_index = (self.logo_index + 1) % len(self.LOGOS)
        self.query_one("#boot_logo", Static).update(self.LOGOS[self.logo_index])
    
    def action_start(self) -> None:
        self.app.pop_screen()


# --- NEW FILE MODAL ---
class NewFileModal(ModalScreen):
    """Modal for creating new files with templates"""
    
    CSS = """
    NewFileModal {
        align: center middle;
    }
    
    #modal_container {
        width: 60;
        height: 25;
        border: thick #FFD700;
        background: #1a1a1a;
        padding: 2;
    }
    
    #modal_title {
        text-align: center;
        text-style: bold;
        color: #FFD700;
        height: 3;
    }
    
    #filename_input {
        margin: 1 0;
    }
    
    .template_btn {
        width: 100%;
        margin: 1 0;
    }
    
    #button_row {
        margin-top: 2;
        height: 3;
        align: center middle;
    }
    
    #button_row Button {
        margin: 0 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="modal_container"):
            yield Static("📝 CREATE NEW FILE", id="modal_title")
            yield Input(placeholder="Enter filename (e.g., counter.v or counter_tb.v)", id="filename_input")
            yield Static("\nSelect Template:", classes="label")
            yield Button("📄 Empty File", id="template_empty", classes="template_btn")
            yield Button("🔧 Module Template", id="template_module", classes="template_btn")
            yield Button("🧪 Testbench Template", id="template_testbench", classes="template_btn")
            with Horizontal(id="button_row"):
                yield Button("Create", variant="success", id="create_btn")
                yield Button("Cancel", variant="error", id="cancel_btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel_btn":
            self.dismiss(None)
        elif event.button.id == "create_btn":
            filename = self.query_one("#filename_input", Input).value
            if filename:
                self.dismiss({"filename": filename, "template": "empty"})
        elif event.button.id.startswith("template_"):
            template_type = event.button.id.replace("template_", "")
            filename = self.query_one("#filename_input", Input).value
            if filename:
                self.dismiss({"filename": filename, "template": template_type})


# --- THEME SELECTOR MODAL ---
class ThemeSelectorModal(ModalScreen):
    """Modal for selecting themes"""
    
    CSS = """
    ThemeSelectorModal {
        align: center middle;
    }
    
    #theme_container {
        width: 70;
        height: 30;
        border: thick #FFD700;
        background: #1a1a1a;
        padding: 2;
    }
    
    #theme_title {
        text-align: center;
        text-style: bold;
        color: #FFD700;
        height: 3;
    }
    
    #theme_scroll {
        height: 1fr;
        border: solid #333333;
        margin: 1 0;
    }
    
    .theme_btn {
        width: 100%;
        margin: 0;
        height: 3;
    }
    
    #close_btn {
        width: 20;
        margin-top: 1;
    }
    """
    
    def compose(self) -> ComposeResult:
        with Container(id="theme_container"):
            yield Static("🎨 THEME SELECTOR (50+ Themes)", id="theme_title")
            with ScrollableContainer(id="theme_scroll"):
                for theme_name in sorted(THEMES.keys()):
                    yield Button(f"🎨 {theme_name}", id=f"theme_{theme_name}", classes="theme_btn")
            yield Button("Close", variant="error", id="close_btn")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close_btn":
            self.dismiss(None)
        elif event.button.id.startswith("theme_"):
            theme_name = event.button.id.replace("theme_", "")
            self.dismiss(theme_name)


# --- MAIN APPLICATION ---
class MavenikArena(App):
    """Main VLSI TUI IDE Application"""
    
    TITLE = "MAVENIK ARENA - VLSI Development Environment"
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+s", "save_active", "Save"),
        Binding("ctrl+shift+s", "save_all", "Save All"),
        Binding("ctrl+n", "new_file", "New File"),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar"),
        Binding("ctrl+f", "focus_swap", "Focus Swap"),
        Binding("ctrl+t", "theme_selector", "Themes"),
        Binding("f5", "compile", "Compile"),
        Binding("f6", "simulate", "Simulate"),
        Binding("f7", "synthesize", "Synthesize"),
        Binding("f8", "view_waves", "Waves"),
        Binding("f9", "schematic", "Schematic"),
    ]
    
    CSS = """
    Screen {
        background: #0a0a0a;
    }
    
    #main_header {
        background: #00FF41;
        color: #000000;
        text-align: center;
        text-style: bold;
        height: 1;
    }
    
    #sidebar {
        width: 35;
        background: #1a1a1a;
        border-right: heavy #00FF41;
    }
    
    #sidebar.hidden {
        display: none;
    }
    
    .panel_header {
        background: #2a2a2a;
        color: #FFD700;
        text-align: center;
        text-style: bold;
        height: 1;
        border-bottom: solid #00FF41;
    }
    
    #work_area {
        width: 1fr;
    }
    
    #editor_split {
        height: 1fr;
    }
    
    #design_pane {
        width: 1fr;
        border-right: solid #333333;
    }
    
    #testbench_pane {
        width: 1fr;
    }
    
    .file_label {
        background: #1a1a1a;
        color: #00FF41;
        text-style: bold;
        padding: 0 1;
        height: 1;
    }
    
    TextArea {
        background: #0a0a0a;
        color: #00FF41;
        border: none;
        height: 1fr;
    }
    
    TextArea:focus {
        border: solid #FFD700;
    }
    
    #bottom_section {
        height: 15;
        border-top: heavy #00FF41;
    }
    
    #console_pane {
        width: 1fr;
    }
    
    #console {
        background: #000000;
        color: #00FF41;
        height: 1fr;
        padding: 1;
        border: solid #333333;
    }
    
    #tool_panel {
        width: 40;
        border-left: solid #333333;
        background: #1a1a1a;
    }
    
    #tool_grid {
        padding: 1;
    }
    
    .tool_section {
        margin: 1 0;
    }
    
    .section_label {
        color: #FFD700;
        text-style: bold;
        margin-bottom: 1;
    }
    
    .tool_btn {
        width: 100%;
        margin: 0 0 1 0;
        height: 3;
    }
    
    .tool_btn.primary {
        background: #00FF41;
        color: #000000;
    }
    
    .tool_btn.primary:hover {
        background: #FFD700;
    }
    
    .tool_btn.secondary {
        background: #2a2a2a;
        color: #00FF41;
    }
    
    .tool_btn.secondary:hover {
        background: #3a3a3a;
    }
    
    #file_ops {
        padding: 1;
    }
    
    .file_btn {
        width: 100%;
        margin: 0 0 1 0;
    }
    
    DirectoryTree {
        height: 1fr;
        padding: 1;
    }
    """
    
    current_theme = reactive("Monokai")
    design_file = reactive("")
    testbench_file = reactive("")
    
    def __init__(self):
        super().__init__()
        self.workspace = Path.cwd() / "mavenik_workspace"
        self.workspace.mkdir(exist_ok=True)
        self.design_path = None
        self.testbench_path = None
    
    def compose(self) -> ComposeResult:
        yield Static("⚡ MAVENIK ARENA | MAYANK ANAND VLSI WORKSTATION ⚡", id="main_header")
        
        with Horizontal():
            # Sidebar
            with Vertical(id="sidebar"):
                yield Static("📁 PROJECT EXPLORER", classes="panel_header")
                yield DirectoryTree("./", id="file_tree")
                
                with Container(id="file_ops"):
                    yield Button("📝 New File", id="btn_new", classes="file_btn", variant="success")
                    yield Button("🔄 Refresh", id="btn_refresh", classes="file_btn", variant="primary")
                    yield Button("🎨 Themes", id="btn_themes", classes="file_btn", variant="default")
            
            # Main work area
            with Vertical(id="work_area"):
                # Split editors
                with Horizontal(id="editor_split"):
                    # Design editor
                    with Vertical(id="design_pane"):
                        yield Static("📄 Design: (No file)", id="design_label", classes="file_label")
                        yield TextArea("", language="verilog", id="design_editor")
                    
                    # Testbench editor
                    with Vertical(id="testbench_pane"):
                        yield Static("🧪 Testbench: (No file)", id="testbench_label", classes="file_label")
                        yield TextArea("", language="verilog", id="testbench_editor")
                
                # Bottom section
                with Horizontal(id="bottom_section"):
                    # Console
                    with Vertical(id="console_pane"):
                        yield Static("💻 SYSTEM CONSOLE", classes="panel_header")
                        yield TextArea("", read_only=True, id="console")
                    
                    # Tool panel
                    with Vertical(id="tool_panel"):
                        yield Static("🛠️ TOOLS", classes="panel_header")
                        
                        with ScrollableContainer(id="tool_grid"):
                            # Compilation
                            with Container(classes="tool_section"):
                                yield Static("🔧 COMPILATION", classes="section_label")
                                yield Button("▶ Compile (F5)", id="tool_compile", classes="tool_btn primary")
                                yield Button("⚡ Lint", id="tool_lint", classes="tool_btn secondary")
                            
                            # Simulation
                            with Container(classes="tool_section"):
                                yield Static("🎬 SIMULATION", classes="section_label")
                                yield Button("▶ Simulate (F6)", id="tool_simulate", classes="tool_btn primary")
                            
                            # Analysis
                            with Container(classes="tool_section"):
                                yield Static("📊 ANALYSIS", classes="section_label")
                                yield Button("🔨 Synthesize (F7)", id="tool_synth", classes="tool_btn primary")
                                yield Button("📐 Schematic (F9)", id="tool_schem", classes="tool_btn secondary")
                            
                            # Waveforms
                            with Container(classes="tool_section"):
                                yield Static("🌊 WAVEFORMS", classes="section_label")
                                yield Button("📺 GTKWave", id="tool_gtkwave", classes="tool_btn secondary")
                                yield Button("🌊 Surfer", id="tool_surfer", classes="tool_btn secondary")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize application"""
        self.push_screen(BootScreen())
        self.log_console("🚀 MAVENIK ARENA initialized", "success")
        self.log_console("📁 Workspace: " + str(self.workspace), "info")
        self.check_tools()
    
    def check_tools(self) -> None:
        """Check if tools are installed"""
        self.log_console("\n🔍 Checking installed tools...", "info")
        
        for tool_name, tool_path in TOOL_PATHS.items():
            if os.path.exists(tool_path):
                self.log_console(f"  ✓ {tool_name}: {tool_path}", "success")
            else:
                self.log_console(f"  ✗ {tool_name}: Not found", "error")
    
    def log_console(self, message: str, level: str = "info") -> None:
        """Add message to console with color coding"""
        console = self.query_one("#console", TextArea)
        
        color_prefixes = {
            "info": "[cyan]",
            "success": "[green]✓ ",
            "error": "[red]✗ ",
            "warning": "[yellow]⚠ ",
        }
        
        prefix = color_prefixes.get(level, "")
        console.text += f"{prefix}{message}[/]\n"
    
    def on_directory_tree_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Handle file selection from tree"""
        try:
            file_path = event.path
            filename = file_path.name.lower()
            
            # Read file content
            content = file_path.read_text()
            
            # Smart routing based on filename
            is_testbench = any(x in filename for x in ["_tb", "tb_", "test", "testbench"])
            
            if is_testbench:
                # Load into testbench editor
                self.query_one("#testbench_editor", TextArea).text = content
                self.query_one("#testbench_label", Static).update(f"🧪 Testbench: {file_path.name}")
                self.testbench_path = str(file_path)
                self.log_console(f"📂 Loaded testbench: {file_path.name}", "success")
            else:
                # Load into design editor
                self.query_one("#design_editor", TextArea).text = content
                self.query_one("#design_label", Static).update(f"📄 Design: {file_path.name}")
                self.design_path = str(file_path)
                self.log_console(f"📂 Loaded design: {file_path.name}", "success")
                
        except Exception as e:
            self.log_console(f"Error loading file: {str(e)}", "error")
    
    def sync_files(self) -> None:
        """Save current editor contents to files"""
        try:
            # Save design
            if self.design_path:
                design_content = self.query_one("#design_editor", TextArea).text
                with open(self.design_path, "w") as f:
                    f.write(design_content)
            
            # Save testbench
            if self.testbench_path:
                testbench_content = self.query_one("#testbench_editor", TextArea).text
                with open(self.testbench_path, "w") as f:
                    f.write(testbench_content)
            
            # Create combined file for simulation
            combined_path = self.workspace / "top_active.sv"
            with open(combined_path, "w") as f:
                f.write(self.query_one("#design_editor", TextArea).text)
                f.write("\n\n")
                f.write(self.query_one("#testbench_editor", TextArea).text)
            
            self.log_console("💾 Files synchronized", "success")
            
        except Exception as e:
            self.log_console(f"Error syncing files: {str(e)}", "error")
    
    def run_command(self, cmd: str, cwd: str = None) -> tuple:
        """Execute shell command and return output"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd or str(self.workspace),
                timeout=60
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timeout"
        except Exception as e:
            return -1, "", str(e)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle all button clicks"""
        btn_id = event.button.id
        
        # File operations
        if btn_id == "btn_new":
            self.action_new_file()
        elif btn_id == "btn_refresh":
            self.query_one("#file_tree", DirectoryTree).reload()
            self.log_console("🔄 File tree refreshed", "info")
        elif btn_id == "btn_themes":
            self.action_theme_selector()
        
        # Tool operations (always sync first)
        elif btn_id.startswith("tool_"):
            self.sync_files()
            
            if btn_id == "tool_compile":
                self.action_compile()
            elif btn_id == "tool_lint":
                self.action_lint()
            elif btn_id == "tool_simulate":
                self.action_simulate()
            elif btn_id == "tool_synth":
                self.action_synthesize()
            elif btn_id == "tool_schem":
                self.action_schematic()
            elif btn_id == "tool_gtkwave":
                self.action_view_waves("gtkwave")
            elif btn_id == "tool_surfer":
                self.action_view_waves("surfer")
    
    def action_compile(self) -> None:
        """Compile with iverilog"""
        self.log_console("\n🔨 COMPILING with iverilog...", "info")
        
        cmd = f"{TOOL_PATHS['iverilog']} -g2012 -o {self.workspace}/design.vvp {self.workspace}/top_active.sv"
        code, stdout, stderr = self.run_command(cmd)
        
        if code == 0:
            self.log_console("✓ Compilation successful!", "success")
            if stdout:
                self.log_console(stdout, "info")
        else:
            self.log_console("✗ Compilation failed!", "error")
            self.log_console(stderr, "error")
    
    def action_lint(self) -> None:
        """Lint with Verilator"""
        self.log_console("\n⚡ LINTING with Verilator...", "info")
        
        cmd = f"{TOOL_PATHS['verilator']} --lint-only -Wall {self.workspace}/top_active.sv"
        code, stdout, stderr = self.run_command(cmd)
        
        if "Error" not in stderr:
            self.log_console("✓ Lint check passed!", "success")
        else:
            self.log_console("⚠ Lint warnings/errors:", "warning")
        
        if stderr:
            self.log_console(stderr, "warning")
    
    def action_simulate(self) -> None:
        """Run simulation"""
        self.log_console("\n▶ SIMULATING...", "info")
        
        vvp_file = self.workspace / "design.vvp"
        if not vvp_file.exists():
            self.log_console("✗ No compiled design. Run compile first!", "error")
            return
        
        cmd = f"{TOOL_PATHS['vvp']} {vvp_file}"
        code, stdout, stderr = self.run_command(cmd)
        
        if code == 0:
            self.log_console("✓ Simulation complete!", "success")
            if stdout:
                self.log_console(stdout, "info")
        else:
            self.log_console("✗ Simulation failed!", "error")
            if stderr:
                self.log_console(stderr, "error")
    
    def action_synthesize(self) -> None:
        """Synthesize with Yosys"""
        self.log_console("\n🔨 SYNTHESIZING with Yosys...", "info")
        
        script = f"""
read_verilog -sv {self.workspace}/top_active.sv
hierarchy -auto-top
proc; opt; fsm; opt; memory; opt
techmap; opt
stat
"""
        
        script_file = self.workspace / "synth.ys"
        script_file.write_text(script)
        
        cmd = f"{TOOL_PATHS['yosys']} -s {script_file}"
        code, stdout, stderr = self.run_command(cmd)
        
        if code == 0:
            self.log_console("✓ Synthesis complete!", "success")
            # Extract stats from output
            for line in stdout.split("\n"):
                if "Number of cells" in line or "Chip area" in line:
                    self.log_console(line.strip(), "info")
        else:
            self.log_console("✗ Synthesis failed!", "error")
            if stderr:
                self.log_console(stderr, "error")
    
    def action_schematic(self) -> None:
        """Generate schematic"""
        self.log_console("\n📐 GENERATING SCHEMATIC...", "info")
        
        script = f"""
read_verilog -sv {self.workspace}/top_active.sv
hierarchy -auto-top
proc; opt
show -format dot -prefix {self.workspace}/schematic
"""
        
        script_file = self.workspace / "schem.ys"
        script_file.write_text(script)
        
        cmd = f"{TOOL_PATHS['yosys']} -s {script_file}"
        code, stdout, stderr = self.run_command(cmd)
        
        if code == 0:
            dot_file = self.workspace / "schematic.dot"
            if dot_file.exists():
                # Convert to PNG
                png_file = self.workspace / "schematic.png"
                subprocess.run(f"dot -Tpng {dot_file} -o {png_file}", shell=True)
                
                if png_file.exists():
                    self.log_console("✓ Schematic generated!", "success")
                    subprocess.Popen(["xdg-open", str(png_file)])
                else:
                    self.log_console("⚠ Could not convert to PNG", "warning")
            else:
                self.log_console("⚠ DOT file not generated", "warning")
        else:
            self.log_console("✗ Schematic generation failed!", "error")
    
    def action_view_waves(self, viewer: str) -> None:
        """Open waveform viewer"""
        vcd_file = self.workspace / "dump.vcd"
        
        if not vcd_file.exists():
            self.log_console(f"✗ No waveform file found. Run simulation first!", "error")
            return
        
        self.log_console(f"\n🌊 Opening {viewer.upper()}...", "info")
        
        try:
            if viewer == "gtkwave":
                subprocess.Popen([TOOL_PATHS["gtkwave"], str(vcd_file)])
            else:
                subprocess.Popen([TOOL_PATHS["surfer"], str(vcd_file)])
            
            self.log_console(f"✓ {viewer.upper()} launched", "success")
        except Exception as e:
            self.log_console(f"✗ Could not launch {viewer}: {str(e)}", "error")
    
    def action_new_file(self) -> None:
        """Show new file modal"""
        def handle_result(result):
            if result:
                self.create_file(result["filename"], result["template"])
        
        self.push_screen(NewFileModal(), handle_result)
    
    def create_file(self, filename: str, template: str) -> None:
        """Create new file with template"""
        try:
            file_path = Path(filename)
            
            # Generate template content
            module_name = file_path.stem
            
            if template == "empty":
                content = ""
            elif template == "module":
                content = f"""module {module_name} (
    input wire clk,
    input wire rst,
    output reg [7:0] data_out
);

// Your code here

endmodule
"""
            elif template == "testbench":
                content = f"""module {module_name};

    reg clk;
    reg rst;
    wire [7:0] data_out;
    
    // Instantiate DUT
    // your_module dut (
    //     .clk(clk),
    //     .rst(rst),
    //     .data_out(data_out)
    // );
    
    // Clock generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end
    
    // VCD dump
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, {module_name});
    end
    
    // Test stimulus
    initial begin
        rst = 1;
        #20 rst = 0;
        
        // Your test cases here
        
        #1000 $finish;
    end

endmodule
"""
            else:
                content = ""
            
            # Write file
            file_path.write_text(content)
            self.log_console(f"✓ Created: {filename}", "success")
            
            # Refresh tree
            self.query_one("#file_tree", DirectoryTree).reload()
            
        except Exception as e:
            self.log_console(f"✗ Error creating file: {str(e)}", "error")
    
    def action_theme_selector(self) -> None:
        """Show theme selector"""
        def handle_theme(theme_name):
            if theme_name:
                self.apply_theme(theme_name)
        
        self.push_screen(ThemeSelectorModal(), handle_theme)
    
    def apply_theme(self, theme_name: str) -> None:
        """Apply selected theme"""
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.log_console(f"🎨 Applied theme: {theme_name}", "success")
            # Note: Full theme application would require CSS regeneration
            # For now, just log the change
        else:
            self.log_console(f"⚠ Theme not found: {theme_name}", "warning")
    
    def action_toggle_sidebar(self) -> None:
        """Toggle sidebar visibility"""
        sidebar = self.query_one("#sidebar")
        sidebar.toggle_class("hidden")
    
    def action_focus_swap(self) -> None:
        """Swap focus between editors"""
        design_editor = self.query_one("#design_editor", TextArea)
        testbench_editor = self.query_one("#testbench_editor", TextArea)
        
        if self.focused == design_editor:
            testbench_editor.focus()
        else:
            design_editor.focus()
    
    def action_save_active(self) -> None:
        """Save currently focused editor"""
        focused = self.focused
        
        if isinstance(focused, TextArea) and focused.id == "design_editor":
            if self.design_path:
                with open(self.design_path, "w") as f:
                    f.write(focused.text)
                self.log_console("💾 Design saved", "success")
        elif isinstance(focused, TextArea) and focused.id == "testbench_editor":
            if self.testbench_path:
                with open(self.testbench_path, "w") as f:
                    f.write(focused.text)
                self.log_console("💾 Testbench saved", "success")
    
    def action_save_all(self) -> None:
        """Save both editors"""
        self.sync_files()
        self.log_console("💾 All files saved", "success")


if __name__ == "__main__":
    app = MavenikArena()
    app.run()