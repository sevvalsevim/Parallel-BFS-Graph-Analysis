import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import threading
import os
from PIL import Image

# --- GIRLY-TECH RENK PALETİ ---
COLOR_ACCENT_PINK = "#FF69B4"   # Canlı Hot Pink (Vurgular ve Butonlar)
COLOR_PASTEL_PURPLE = "#DDA0DD" # Lolipop Mor / Lila (Yazılar ve Başlıklar)
COLOR_DARK_PURPLE = "#4B0082"   # İndigo Mor (Hover Durumları)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue") 

class GirlyParallelBFSApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere Ayarları
        self.title("High-Performance Graph Analytics - Parallel BFS (✨ Girls Edition)")
        self.geometry("1100x720")
        self.selected_file = ""

        # =====================================================================
        # SOL KONTROL PANELİ
        # =====================================================================
        self.left_panel = ctk.CTkFrame(self, width=300, corner_radius=15, border_width=2, border_color=COLOR_ACCENT_PINK)
        self.left_panel.pack(side="left", fill="y", padx=15, pady=15)
        self.left_panel.pack_propagate(False)

        # Panel Ana Başlığı (Işıltılı Başlık)
        self.lbl_main_title = ctk.CTkLabel(self.left_panel, text="✨ BFS ENGINE", font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=COLOR_ACCENT_PINK)
        self.lbl_main_title.pack(pady=(25, 5), padx=20, anchor="w")
        
        self.lbl_sub_title = ctk.CTkLabel(self.left_panel, text="MPI Parallel Traversal Control", font=ctk.CTkFont(size=12, slant="italic"), text_color=COLOR_PASTEL_PURPLE)
        self.lbl_sub_title.pack(pady=(0, 25), padx=20, anchor="w")

        # --- SEKTÖR 1: VERİ SETİ SEÇİMİ ---
        self.frame_dataset = ctk.CTkFrame(self.left_panel, border_width=1, border_color="#3A3A3A")
        self.frame_dataset.pack(fill="x", padx=15, pady=10)
        
        self.lbl_section_1 = ctk.CTkLabel(self.frame_dataset, text="💖 GRAPH DATASET", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_PASTEL_PURPLE)
        self.lbl_section_1.pack(pady=(10, 5), padx=15, anchor="w")

        self.btn_browse = ctk.CTkButton(self.frame_dataset, text="Select Dataset (.txt)", fg_color=COLOR_ACCENT_PINK, hover_color="#FF1493", text_color="#FFFFFF", font=ctk.CTkFont(weight="bold"), corner_radius=8, command=self.browse_file)
        self.btn_browse.pack(pady=8, padx=15, fill="x")

        self.lbl_file = ctk.CTkLabel(self.frame_dataset, text="No dataset selected.", text_color="#FF8484", font=ctk.CTkFont(size=12, slant="italic"), wraplength=240)
        self.lbl_file.pack(pady=(0, 10), padx=15, anchor="w")

        # --- SEKTÖR 2: DONANIM YAPILANDIRMASI ---
        self.frame_hardware = ctk.CTkFrame(self.left_panel, border_width=1, border_color="#3A3A3A")
        self.frame_hardware.pack(fill="x", padx=15, pady=10)

        self.lbl_section_2 = ctk.CTkLabel(self.frame_hardware, text="🚀 PARALLEL CORES (MPI)", font=ctk.CTkFont(size=12, weight="bold"), text_color=COLOR_PASTEL_PURPLE)
        self.lbl_section_2.pack(pady=(10, 5), padx=15, anchor="w")
        
        self.core_combo = ctk.CTkComboBox(self.frame_hardware, values=["1", "2", "4"], border_color=COLOR_ACCENT_PINK, button_color=COLOR_ACCENT_PINK)
        self.core_combo.set("4")
        self.core_combo.pack(pady=(5, 15), padx=15, fill="x")

        # --- ÇALIŞTIRMA VE ANALİZ BUTONLARI ---
        self.btn_run = ctk.CTkButton(self.left_panel, text="🎀 LAUNCH ALGORITHM", fg_color="#BA55D3", hover_color=COLOR_DARK_PURPLE, text_color="#FFFFFF", font=ctk.CTkFont(size=14, weight="bold"), corner_radius=10, command=self.start_bfs_thread)
        self.btn_run.pack(pady=(25, 10), padx=15, fill="x")

        self.btn_plot = ctk.CTkButton(self.left_panel, text="📊 Show Dashboard Charts", fg_color="transparent", border_width=1, border_color=COLOR_ACCENT_PINK, text_color=COLOR_ACCENT_PINK, hover_color="#2B1A2F", corner_radius=10, state="disabled", command=self.load_charts)
        self.btn_plot.pack(pady=5, padx=15, fill="x")

        # --- EKİP KÜNYESİ ---
        self.frame_team = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.frame_team.pack(side="bottom", fill="x", padx=15, pady=20)
        
        ctk.CTkLabel(self.frame_team, text="DEVELOPED BY", font=ctk.CTkFont(size=10, weight="bold"), text_color=COLOR_PASTEL_PURPLE).pack(anchor="w")
        ctk.CTkLabel(self.frame_team, text="Ayşegül • Mine • Sude • Şevval", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=COLOR_ACCENT_PINK).pack(anchor="w", pady=2)
        ctk.CTkLabel(self.frame_team, text="Computer Engineering Senior Project 👩‍💻", font=ctk.CTkFont(size=11), text_color="gray").pack(anchor="w")

        # =====================================================================
        # SAĞ LOG & PANEL GÖRÜNÜMÜ
        # =====================================================================
        self.right_panel = ctk.CTkFrame(self, corner_radius=15, border_width=1, border_color="#2A2A2A")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.tabview = ctk.CTkTabview(self.right_panel)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_console = self.tabview.add("Live System Logs")
        self.tab_charts = self.tabview.add("Analytics Dashboard")

        # Terminal Ekranı
        self.txt_console = ctk.CTkTextbox(self.tab_console, text_color="#E6E6FA", font=ctk.CTkFont(family="Consolas", size=12), border_width=1, border_color="#333333")
        self.txt_console.pack(fill="both", expand=True, padx=5, pady=5)
        
        # --- 4'LÜ GRAFİK ALANI (2x2 Grid) ---
        self.grid_frame = ctk.CTkFrame(self.tab_charts, fg_color="transparent")
        self.grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.grid_frame.grid_rowconfigure(0, weight=1)
        self.grid_frame.grid_rowconfigure(1, weight=1)
        self.grid_frame.grid_columnconfigure(0, weight=1)
        self.grid_frame.grid_columnconfigure(1, weight=1)

        # Grafik 1: Size Analysis (Sol Üst)
        self.lbl_chart1 = ctk.CTkLabel(self.grid_frame, text="📊 Graph Size Chart waiting...", text_color=COLOR_PASTEL_PURPLE)
        self.lbl_chart1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Grafik 2: Density Analysis (Sağ Üst)
        self.lbl_chart2 = ctk.CTkLabel(self.grid_frame, text="📊 Density Chart waiting...", text_color=COLOR_PASTEL_PURPLE)
        self.lbl_chart2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Grafik 3: Execution Time (Sol Alt)
        self.lbl_chart3 = ctk.CTkLabel(self.grid_frame, text="📊 Runtime Processors Chart waiting...", text_color=COLOR_PASTEL_PURPLE)
        self.lbl_chart3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Grafik 4: Speedup Analysis (Sağ Alt)
        self.lbl_chart4 = ctk.CTkLabel(self.grid_frame, text="📊 Speedup Chart waiting...", text_color=COLOR_PASTEL_PURPLE)
        self.lbl_chart4.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            self.selected_file = file_path
            self.lbl_file.configure(text=f"✔ {os.path.basename(file_path)}", text_color=COLOR_ACCENT_PINK)

    def start_bfs_thread(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "Please select your 'roadNet-PA.txt' file first! 🎀")
            return
        
        self.btn_run.configure(state="disabled", text="PROCESSING... 💞")
        self.txt_console.delete("1.0", ctk.END)
        self.txt_console.insert(ctk.END, "[INFO] Initializing MPI Cluster Environment...\n")
        self.tabview.set("Live System Logs")
        
        threading.Thread(target=self.run_parallel_bfs, daemon=True).start()

    def run_parallel_bfs(self):
        cores = self.core_combo.get()
        
        current_dir = os.getcwd()
        python_path = os.path.join(current_dir, "venv", "Scripts", "python.exe")
        script_path = os.path.join(current_dir, "parallel_bfs.py")
        
        cmd = ["mpiexec", "-n", cores, python_path, script_path]
        
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
            
            while True:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    self.txt_console.insert(ctk.END, line)
                    self.txt_console.see(ctk.END)
            
            process.wait()
            
        except Exception as e:
            self.txt_console.insert(ctk.END, f"\n[CRITICAL ERROR]: {str(e)}")
        
        finally:
            self.btn_run.configure(state="normal", text="🎀 LAUNCH ALGORITHM")
            self.btn_plot.configure(state="normal")
            messagebox.showinfo("Success", "Parallel BFS job completed successfully! ✨")

    def load_charts(self):
        comp_path = "complexity_analysis.png"
        perf_path = "performance_results.png"
        
        if os.path.exists(comp_path) and os.path.exists(perf_path):
            try:
                img_comp = Image.open(comp_path)
                width, height = img_comp.width, img_comp.height
                
                box_size = (0, 0, width // 2, height)
                img_size = img_comp.crop(box_size)
                
                box_density = (width // 2, 0, width, height)
                img_density = img_comp.crop(box_density)
                
                img_perf = Image.open(perf_path)
                w_p, h_p = img_perf.width, img_perf.height
                
                box_time = (0, 0, w_p // 2, h_p)
                img_time = img_perf.crop(box_time)
                
                box_speedup = (w_p // 2, 0, w_p, h_p)
                img_speedup = img_perf.crop(box_speedup)

                ctk_size = ctk.CTkImage(light_image=img_size, dark_image=img_size, size=(360, 220))
                ctk_density = ctk.CTkImage(light_image=img_density, dark_image=img_density, size=(360, 220))
                ctk_time = ctk.CTkImage(light_image=img_time, dark_image=img_time, size=(360, 220))
                ctk_speedup = ctk.CTkImage(light_image=img_speedup, dark_image=img_speedup, size=(360, 220))

                self.lbl_chart1.configure(image=ctk_size, text="")
                self.lbl_chart2.configure(image=ctk_density, text="")
                self.lbl_chart3.configure(image=ctk_time, text="")
                self.lbl_chart4.configure(image=ctk_speedup, text="")
                
                self.tabview.set("Analytics Dashboard")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to slice or render chart images: {str(e)}")
        else:
            messagebox.showwarning("Not Found", "Missing analysis assets. Please ensure both 'complexity_analysis.png' and 'performance_results.png' exist. 💕")

if __name__ == "__main__":
    app = GirlyParallelBFSApp()
    app.mainloop()