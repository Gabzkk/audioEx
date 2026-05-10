import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import struct

try:
    from PIL import Image
except ImportError:
    import sys
    print("Error: Pillow library is required. Please install it using 'pip install Pillow'")
    sys.exit(1)

# Design Language from CTFskill.md
BG_PRIMARY = "#0d1117"
BG_SECONDARY = "#161b22"
BG_CARD = "#21262d"
BORDER = "#30363d"
ACCENT = "#58a6ff"
ACCENT_GREEN = "#3fb950"
ACCENT_RED = "#f85149"
ACCENT_YELLOW = "#d29922"
TEXT_PRIMARY = "#c9d1d9"
TEXT_MUTED = "#8b949e"
FONT_MONO = ("Courier New", 11)
FONT_UI = ("Arial", 11)

class CustomButton(tk.Button):
    def __init__(self, master, primary=True, **kwargs):
        super().__init__(master, **kwargs)
        if primary:
            self.configure(
                bg=ACCENT, fg="#0d1117", font=(FONT_UI[0], 11, "bold"),
                relief="flat", padx=20, pady=8, activebackground="#79b8ff",
                cursor="hand2", borderwidth=0
            )
        else:
            self.configure(
                bg=BG_SECONDARY, fg=TEXT_MUTED, font=(FONT_UI[0], 10),
                relief="solid", bd=1, padx=14, pady=6,
                activebackground=BORDER, activeforeground=TEXT_PRIMARY,
                cursor="hand2", highlightbackground=BORDER
            )

class StegoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CTF Tool - Audio Steganography (LSB)")
        self.geometry("600x550")
        self.configure(bg=BG_PRIMARY)
        self.resizable(False, False)

        # Header
        header_frame = tk.Frame(self, bg=BG_PRIMARY)
        header_frame.pack(fill="x", pady=(20, 10))
        tk.Label(header_frame, text="CTF Steganography Tool", font=(FONT_UI[0], 16, "bold"), bg=BG_PRIMARY, fg=TEXT_PRIMARY).pack()
        tk.Label(header_frame, text="Hide and extract binary audio inside image LSBs", font=(FONT_UI[0], 10), bg=BG_PRIMARY, fg=TEXT_MUTED).pack()

        # Notebook
        style = ttk.Style()
        style.theme_use("alt")
        style.configure("TNotebook", background=BG_PRIMARY, borderwidth=0)
        style.configure("TNotebook.Tab", padding=[15, 5], background=BG_SECONDARY, foreground=TEXT_MUTED,
                        borderwidth=1, bordercolor=BORDER, font=FONT_UI)
        style.map("TNotebook.Tab", background=[("selected", BG_CARD)], foreground=[("selected", TEXT_PRIMARY)],
                  expand=[("selected", [1, 1, 1, 0])])
        style.configure("TFrame", background=BG_CARD)

        notebook_frame = tk.Frame(self, bg=BG_PRIMARY, padx=20, pady=10)
        notebook_frame.pack(fill="both", expand=True)

        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill="both", expand=True)

        # Tabs
        self.tab_hide = ttk.Frame(self.notebook)
        self.tab_extract = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_hide, text="Hide Audio")
        self.notebook.add(self.tab_extract, text="Extract Audio")

        self.setup_hide_tab()
        self.setup_extract_tab()

        # Footer
        footer = tk.Frame(self, bg=BG_PRIMARY)
        footer.pack(fill="x", side="bottom", pady=15)
        tk.Frame(footer, bg=BORDER, height=1).pack(fill="x", padx=20, pady=(0, 10))
        tk.Label(footer, text="For authorized CTF competitions and educational use only.\nDo not use against systems without explicit permission.",
                 font=(FONT_UI[0], 9), bg=BG_PRIMARY, fg=TEXT_MUTED).pack()

    def create_file_selector(self, parent, label_text, is_save=False, filetypes=None):
        frame = tk.Frame(parent, bg=BG_CARD)
        frame.pack(fill="x", pady=8, padx=15)
        
        tk.Label(frame, text=label_text, bg=BG_CARD, fg=TEXT_PRIMARY, font=FONT_UI).pack(anchor="w", pady=(0, 2))
        
        inner = tk.Frame(frame, bg=BG_CARD)
        inner.pack(fill="x")
        
        var = tk.StringVar()
        entry = tk.Entry(inner, textvariable=var, font=FONT_MONO, bg=BG_SECONDARY, fg=TEXT_PRIMARY,
                         insertbackground=TEXT_PRIMARY, relief="flat", highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT)
        entry.pack(side="left", fill="x", expand=True, ipady=4, padx=(0, 10))
        
        def browse():
            if is_save:
                path = filedialog.asksaveasfilename(filetypes=filetypes, defaultextension=filetypes[0][1].replace('*',''))
            else:
                path = filedialog.askopenfilename(filetypes=filetypes)
            if path:
                var.set(path)
                
        CustomButton(inner, primary=False, text="Browse", command=browse).pack(side="right")
        return var

    def create_status_bar(self, parent):
        frame = tk.Frame(parent, bg=BG_CARD)
        frame.pack(fill="x", pady=10, padx=15, side="bottom")
        
        # We simulate the status badge from CTFskill.md
        badge_frame = tk.Frame(frame, bg="#273342", padx=2, pady=2)
        badge_frame.pack(side="left")
        status_label = tk.Label(badge_frame, text="INFO", font=(FONT_MONO[0], 10, "bold"), bg="#273342", fg=ACCENT)
        status_label.pack()
        
        msg_label = tk.Label(frame, text="Ready for input.", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_UI)
        msg_label.pack(side="left", padx=10)
        
        return badge_frame, status_label, msg_label

    def set_status(self, badge_frame, status_label, msg_label, state, message):
        states = {
            "OK": (ACCENT_GREEN, "#243530"),
            "ERROR": (ACCENT_RED, "#372a2f"),
            "INFO": (ACCENT, "#273342"),
            "WARN": (ACCENT_YELLOW, "#33312b")
        }
        fg, bg = states.get(state, (TEXT_MUTED, BG_SECONDARY))
        badge_frame.config(bg=bg)
        status_label.config(text=state, fg=fg, bg=bg)
        msg_label.config(text=message, fg=TEXT_PRIMARY)
        self.update()

    def setup_hide_tab(self):
        tk.Label(self.tab_hide, text="Select files to embed audio into an image (LSB encoding).", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_UI).pack(pady=(15, 5))
        
        self.hide_img_var = self.create_file_selector(self.tab_hide, "Input Image (Cover):", filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        self.hide_aud_var = self.create_file_selector(self.tab_hide, "Input Audio (Secret):", filetypes=[("Audio", "*.wav *.mp3 *.ogg *.flac"), ("All Files", "*.*")])
        
        self.hide_badge, self.hide_status, self.hide_msg = self.create_status_bar(self.tab_hide)
        
        btn_frame = tk.Frame(self.tab_hide, bg=BG_CARD)
        btn_frame.pack(pady=15)
        CustomButton(btn_frame, primary=True, text="Hide Audio", command=self.do_hide).pack()

    def setup_extract_tab(self):
        tk.Label(self.tab_extract, text="Select a PNG image to extract hidden audio from.", bg=BG_CARD, fg=TEXT_MUTED, font=FONT_UI).pack(pady=(15, 5))
        
        self.ext_img_var = self.create_file_selector(self.tab_extract, "Input Image (Stego):", filetypes=[("PNG Image", "*.png")])
        
        self.ext_badge, self.ext_status, self.ext_msg = self.create_status_bar(self.tab_extract)
        
        btn_frame = tk.Frame(self.tab_extract, bg=BG_CARD)
        btn_frame.pack(pady=15)
        CustomButton(btn_frame, primary=True, text="Extract Audio", command=self.do_extract).pack()

    def do_hide(self):
        img_path = self.hide_img_var.get()
        aud_path = self.hide_aud_var.get()
        
        if not all([img_path, aud_path]):
            self.set_status(self.hide_badge, self.hide_status, self.hide_msg, "ERROR", "Please fill all file paths.")
            return
            
        base_path, _ = os.path.splitext(img_path)
        out_path = f"{base_path}_stego.png"

        self.set_status(self.hide_badge, self.hide_status, self.hide_msg, "INFO", "Analyzing and encoding...")
        
        try:
            with open(aud_path, 'rb') as f:
                secret_data = f.read()
                
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            width, height = img.size
            data_len = len(secret_data)
            header = struct.pack('>I', data_len)
            full_data = header + secret_data
            
            total_bits = len(full_data) * 8
            max_bits = width * height * 3
            
            if total_bits > max_bits:
                self.set_status(self.hide_badge, self.hide_status, self.hide_msg, "ERROR", f"Image too small! Needs {total_bits//8} bytes max.")
                return
                
            img_data = bytearray(img.tobytes())
            idx = 0
            for byte in full_data:
                for i in range(7, -1, -1):
                    bit = (byte >> i) & 1
                    img_data[idx] = (img_data[idx] & 0xFE) | bit
                    idx += 1
                    
            encoded_img = Image.frombytes('RGB', img.size, bytes(img_data))
            encoded_img.save(out_path, "PNG")
            
            self.set_status(self.hide_badge, self.hide_status, self.hide_msg, "OK", f"Success! Embedded {data_len} bytes.")
            
        except Exception as e:
            self.set_status(self.hide_badge, self.hide_status, self.hide_msg, "ERROR", f"Failed: {str(e)}")

    def do_extract(self):
        img_path = self.ext_img_var.get()
        
        if not img_path:
            self.set_status(self.ext_badge, self.ext_status, self.ext_msg, "ERROR", "Please select an image file.")
            return
            
        base_path, _ = os.path.splitext(img_path)
        out_path = f"{base_path}_extracted.wav"
            
        self.set_status(self.ext_badge, self.ext_status, self.ext_msg, "INFO", "Extracting data...")
        
        try:
            img = Image.open(img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            img_data = img.tobytes()
            
            if len(img_data) < 32:
                self.set_status(self.ext_badge, self.ext_status, self.ext_msg, "ERROR", "Image too small to contain data.")
                return
                
            length_val = 0
            for i in range(32):
                bit = img_data[i] & 1
                length_val = (length_val << 1) | bit
                
            if length_val == 0 or length_val > (len(img_data) - 32) // 8:
                self.set_status(self.ext_badge, self.ext_status, self.ext_msg, "ERROR", f"Invalid size header: {length_val}. No hidden data found.")
                return
                
            audio_data = bytearray(length_val)
            idx = 32
            for b in range(length_val):
                byte_val = 0
                for _ in range(8):
                    bit = img_data[idx] & 1
                    byte_val = (byte_val << 1) | bit
                    idx += 1
                audio_data[b] = byte_val
                
            with open(out_path, 'wb') as f:
                f.write(audio_data)
                
            self.set_status(self.ext_badge, self.ext_status, self.ext_msg, "OK", f"Success! Extracted {length_val} bytes.")
            
        except Exception as e:
            self.set_status(self.ext_badge, self.ext_status, self.ext_msg, "ERROR", f"Failed: {str(e)}")

if __name__ == "__main__":
    app = StegoApp()
    app.mainloop()
