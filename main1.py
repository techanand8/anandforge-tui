import os
import subprocess
import datetime
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

# --- 1. START SCREEN (DESIGNED BY MAYANK ANAND) ---
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
            yield Static("--- FORGE ENGINE v2.5 ONLINE ---", id="status")
            yield Static("DESIGNED BY MAYANK ANAND", id="designer-tag")
            yield Static("[ PRESS ENTER TO START ]", id="blink-text")

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            self.app.push_screen(EditorScreen())


# --- 2. MODAL ---
class FileModal(ModalScreen):
    def __init__(self, mode="new"):
        super().__init__()
        self.mode = mode

    def compose(self) -> ComposeResult:
        title = "New File Name:" if self.mode == "new" else "Rename To:"
        with Vertical(id="modal"):
            yield Static(title)
            yield Input(id="file_input", placeholder="alu.v")
            with Horizontal():
                yield Button("CONFIRM", variant="success", id="ok")
                yield Button("CANCEL", variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(self.query_one("#file_input").value)
        else:
            self.dismiss(None)


# --- 3. THE IDE ---
class EditorScreen(Screen):
    BINDINGS = [
        Binding("ctrl+s", "save_current", "Save"),
        Binding("ctrl+n", "new_file", "New"),
        Binding("ctrl+b", "toggle_sidebar", "Sidebar"),
        Binding("ctrl+f", "cycle_focus", "Cycle View"),
        Binding("q", "quit", "Exit"),
    ]

    def on_mount(self) -> None:
        self.view_mode = "split"
        self.sidebar_visible = True
        self.current_path = ""

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("📁 EXPLORER", id="side-title")
                yield DirectoryTree("./", id="tree")
                with Grid(id="file-ops"):
                    yield Button("New", id="btn_new", variant="primary")
                    yield Button("Ren", id="btn_ren", variant="warning")
                    yield Button("Del", id="btn_del", variant="error")
                yield Static("📊 SYNTH STATS", id="stat-title")
                yield Static("Cells: 0\nNets: 0", id="synth_report")

            with Vertical(id="main-area"):
                with Horizontal(id="editors-container"):
                    with Vertical(id="design-pane"):
                        yield Static(
                            "📄 DESIGN: (None)", id="lbl_design", classes="label"
                        )
                        yield TextArea(id="design_ed", language="verilog")
                    with Vertical(id="tb-pane"):
                        yield Static(
                            "🧪 TESTBENCH: (None)", id="lbl_tb", classes="label"
                        )
                        yield TextArea(id="tb_ed", language="verilog")

                with Horizontal(id="action-bar"):
                    yield Button("🚀 SIM", id="run_sim", classes="eda-btn")
                    yield Button("🛠️ SYNTH", id="run_synth", classes="eda-btn")
                    yield Button("📐 SCHEM", id="run_schem", classes="eda-btn")
                    yield Button("📈 GTK", id="run_gtk", classes="eda-btn")
                    yield Button("🏄 SURF", id="run_surfer", classes="eda-btn")
                    yield Button("🔄 VIEW", id="btn_cycle", classes="eda-btn")

                yield Static("OUTPUT CONSOLE:", id="con-label")
                yield TextArea(id="console", read_only=True)
        yield Footer()

    # --- ROUTING ENGINE ---
    def on_directory_tree_file_selected(
        self, event: DirectoryTree.FileSelected
    ) -> None:
        self.current_path = str(event.path)
        fname = os.path.basename(self.current_path)
        try:
            with open(self.current_path, "r") as f:
                content = f.read()
            is_tb = (
                any(x in fname.lower() for x in ["tb.v", "_tb", "testbench"])
                or "$dump" in content
            )

            if is_tb:
                self.query_one("#tb_ed").text = content
                self.query_one("#lbl_tb").update(f"🧪 TESTBENCH: {fname}")
            else:
                self.query_one("#design_ed").text = content
                self.query_one("#lbl_design").update(f"📄 DESIGN: {fname}")
        except Exception as e:
            self.log_msg(f"Error: {e}")

    # --- ACTIONS ---
    def action_toggle_sidebar(self) -> None:
        self.sidebar_visible = not self.sidebar_visible
        self.query_one("#sidebar").display = self.sidebar_visible

    def action_cycle_focus(self) -> None:
        d_p, t_p = self.query_one("#design-pane"), self.query_one("#tb-pane")
        btn = self.query_one("#btn_cycle")
        if self.view_mode == "split":
            self.view_mode = "design"
            d_p.display, t_p.display = True, False
            btn.label = "📂 DESIGN"
        elif self.view_mode == "design":
            self.view_mode = "tb"
            d_p.display, t_p.display = False, True
            btn.label = "🧪 TB"
        else:
            self.view_mode = "split"
            d_p.display, t_p.display = True, True
            btn.label = "📐 SPLIT"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        cid = event.button.id
        if cid == "btn_cycle":
            self.action_cycle_focus()
        elif cid == "btn_new":
            self.app.push_screen(FileModal(mode="new"), self.add_file)
        elif cid == "btn_ren":
            self.app.push_screen(FileModal(mode="ren"), self.rename_file)
        elif cid == "btn_del":
            self.delete_file()
        elif cid in ["run_sim", "run_synth", "run_schem", "run_gtk", "run_surfer"]:
            self.handle_eda(cid)

    def add_file(self, name):
        if name:
            with open(name, "w") as f:
                f.write("// New Module\n")
            self.query_one("#tree").reload()

    def rename_file(self, new_name):
        if new_name and self.current_path:
            os.rename(self.current_path, new_name)
            self.query_one("#tree").reload()

    def delete_file(self):
        if self.current_path:
            os.remove(self.current_path)
            self.query_one("#tree").reload()

    def handle_eda(self, action):
        with open("top_active.v", "w") as f:
            f.write(self.query_one("#design_ed").text)
        with open("tb_active.v", "w") as f:
            f.write(self.query_one("#tb_ed").text)

        if action == "run_sim":
            self.exec_and_log(
                "iverilog -o sim.out top_active.v tb_active.v && vvp sim.out",
                "SIMULATION",
            )
        elif action == "run_synth":
            res = self.exec_and_log(
                "yosys -p 'read_verilog -sv top_active.v; proc; opt; stat'", "SYNTHESIS"
            )
            stats = [l.strip() for l in res.split("\n") if "Number of" in l]
            self.query_one("#synth_report").update("\n".join(stats[:4]))
        elif action == "run_schem":
            subprocess.run(
                "yosys -p 'read_verilog -sv top_active.v; proc; opt; show -format dot -prefix forge_out'",
                shell=True,
            )
            if os.path.exists("forge_out.dot"):
                subprocess.run("dot -Tpng forge_out.dot -o forge_out.png", shell=True)
                subprocess.Popen(["xdg-open", "forge_out.png"])
        elif action == "run_gtk":
            if os.path.exists("dump.vcd"):
                subprocess.Popen(["gtkwave", "dump.vcd"])
        elif action == "run_surfer":
            if os.path.exists("dump.vcd"):
                subprocess.Popen(["surfer", "dump.vcd"])

    def exec_and_log(self, cmd, title):
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        time_stamp = datetime.datetime.now().strftime("%H:%M:%S")
        f_out = f"╔{'═'*40}╗\n║ [{time_stamp}] {title} RESULTS ║\n╠{'═'*40}╣\n{res.stdout}{res.stderr}\n╚{'═'*40}╝"
        self.query_one("#console").text = f_out
        return res.stdout

    def log_msg(self, msg):
        self.query_one("#console").text += f"\n[SYS]: {msg}"


# --- 4. ERROR-FREE CSS ---
class AnandForgeApp(App):
    CSS = """
    #intro-container { align: center middle; background: #050505; }
    #logo { color: #D4AF37; text-align: center; }
    #status { color: #00FF41; margin-top: 1; }
    #designer-tag { color: #FFA500; margin-top: 1; border-top: solid #333; padding-top: 1; text-style: italic; }
    #blink-text { color: white; margin-top: 2; }
    
    #sidebar { width: 32; border-right: tall #00FF41; background: #0a0a0a; }
    #side-title, #stat-title { background: #00FF41; color: black; text-align: center; text-style: bold; }
    #file-ops { grid-size: 3; height: 3; margin: 1; }
    
    .label { background: #1a1a1a; color: #00FF41; padding: 0 1; border-bottom: solid #00FF41; text-style: bold; }
    TextArea { height: 1fr; border: solid #333; background: #050505; }
    #console { height: 12; background: #000; color: #00FF41; border-top: double #00FF41; }
    
    #action-bar { height: 4; align: center middle; background: #111; border-top: solid #333; }
    .eda-btn { margin: 0 1; min-width: 9; background: #222; border: solid #444; }
    .eda-btn:hover { background: #00FF41; color: black; }
    
    #modal { padding: 2; background: #1a1a1a; border: thick #00FF41; align: center middle; height: 12; width: 45; }
    #synth_report { color: #FFA500; padding: 1; }
    """

    def on_mount(self) -> None:
        self.push_screen(IntroScreen())


if __name__ == "__main__":
    AnandForgeApp().run()
