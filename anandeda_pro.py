import streamlit as st
from streamlit_ace import st_ace
import os
import subprocess
import tempfile
import graphviz
from PIL import Image
import io
from themes import THEMES

st.set_page_config(
    page_title="AnandEDA Pro - VLSI Playground",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session State
if "files" not in st.session_state:
    st.session_state.files = (
        {}
    )  # filename: {'content': str, 'type': 'design'/'tb', 'lang': 'verilog'/'systemverilog'}
if "theme" not in st.session_state:
    st.session_state.theme = "VS Code Dark"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "split"
if "language" not in st.session_state:
    st.session_state.language = "verilog"
if "wave_viewer" not in st.session_state:
    st.session_state.wave_viewer = "gtkwave"
if "console_output" not in st.session_state:
    st.session_state.console_output = ""
if "schematic_png" not in st.session_state:
    st.session_state.schematic_png = None
if "vcd_path" not in st.session_state:
    st.session_state.vcd_path = None

# Get current theme
theme = THEMES[st.session_state.theme]

# Enhanced Professional CSS
css = f"""
<style>
    .stApp {{
        background: {theme['gradient']};
        color: {theme['txt']};
        font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95%;
    }}
    h1, h2, h3 {{
        color: {theme['acc']};
        font-weight: 600;
    }}
    .stButton > button {{
        background-color: {theme['acc']};
        color: {theme['txt']};
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: 500;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s;
        height: auto;
        width: 100%;
    }}
    .stButton > button:hover {{
        background-color: {theme['accent2']};
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }}
    .tab-button {{
        background-color: {theme['con']};
        color: {theme['txt']};
        border: 2px solid {theme['acc']};
        border-bottom: none;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        margin-right: 8px;
        font-weight: bold;
        transition: all 0.3s;
    }}
    .active-tab {{
        background-color: {theme['acc']};
        color: {theme['txt']};
    }}
    .ace_editor, .ace_gutter, .ace_content {{
        background-color: {theme['con']} !important;
        color: {theme['txt']} !important;
    }}
    .stTextArea > div > div > textarea {{
        background-color: {theme['con']};
        color: {theme['txt']};
        border-radius: 8px;
        border: 1px solid {theme['acc']};
    }}
    .stSelectbox > div > div {{
        background-color: {theme['con']};
        border-radius: 8px;
        border: 1px solid {theme['acc']};
    }}
    .sidebar .sidebar-content {{
        background: {theme['con']};
    }}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/circuit.png", width=80)
    st.title("AnandEDA Pro")
    st.markdown("**Professional VLSI Playground**")

    st.session_state.theme = st.selectbox(
        "🎨 Theme",
        options=list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.theme),
    )
    st.session_state.language = st.selectbox(
        "🌐 Language", ["verilog", "systemverilog"]
    )
    st.session_state.view_mode = st.selectbox(
        "👀 View Mode", ["split", "focus_design", "focus_tb"]
    )
    st.session_state.wave_viewer = st.selectbox("🌊 Wave Viewer", ["gtkwave", "surfer"])

    st.markdown("---")
    st.subheader("📁 File Manager")
    new_name = st.text_input("New File Name (no extension)")
    file_type = st.selectbox("Type", ["design", "tb"], key="new_type")
    if st.button("➕ Create File") and new_name.strip():
        ext = ".v" if st.session_state.language == "verilog" else ".sv"
        filename = f"{new_name.strip()}{ext}"
        if filename in st.session_state.files:
            st.error("File already exists!")
        else:
            st.session_state.files[filename] = {
                "content": "",
                "type": file_type,
                "lang": st.session_state.language,
            }
            st.success(f"Created {filename}")
            st.rerun()

    if st.session_state.files:
        st.markdown("---")
        for file in list(st.session_state.files):
            with st.expander(f"📄 {file}", expanded=False):
                new_base = st.text_input(
                    "Rename to", value=file.rsplit(".", 1)[0], key=f"rn_input_{file}"
                )
                col_rename, col_del = st.columns(2)
                if col_rename.button("Rename", key=f"rn_btn_{file}"):
                    ext = ".v" if st.session_state.language == "verilog" else ".sv"
                    new_file = f"{new_base}{ext}"
                    if new_file != file and new_file not in st.session_state.files:
                        st.session_state.files[new_file] = st.session_state.files.pop(
                            file
                        )
                        st.success("Renamed!")
                        st.rerun()
                    else:
                        st.error("Invalid name or exists")
                if col_del.button("🗑️ Delete", key=f"del_btn_{file}"):
                    del st.session_state.files[file]
                    st.success("Deleted!")
                    st.rerun()

# File Tabs
if st.session_state.files:
    st.markdown("### 📂 Open Files")
    cols = st.columns(len(st.session_state.files))
    for idx, file in enumerate(st.session_state.files):
        with cols[idx]:
            active_class = (
                "active-tab"
                if file
                in [
                    f
                    for f in st.session_state.files
                    if st.session_state.files[f]["type"] == "design"
                    or st.session_state.files[f]["type"] == "tb"
                ]
                else ""
            )  # always active for simplicity
            if st.button(file, key=f"tab_{file}", help="Currently editing"):
                pass  # tabs are visual, editing below

# Auto detect design and tb files
design_files = [
    f for f in st.session_state.files if st.session_state.files[f]["type"] == "design"
]
tb_files = [
    f for f in st.session_state.files if st.session_state.files[f]["type"] == "tb"
]

# Editor
if not st.session_state.files:
    st.info("👈 Create files in sidebar to start coding!")
else:
    if st.session_state.view_mode == "split" and design_files and tb_files:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔧 Design Code")
            design_file = design_files[0]  # auto use first
            lang = (
                "verilog"
                if st.session_state.files[design_file]["lang"] == "verilog"
                else "systemverilog"
            )
            code = st_ace(
                value=st.session_state.files[design_file]["content"],
                language=lang,
                theme=theme["ace"],
                height=600,
                auto_update=True,
                key="ace_design_unique",
            )
            st.session_state.files[design_file]["content"] = code
        with col2:
            st.markdown("### 🧪 Testbench Code")
            tb_file = tb_files[0]  # auto use first
            lang = (
                "verilog"
                if st.session_state.files[tb_file]["lang"] == "verilog"
                else "systemverilog"
            )
            code = st_ace(
                value=st.session_state.files[tb_file]["content"],
                language=lang,
                theme=theme["ace"],
                height=600,
                auto_update=True,
                key="ace_tb_unique",
            )
            st.session_state.files[tb_file]["content"] = code
    else:
        target = "design" if "design" in st.session_state.view_mode else "tb"
        target_files = design_files if target == "design" else tb_files
        if target_files:
            file = target_files[0]
            st.markdown(
                f"### {'🔧 Design' if target == 'design' else '🧪 Testbench'} Code - {file}"
            )
            lang = (
                "verilog"
                if st.session_state.files[file]["lang"] == "verilog"
                else "systemverilog"
            )
            code = st_ace(
                value=st.session_state.files[file]["content"],
                language=lang,
                theme=theme["ace"],
                height=700,
                auto_update=True,
                key=f"ace_focus_{target}",
            )
            st.session_state.files[file]["content"] = code
        else:
            st.warning(f"No {target} files yet!")

# Action Buttons
st.markdown("---")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("🚀 Run Simulation"):
        if not st.session_state.files:
            st.error("No files to simulate!")
        else:
            with tempfile.TemporaryDirectory() as tmp:
                for f, data in st.session_state.files.items():
                    with open(os.path.join(tmp, f), "w") as fh:
                        fh.write(data["content"])
                os.chdir(tmp)
                output = ""
                vcd_generated = False
                if st.session_state.language == "verilog":
                    compile_res = subprocess.run(
                        ["iverilog", "-o", "sim.out"]
                        + list(st.session_state.files.keys()),
                        capture_output=True,
                        text=True,
                    )
                    if compile_res.returncode == 0:
                        sim_res = subprocess.run(
                            ["vvp", "sim.out"], capture_output=True, text=True
                        )
                        output = sim_res.stdout + sim_res.stderr
                        vcd_generated = os.path.exists("dump.vcd")
                    else:
                        output = compile_res.stderr
                else:  # systemverilog with verilator (simplified)
                    tb_name = tb_files[0].rsplit(".", 1)[0] if tb_files else "tb"
                    res = subprocess.run(
                        ["verilator", "--binary", "--trace", "--top-module", tb_name]
                        + list(st.session_state.files.keys()),
                        capture_output=True,
                        text=True,
                    )
                    output = res.stdout + res.stderr
                    if res.returncode == 0 and os.path.exists("obj_dir"):
                        run_res = subprocess.run(
                            ["./obj_dir/V" + tb_name], capture_output=True, text=True
                        )
                        output += "\n" + run_res.stdout + run_res.stderr
                    vcd_generated = os.path.exists("dump.vcd")
                st.session_state.console_output = output or "No output"
                if vcd_generated:
                    st.session_state.vcd_path = os.path.join(tmp, "dump.vcd")

with c2:
    if st.button("🌊 View Waves"):
        if st.session_state.vcd_path and os.path.exists(st.session_state.vcd_path):
            viewer = (
                "gtkwave" if st.session_state.wave_viewer == "gtkwave" else "surfer"
            )
            subprocess.Popen([viewer, st.session_state.vcd_path])
            st.success("Wave viewer opened!")
        else:
            st.warning("Run simulation first to generate VCD")

with c3:
    if st.button("📐 View Schematic"):
        if design_files:
            with tempfile.TemporaryDirectory() as tmp:
                for f in design_files:
                    with open(os.path.join(tmp, f), "w") as fh:
                        fh.write(st.session_state.files[f]["content"])
                os.chdir(tmp)
                subprocess.run(
                    [
                        "yosys",
                        "-p",
                        f"read_verilog {' '.join(design_files)}; synth; show -format png -prefix schematic",
                    ],
                    stdout=subprocess.DEVNULL,
                )
                png_path = os.path.join(tmp, "schematic.png")
                if os.path.exists(png_path):
                    st.session_state.schematic_png = png_path
                    st.success("Schematic generated!")
        else:
            st.warning("Need at least one design file")

with c4:
    if st.session_state.vcd_path and os.path.exists(st.session_state.vcd_path):
        with open(st.session_state.vcd_path, "rb") as f:
            st.download_button(
                "💾 Download VCD", f.read(), "dump.vcd", "application/octet-stream"
            )

with c5:
    if st.session_state.schematic_png and os.path.exists(
        st.session_state.schematic_png
    ):
        with open(st.session_state.schematic_png, "rb") as f:
            st.download_button(
                "💾 Download Schematic", f.read(), "schematic.png", "image/png"
            )

# Console
st.markdown("---")
st.subheader("📟 Console Output")
st.code(st.session_state.console_output, language="text")

# Schematic Display
if st.session_state.schematic_png and os.path.exists(st.session_state.schematic_png):
    st.markdown("---")
    st.subheader("📐 Gate-Level Schematic")
    st.image(st.session_state.schematic_png, use_column_width=True)

st.caption("AnandEDA Pro by Mayank Anand © 2026 | Professional Local VLSI IDE")
