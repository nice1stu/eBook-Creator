import tkinter as tk
from tkinter import filedialog, messagebox
import os
import requests
from converter_logic import eBookConverterLogic

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("eBook Creator v2.3.1")
        self.root.geometry("500x500")
        self.logic = eBookConverterLogic()
        self.cover_path = None
        self.current_file = None
        
        # Setup Default Paths
        self.source_dir = os.path.join(os.getcwd(), "To_Be_Processed")
        self.output_dir = os.path.join(os.getcwd(), "Processed")
        for d in [self.source_dir, self.output_dir]:
            if not os.path.exists(d): os.makedirs(d)

        tk.Label(root, text="Step 1: Select File", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Button(root, text="📁 Choose File", command=self.select_and_parse).pack()
        
        tk.Label(root, text="Title:").pack(pady=(20,0))
        self.ent_title = tk.Entry(root, width=40)
        self.ent_title.pack()
        
        tk.Label(root, text="Author:").pack(pady=(10,0))
        self.ent_author = tk.Entry(root, width=40)
        self.ent_author.pack()

        self.lbl_cover = tk.Label(root, text="No cover", fg="gray")
        self.lbl_cover.pack(pady=10)
        
        tk.Button(root, text="Convert Now", command=self.run_conversion, bg="green", fg="white", height=2).pack(pady=20)

    def select_and_parse(self):
        f = filedialog.askopenfilename(initialdir=self.source_dir)
        if not f: return
        self.current_file = f
        t, a = self.logic.parse_filename(f)
        self.ent_title.delete(0, tk.END); self.ent_title.insert(0, t)
        self.ent_author.delete(0, tk.END); self.ent_author.insert(0, a)
        
        # Fetch Online
        data = self.logic.fetch_metadata_online(t, a)
        if data:
            self.ent_title.delete(0, tk.END); self.ent_title.insert(0, data['title'])
            self.ent_author.delete(0, tk.END); self.ent_author.insert(0, data['author'])
            if data['cover_url']: self.download_cover(data['cover_url'])

    def download_cover(self, url):
        try:
            r = requests.get(url)
            self.cover_path = "temp_cover.jpg"
            with open(self.cover_path, 'wb') as f: f.write(r.content)
            self.lbl_cover.config(text="Cover: Found!", fg="green")
        except: pass

    def run_conversion(self):
        if not self.current_file:
            messagebox.showwarning("Warning", "Please select a file first!")
            return
        
        success, result = self.logic.convert_to_epub(
            self.current_file, self.output_dir, 
            self.ent_title.get(), self.ent_author.get(), self.cover_path
        )
        
        if success:
            # This line opens the folder and highlights the new file
            os.startfile(self.output_dir) 
            messagebox.showinfo("Success", f"EPUB Created: {os.path.basename(result)}")
            if os.path.exists("temp_cover.jpg"): os.remove("temp_cover.jpg")
            self.cover_path = None
        else:
            messagebox.showerror("Error", f"Conversion failed: {result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()