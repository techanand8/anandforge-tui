import os
import subprocess
from textual.app import App, ComposeResult
from textual.widgets import (
    Header,
    Footer,
    Static,
    Button,
    TextArea,
    DirectoryTree,
    Input,
)
from textual.containers import Horizontal, Vertical, Grid
from textual.screen import Screen, ModalScreen
from textual.binding import Binding
from textual import events

# --- 1. STARTUP SCREEN ---
LOGO_TEXT = r"""
  ___                       _ _____                       
 / _ \                     | |  ___|                      
/ /_\ \_ __   __ _ _ __   __| | |_ ___  _ __ __ _  ___ 
|  _  | '_ \ / _` | '_ \ / _` |  _/ _ \| '__/ _` |/ _ \
| | | | | | | (_| | | | | (_| | || (_) | | | (_| |  __/
\_| |_/_| |_|\__,_|_| |_|\__,_\_| \___/|_|  \__, |\___|
"""


class IntroScreen(Screen):
    def compose(self) -> ComposeResult:
        with Vertical(id="intro-container"):
            yield Static(LOGO_TEXT, id="logo")
            yield Static("--- FORGE ENGINE v4.5 STABLE ---", id="status")
            yield Static("DESIGNED BY MAYANK ANAND", id="designer-tag")
            yield Static("[ PRESS ENTER TO START ]", id="blink-text")

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.app.push_screen(EditorScreen())


