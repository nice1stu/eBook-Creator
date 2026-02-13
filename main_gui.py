# main_gui.py - Version 2.0.0
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from converter_logic import eBookConverterLogic

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal eBook Creator v2.0.0")
        self.root.geometry("500x450")
        self.logic = eBookConverterLogic()
        self.cover_path = None

        # --- UI Layout ---
        tk.Label(root, text="Step 1: Enter Book Details", font=("Arial", 10, "bold")).pack(pady=10)

        tk.Label(root, text="Book Title:").pack()
        self.ent_title = tk.Entry(root, width=45)
        self.ent_title.pack(pady=5)

        tk.Label(root, text="Author Name:").pack()
        self.ent_author = tk.Entry(root, width=45)
        self.ent_author.pack(pady=5)

        tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=20, pady=15)

        tk.Label(root, text="Step 2: Add Visuals", font=("Arial", 10, "bold")).pack()
        self.lbl_cover_status = tk.Label(root, text="No cover selected", fg="gray")
        self.lbl_cover_status.pack()
        
        self.btn_cover = tk.Button(root, text="Select Cover Image (JPG/PNG)", command=self.get_cover)
        self.btn_cover.pack(pady=5)

        tk.Frame(root, height=2, bd=1, relief="sunken").pack(fill="x", padx=20, pady=15)

        self.btn_convert = tk.Button(
            root, text="Step 3: Choose File & Convert", 
            command=self.run_conversion, 
            bg="#2ecc71", fg="white", font=("Arial", 10, "bold"), height=2
        )
        self.btn_convert.pack(pady=10)

        # Status Bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")

    def get_cover(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if path:
            self.cover_path = path
            self.lbl_cover_status.config(text=f"Cover: {os.path.basename(path)}", fg="green")

    def run_conversion(self):
        title = self.ent_title.get().strip() or "Untitled"
        author = self.ent_author.get().strip() or "Unknown Author"

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("All Supported", "*.rtf *.txt *.pdf *.docx"),
                ("RTF Document", "*.rtf"),
                ("Text File", "*.txt"),
                ("PDF Document", "*.pdf"),
                ("Word Document", "*.docx")
            ]
        )

        if file_path:
            self.status_var.set("Converting... Please wait.")
            self.root.update_idletasks()
            
            success, result = self.logic.convert_to_epub(file_path, title, author, self.cover_path)
            
            if success:
                self.status_var.set("Conversion Successful!")
                messagebox.showinfo("Success", f"EPUB created:\n{result}")
            else:
                self.status_var.set("Conversion Failed.")
                messagebox.showerror("Error", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()