# main_gui.py - Version 2.4.0
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import requests
import threading # To keep the UI from freezing during batch
from converter_logic import eBookConverterLogic

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI eBook Creator v2.4.0 - Batch Edition")
        self.root.geometry("550x650")
        self.logic = eBookConverterLogic()
        
        self.output_dir = os.path.join(os.getcwd(), "Processed")
        if not os.path.exists(self.output_dir): os.makedirs(self.output_dir)

        self.setup_ui()

    def setup_ui(self):
        # Single File Section
        tk.Label(self.root, text="--- Single File Mode ---", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Button(self.root, text="📁 Select Single File", command=self.select_single).pack()

        # Metadata Fields
        self.ent_title = tk.Entry(self.root, width=45); self.ent_title.pack(pady=5)
        self.ent_author = tk.Entry(self.root, width=45); self.ent_author.pack(pady=5)
        self.lbl_cover = tk.Label(self.root, text="No cover", fg="gray"); self.lbl_cover.pack()
        
        # Batch Section
        tk.Frame(self.root, height=2, bd=1, relief="sunken").pack(fill="x", padx=20, pady=20)
        tk.Label(self.root, text="--- Batch Mode ---", font=("Arial", 10, "bold")).pack()
        tk.Button(self.root, text="🗂️ Select Folder to Convert All", command=self.start_batch_thread, bg="#3498db", fg="white").pack(pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=20)
        
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w").pack(side="bottom", fill="x")

        # Convert Button for Single Mode
        self.btn_single = tk.Button(self.root, text="Convert Single File", command=self.run_single_conversion, bg="#2ecc71", fg="white")
        self.btn_single.pack(pady=10)

    def select_single(self):
        f = filedialog.askopenfilename()
        if not f: return
        self.current_file = f
        t, a = self.logic.parse_filename(f)
        self.update_metadata_ui(t, a)

    def update_metadata_ui(self, t, a):
        self.ent_title.delete(0, tk.END); self.ent_title.insert(0, t)
        self.ent_author.delete(0, tk.END); self.ent_author.insert(0, a)
        data = self.logic.fetch_metadata_online(t, a)
        if data:
            self.ent_title.delete(0, tk.END); self.ent_title.insert(0, data['title'])
            self.ent_author.delete(0, tk.END); self.ent_author.insert(0, data['author'])
            self.cover_path = self.logic.download_cover(data['cover_url'])
            self.lbl_cover.config(text="Cover Found!", fg="green")
        else:
            self.cover_path = None
            self.lbl_cover.config(text="No cover found", fg="gray")

    def run_single_conversion(self):
        success, result = self.logic.convert_to_epub(self.current_file, self.output_dir, self.ent_title.get(), self.ent_author.get(), self.cover_path)
        if success: 
            os.startfile(self.output_dir)
            messagebox.showinfo("Done", "Conversion Complete!")

    def start_batch_thread(self):
        folder = filedialog.askdirectory()
        if not folder: return
        # We run this in a thread so the UI doesn't freeze
        threading.Thread(target=self.run_batch, args=(folder,), daemon=True).start()

    def run_batch(self, folder):
        files = [f for f in os.listdir(folder) if f.lower().endswith(('.txt', '.rtf', '.docx'))]
        if not files:
            messagebox.showinfo("Empty", "No compatible files found in folder.")
            return

        self.progress["maximum"] = len(files)
        count = 0
        
        for filename in files:
            count += 1
            full_path = os.path.join(folder, filename)
            self.status_var.set(f"Processing {count}/{len(files)}: {filename}")
            self.progress["value"] = count
            
            # 1. Parse
            t, a = self.logic.parse_filename(full_path)
            # 2. Scrape
            data = self.logic.fetch_metadata_online(t, a)
            final_t = data['title'] if data else t
            final_a = data['author'] if data else a
            cover = self.logic.download_cover(data['cover_url']) if data else None
            
            # 3. Convert
            self.logic.convert_to_epub(full_path, self.output_dir, final_t, final_a, cover)
            
        self.status_var.set("Batch Complete!")
        os.startfile(self.output_dir)
        messagebox.showinfo("Batch Done", f"Successfully processed {len(files)} files!")
        self.progress["value"] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()