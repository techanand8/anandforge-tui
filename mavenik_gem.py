import os
import asyncio
import subprocess
import shutil
import time
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header,
    Footer,
    Static,
    TextArea,
    Button,
    Label,
    Log,
    DirectoryTree,
    Input,
)
from textual.binding import Binding
from textual.screen import Screen, ModalScreen


# --- TERMINAL DETECTOR ---
def get_terminal_cmd():
    for term in ["konsole", "gnome-terminal", "xfce4-terminal", "xterm", "terminator"]:
        if shutil.which(term):
            return term
    return "x-terminal-emulator"


# --- SPLASH SCREEN ---
class Splash(Screen):
    """Intro screen designed by Mayank Anand"""

    def compose(self) -> ComposeResult:
        yield Container(
            Static("╔════════════════════════════════════╗", classes="sp_dec"),
            Static("║      ANANDFORGE VLSI STUDIO      ║", id="sp_title"),
            Static("╠════════════════════════════════════╣", classes="sp_dec"),
            Static("║     DESIGNED BY MAYANK ANAND     ║", id="sp_author"),
            Static("╚════════════════════════════════════╝", classes="sp_dec"),
            Static("\n[ PRESS ENTER TO START ]", id="sp_hint"),
            id="splash_box",
        )

    def on_key(self, event):
        if event.key == "enter":
            self.app.pop_screen()


# --- MODAL: NEW FILE ---
class FilePrompt(ModalScreen):
    def compose(self) -> ComposeResult:
        yield Vertical(
            Label("New File Name:"),
            Input(id="inp_new", placeholder="module.v"),
            Horizontal(
                Button("Create", id="btn_create", variant="success"),
                Button("Cancel", id="btn_cancel", variant="error"),
            ),
            id="modal_box",
        )

    def on_button_pressed(self, event):
        if event.button.id == "btn_create":
            self.dismiss(self.query_one("#inp_new").value)
        else:
            self.dismiss(None)


# --- MODAL: RENAME FILE ---
class RenamePrompt(ModalScreen):
    def __init__(self, old_name):
        super().__init__()
        self.old_name = old_name

    def compose(self) -> ComposeResult:
        yield Vertical(
            Label(f"Rename '{self.old_name}' to:"),
            Input(id="inp_ren", placeholder=self.old_name),
            Horizontal(
                Button("Rename", id="btn_ren", variant="primary"),
                Button("Cancel", id="btn_cancel", variant="error"),
            ),
            id="modal_box",
        )

    def on_button_pressed(self, event):
        if event.button.id == "btn_ren":
            self.dismiss(self.query_one("#inp_ren").value)
        else:
            self.dismiss(None)