class FileModal(ModalScreen):
    def __init__(self, mode="new"):
        super().__init__()
        self.mode = mode

    def compose(self) -> ComposeResult:
        title = "New File Name:" if self.mode == "new" else "Rename To:"
        with Vertical(id="modal"):
            yield Static(title)
            yield Input(id="file_input", placeholder="e.g. adder.sv")
            with Horizontal():
                yield Button("CONFIRM", variant="success", id="ok")
                yield Button("CANCEL", variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(self.query_one("#file_input").value)
        else:
            self.dismiss(None)


# --- 2. MAIN IDE CORE ---
class EditorScreen(Screen):
    BINDINGS = [
        Binding("ctrl+s", "save_current", "Save"),
        Binding("ctrl+n", "new_file_shortcut", "New"),
        Binding("ctrl+b", "toggle_sidebar", "Sidebar"),
        Binding("ctrl+f", "cycle_focus", "View"),
        Binding("q", "quit", "Exit"),
    ]

    def on_mount(self) -> None:
        self.view_mode = "split"
        self.sidebar_visible = True
        self.current_path = ""

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            # SIDEBAR
            with Vertical(id="sidebar_panel"):
                yield Static("📁 EXPLORER", id="side-title")
                yield DirectoryTree("./", id="tree")
                with Grid(id="file-ops"):
                    yield Button("New", id="btn_new", variant="primary")
                    yield Button("Ren", id="btn_ren", variant="warning")
                    yield Button("Del", id="btn_del", variant="error")
                yield Static("📊 SYNTH STATS", id="stat-title")
                yield Static("System Online", id="synth_report")

            # MAIN WORKSPACE
            with Vertical(id="main-area"):
                with Horizontal(id="editors-container"):
                    with Vertical(id="design-pane"):
                        yield Static("📄 DESIGN", id="lbl_design", classes="label")
                        yield TextArea(id="design_ed", language="verilog")
                    with Vertical(id="tb-pane"):
                        yield Static("🧪 TESTBENCH", id="lbl_tb", classes="label")
                        yield TextArea(id="tb_ed", language="verilog")

                # TOOLBAR
                with Horizontal(id="action-bar"):
                    yield Button("🚀 SIM", id="run_sim", classes="eda-btn")
                    yield Button("🛠️ SYNTH", id="run_synth", classes="eda-btn")
                    yield Button("📐 SCHEM", id="run_schem", classes="eda-btn")
                    yield Button("📈 GTK", id="run_gtk", classes="eda-btn")
                    yield Button("🏄 SURF", id="run_surfer", classes="eda-btn")
                    yield Button("🔄 VIEW", id="btn_cycle", classes="eda-btn")

                yield Static("CONSOLE:", id="con-label")
                yield TextArea(id="console", read_only=True)
        yield Footer()

    # --- THE STRICT ROUTER ---
    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        self.current_path = str(event.path)
        fname = os.path.basename(self.current_path).lower()
        try:
            with open(self.current_path, "r") as f:
                content = f.read()

            # Pattern check: ONLY move to TB if 'tb' is explicitly in the name structure
            is_tb_pattern = "tb_" in fname or "_tb" in fname or ".tb" in fname

            if is_tb_pattern:
                self.query_one("#tb_ed").text = content
                self.query_one("#lbl_tb").update(
                    f"🧪 TB: {os.path.basename(self.current_path)}"
                )
            else:
                self.query_one("#design_ed").text = content
                self.query_one("#lbl_design").update(
                    f"📄 DESIGN: {os.path.basename(self.current_path)}"
                )
        except Exception as e:
            self.query_one("#console").text = f"Error opening: {e}"

    # --- SIDEBAR TOGGLE ---
    def action_toggle_sidebar(self) -> None:
        sidebar = self.query_one("#sidebar_panel")
        self.sidebar_visible = not self.sidebar_visible
        sidebar.display = self.sidebar_visible

    # --- SAVE LOGIC ---
    def action_save_current(self) -> None:
        if not self.current_path:
            return
        fname = os.path.basename(self.current_path).lower()
        is_tb = "tb_" in fname or "_tb" in fname or ".tb" in fname
        content = (
            self.query_one("#tb_ed").text
            if is_tb
            else self.query_one("#design_ed").text
        )

        try:
            with open(self.current_path, "w") as f:
                f.write(content)
            self.query_one("#console").text = (
                f"SUCCESS: Saved {os.path.basename(self.current_path)}"
            )
        except Exception as e:
            self.query_one("#console").text = f"Save Error: {e}"

    # --- FILE OPS ---
    def action_new_file_shortcut(self) -> None:
        self.app.push_screen(FileModal(mode="new"), self.add_file)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        cid = event.button.id
        if cid == "btn_new":
            self.app.push_screen(FileModal(mode="new"), self.add_file)
        elif cid == "btn_ren":
            self.app.push_screen(FileModal(mode="ren"), self.rename_file)
        elif cid == "btn_del":
            self.delete_file()
        elif cid == "btn_cycle":
            self.action_cycle_focus()
        elif cid in ["run_sim", "run_synth", "run_schem", "run_gtk", "run_surfer"]:
            self.handle_eda(cid)

    def add_file(self, name):
        if name:
            with open(name, "w") as f:
                f.write("// Mayank Design\n")
            self.query_one("#tree").reload()

    def rename_file(self, name):
        if name and self.current_path:
            os.rename(self.current_path, name)
            self.query_one("#tree").reload()

    def delete_file(self):
        if self.current_path:
            os.remove(self.current_path)
            self.query_one("#tree").reload()

    # --- EDA ENGINE ---
    def handle_eda(self, action):
        # Save current active buffers to run simulation
        with open("top_active.v", "w") as f:
            f.write(self.query_one("#design_ed").text)
        with open("tb_active.v", "w") as f:
            f.write(self.query_one("#tb_ed").text)

        files = "top_active.v tb_active.v"

        if action == "run_sim":
            cmd = f"iverilog -g2012 -o sim.out {files} && vvp sim.out"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            self.query_one("#console").text = f"SIMULATION:\n{res.stdout}{res.stderr}"
        elif action == "run_synth":
            cmd = f"yosys -p 'read_verilog -sv top_active.v; proc; opt; stat'"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            self.query_one("#console").text = f"SYNTHESIS:\n{res.stdout}{res.stderr}"
        elif action in ["run_gtk", "run_surfer"]:
            tool = "gtkwave" if action == "run_gtk" else "surfer"
            if os.path.exists("dump.vcd"):
                subprocess.Popen([tool, "dump.vcd"])
        elif action == "run_schem":
            subprocess.run(
                f"yosys -p 'read_verilog -sv top_active.v; proc; opt; show -format dot -prefix out'",
                shell=True,
            )
            if os.path.exists("out.dot"):
                subprocess.run("dot -Tpng out.dot -o out.png", shell=True)
                subprocess.Popen(["xdg-open", "out.png"])

    def action_cycle_focus(self) -> None:
        d_p, t_p = self.query_one("#design-pane"), self.query_one("#tb-pane")
        if self.view_mode == "split":
            self.view_mode = "design"
            d_p.display, t_p.display = True, False
        elif self.view_mode == "design":
            self.view_mode = "tb"
            d_p.display, t_p.display = False, True
        else:
            self.view_mode = "split"
            d_p.display, t_p.display = True, True


# --- 3. CSS ---
class AnandForgeApp(App):
    CSS = """
    #intro-container { align: center middle; background: #050505; }
    #logo { color: #D4AF37; text-align: center; }
    #status { color: #00FF41; margin-top: 1; text-align: center; }
    #designer-tag { color: #FFA500; margin-top: 1; border-top: solid #333; padding-top: 1; text-align: center; }
    #blink-text { color: white; margin-top: 2; text-align: center; }
    #sidebar_panel { width: 30; border-right: tall #00FF41; background: #0a0a0a; }
    #side-title, #stat-title { background: #00FF41; color: black; text-align: center; }
    #file-ops { grid-size: 3; height: 3; margin: 1; }
    .label { background: #1a1a1a; color: #00FF41; padding: 0 1; border-bottom: solid #00FF41; }
    TextArea { height: 1fr; border: solid #333; background: #050505; }
    #console { height: 12; background: #000; color: #00FF41; border-top: double #00FF41; }
    #action-bar { height: 3; align: center middle; background: #111; }
    .eda-btn { margin: 0 1; min-width: 9; background: #222; border: solid #444; }
    #modal { padding: 2; background: #1a1a1a; border: thick #00FF41; align: center middle; height: 12; width: 45; }
    """

    def on_mount(self) -> None:
        self.push_screen(IntroScreen())


if __name__ == "__main__":
    AnandForgeApp().run()
