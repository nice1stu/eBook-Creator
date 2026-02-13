# main_gui.py - Version 2.6.2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
from converter_logic import eBookConverterLogic

class ReviewDialog(simpledialog.Dialog):
    def __init__(self, parent, filename, t, a):
        self.filename = filename
        self.t, self.a = t, a
        super().__init__(parent, "Confirm Metadata")

    def body(self, master):
        tk.Label(master, text=f"Processing: {self.filename}", fg="blue", wraplength=300).pack(pady=5)
        
        tk.Label(master, text="Title:").pack()
        self.e1 = tk.Entry(master, width=50)
        self.e1.insert(0, self.t); self.e1.pack()

        tk.Label(master, text="Author:").pack()
        self.e2 = tk.Entry(master, width=50)
        self.e2.insert(0, self.a); self.e2.pack()

        tk.Button(master, text="🔄 Swap Title/Author", command=self.swap).pack(pady=5)
        return self.e1

    def swap(self):
        t, a = self.e1.get(), self.e2.get()
        self.e1.delete(0, tk.END); self.e1.insert(0, a)
        self.e2.delete(0, tk.END); self.e2.insert(0, t)

    def apply(self):
        self.result = (self.e1.get(), self.e2.get())

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("eBook Creator v2.6.2")
        self.logic = eBookConverterLogic()
        self.output_dir = os.path.join(os.getcwd(), "Processed")
        tk.Button(root, text="📁 Batch Process Folder", command=self.run_batch, height=2, width=30).pack(pady=50)

    def run_batch(self):
        folder = filedialog.askdirectory()
        if not folder: return
        files = [f for f in os.listdir(folder) if f.lower().endswith(self.logic.allowed_formats)]
        
        for filename in files:
            full_path = os.path.join(folder, filename)
            # 1. Parse from filename
            parsed_t, parsed_a = self.logic.parse_filename(full_path)
            # 2. Scrape from Google
            data = self.logic.fetch_metadata_online(parsed_t, parsed_a)
            
            # Use Scraped data if available, else use Parsed data
            display_t = data['title'] if data else parsed_t
            display_a = data['author'] if data else parsed_a
            
            # 3. Mandatory User Review
            dialog = ReviewDialog(self.root, filename, display_t, display_a)
            if dialog.result:
                final_t, final_a = dialog.result
                # If user changed text, try to get a new cover for the corrected title
                if data and (final_t != data['title']):
                    data = self.logic.fetch_metadata_online(final_t, final_a)
                
                cover = self.logic.download_cover(data['cover_url']) if data else None
                self.logic.convert_to_epub(full_path, self.output_dir, final_t, final_a, cover)
            else:
                continue # Skip this file if user hits Cancel

        messagebox.showinfo("Done", "Batch Processing Complete!")

if __name__ == "__main__":
    root = tk.Tk(); app = ConverterApp(root); root.mainloop()