# --- MAIN APP ---
class AnandForge(App):
    TITLE = "ANANDFORGE | VLSI WORKSTATION"

    CSS = """
    Screen { layout: vertical; }
    
    /* SPLASH SCREEN STYLES - FIXED CSS */
    #splash_box {
        align: center middle;
        height: 100%;
        background: #1a1b26;
    }
    #sp_title { color: #bb9af7; text-style: bold; }
    #sp_author { color: #7aa2f7; text-style: italic; }
    #sp_dec { color: #414868; }
    #sp_hint { color: #e0af68; margin-top: 2; text-align: center; width: 100%; }

    /* LEFT SIDEBAR - FULL HEIGHT */
    #sidebar { 
        width: 30; 
        dock: left; 
        background: #16161e; 
        border-right: heavy #7aa2f7; 
        height: 100%;
    }
    
    #right-pane { width: 1fr; height: 100%; layout: vertical; }
    #toolbar { height: 3; background: #1a1b26; border-bottom: solid #414868; align: center middle; }
    #editor-area { width: 1fr; height: 1fr; background: #1a1b26; }
    .editor-box { border: solid #414868; height: 1fr; }
    #console-area { height: 12; border-top: heavy #bb9af7; background: black; }
    #console { height: 1fr; color: #c0caf5; }
    .lbl { text-align: center; background: #24283b; color: #7aa2f7; }
    
    #modal_box { 
        padding: 1 2; 
        background: #24283b; 
        border: thick #7aa2f7; 
        width: 50; 
        height: 14; 
        align: center middle; 
    }
    Button { min-width: 6; margin: 0 1; }
    """

    BINDINGS = [
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar"),
        Binding("ctrl+t", "open_terminal", "Terminal"),
        Binding("ctrl+s", "save_files", "Save"),
        Binding("f1", "view_rtl", "RTL View"),
        Binding("f2", "view_tb", "TB View"),
        Binding("f3", "view_split", "Split View"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-container"):
            with Vertical(id="sidebar"):
                yield Label("PROJECT MANAGER", classes="lbl")
                yield DirectoryTree("./", id="tree")
                with Horizontal(classes="file-ops"):
                    yield Button("NEW", id="btn_new", variant="success")
                    yield Button("DEL", id="btn_del", variant="error")
                    yield Button("REN", id="btn_ren", variant="primary")

            with Vertical(id="right-pane"):
                with Horizontal(id="toolbar"):
                    yield Button("SIDE", id="btn_toggle")
                    yield Button("SIM (IV)", id="btn_sim", variant="primary")
                    yield Button("LINT (VL)", id="btn_lint")
                    yield Button("SYNTH", id="btn_synth")
                    yield Button("SCHEM", id="btn_schem", variant="success")
                    yield Button("GTK", id="btn_gtk")
                    yield Button("SURF", id="btn_surf")
                    yield Button("TERM", id="btn_term", variant="warning")
                    yield Button("RTL", id="btn_v_rtl")
                    yield Button("TB", id="btn_v_tb")
                    yield Button("BOTH", id="btn_v_split")

                with Horizontal(id="editor-area"):
                    with Vertical(id="pane_rtl", classes="editor-box"):
                        yield Label("📄 RTL DESIGN", classes="lbl", id="lbl_rtl")
                        yield TextArea.code_editor(
                            "", language="verilog", id="ed_rtl", show_line_numbers=True
                        )
                    with Vertical(id="pane_tb", classes="editor-box"):
                        yield Label("🧪 TESTBENCH", classes="lbl", id="lbl_tb")
                        yield TextArea.code_editor(
                            "", language="verilog", id="ed_tb", show_line_numbers=True
                        )

                with Vertical(id="console-area"):
                    yield Log(id="console")
        yield Footer()

    def on_mount(self):
        self.push_screen(Splash())
        self.active_rtl = self.active_tb = None
        self.term_cmd = get_terminal_cmd()
        self.log_msg(f"System Ready. Terminal: {self.term_cmd}")

    def log_msg(self, msg):
        self.query_one("#console").write_line(f"[{time.strftime('%H:%M:%S')}] » {msg}")

    def on_directory_tree_file_selected(self, event):
        path = str(event.path)
        if not os.path.isfile(path):
            return
        try:
            content = Path(path).read_text()
            name = os.path.basename(path)
            if "tb" in name.lower() or "test" in name.lower():
                self.active_tb = path
                self.query_one("#ed_tb").load_text(content)
                self.query_one("#lbl_tb").update(f"🧪 {name}")
            else:
                self.active_rtl = path
                self.query_one("#ed_rtl").load_text(content)
                self.query_one("#lbl_rtl").update(f"📄 {name}")
        except:
            pass

    def action_save_files(self):
        if self.active_rtl:
            Path(self.active_rtl).write_text(self.query_one("#ed_rtl").text)
        if self.active_tb:
            Path(self.active_tb).write_text(self.query_one("#ed_tb").text)
        self.log_msg("Files saved.")

    def on_button_pressed(self, event):
        bid = event.button.id
        if bid == "btn_toggle":
            self.action_toggle_sidebar()
        elif bid == "btn_new":
            self.push_screen(FilePrompt(), self.handle_new)
        elif bid == "btn_del":
            self.delete_file()
        elif bid == "btn_ren":
            self.rename_file()
        elif bid == "btn_v_rtl":
            self.action_view_rtl()
        elif bid == "btn_v_tb":
            self.action_view_tb()
        elif bid == "btn_v_split":
            self.action_view_split()
        elif bid == "btn_term":
            self.action_open_terminal()
        elif bid == "btn_sim":
            self.run_simulation()
        elif bid == "btn_lint":
            self.run_verilator()
        elif bid == "btn_synth":
            self.run_synthesis()
        elif bid == "btn_schem":
            self.run_schematic()
        elif bid == "btn_gtk":
            subprocess.Popen(["gtkwave", "dump.vcd"])
        elif bid == "btn_surf":
            subprocess.Popen(["surfer", "dump.vcd"])

    def action_toggle_sidebar(self):
        sb = self.query_one("#sidebar")
        sb.display = not sb.display

    def action_open_terminal(self):
        subprocess.Popen([self.term_cmd])

    def handle_new(self, name):
        if name:
            Path(name).touch()
            self.query_one("#tree").reload()

    def delete_file(self):
        node = self.query_one("#tree").cursor_node
        if node and os.path.isfile(node.data.path):
            os.remove(node.data.path)
            self.query_one("#tree").reload()

    def rename_file(self):
        node = self.query_one("#tree").cursor_node
        if node:
            self.push_screen(RenamePrompt(node.data.path.name), self.handle_rename)

    def handle_rename(self, new_name):
        node = self.query_one("#tree").cursor_node
        if new_name and node:
            os.rename(node.data.path, Path(node.data.path).parent / new_name)
            self.query_one("#tree").reload()

    async def run_process(self, cmd, name):
        self.log_msg(f"Running {name}...")
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            self.query_one("#console").write(stdout.decode())
        if stderr:
            self.query_one("#console").write(stderr.decode())
        return proc.returncode

    def run_simulation(self):
        if self.active_rtl and self.active_tb:
            self.action_save_files()
            self.run_worker(self._sim_flow())

    async def _sim_flow(self):
        if (
            await self.run_process(
                ["iverilog", "-o", "sim.vvp", self.active_rtl, self.active_tb],
                "iVerilog",
            )
            == 0
        ):
            await self.run_process(["vvp", "sim.vvp"], "VVP")

    def run_verilator(self):
        if self.active_rtl:
            self.action_save_files()
            self.run_worker(
                self.run_process(
                    ["verilator", "--lint-only", "-Wall", self.active_rtl], "Verilator"
                )
            )

    def run_synthesis(self):
        if self.active_rtl:
            self.action_save_files()
            script = f"read_verilog {self.active_rtl}; synth -top {Path(self.active_rtl).stem}; write_verilog synth.v; stat"
            Path("synth.ys").write_text(script)
            self.run_worker(self.run_process(["yosys", "synth.ys"], "Yosys"))

    def run_schematic(self):
        if self.active_rtl:
            self.action_save_files()
            Path("schem.ys").write_text(
                f"read_verilog {self.active_rtl}; proc; opt; show -format png -prefix schematic"
            )
            self.run_worker(self._schem_flow())

    async def _schem_flow(self):
        await self.run_process(["yosys", "schem.ys"], "Schematic")
        for v in ["display", "eog", "xdg-open"]:
            if shutil.which(v):
                subprocess.Popen([v, "schematic.png"])
                break

    def action_view_rtl(self):
        self.query_one("#pane_rtl").display, self.query_one("#pane_tb").display = (
            True,
            False,
        )

    def action_view_tb(self):
        self.query_one("#pane_rtl").display, self.query_one("#pane_tb").display = (
            False,
            True,
        )

    def action_view_split(self):
        self.query_one("#pane_rtl").display, self.query_one("#pane_tb").display = (
            True,
            True,
        )


if __name__ == "__main__":
    AnandForge().run()
