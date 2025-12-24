import os
import customtkinter as ctk
from tkinter import messagebox

class EditorFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.editing_file_path = None
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Панель инструментов
        toolbar = ctk.CTkFrame(self, height=50)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ctk.CTkButton(toolbar, text="⬅ Выйти", 
                     command=self.controller.show_explorer).pack(side="left", padx=5)
        
        self.text_edit = ctk.CTkTextbox(self, font=("Consolas", 15), undo=True)
        self.text_edit.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkButton(toolbar, text="💾 Сохранить", 
                     fg_color="#27ae60", 
                     command=self.save_file).pack(side="right", padx=10)

    def open_file(self, file_path):
        self.editing_file_path = file_path
        self.text_edit.delete("1.0", "end")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.text_edit.insert("1.0", content)
        except:
            self.text_edit.insert("1.0", "[Бинарный файл или ошибка чтения]")

    def save_file(self):
        if not self.editing_file_path:
            return
            
        original_mtime = os.path.getmtime(self.editing_file_path)
        
        try:
            with open(self.editing_file_path, "w", encoding="utf-8") as f:
                f.write(self.text_edit.get("1.0", "end-1c"))
            
            if messagebox.askyesno("Сохранить дату", "Заморозить дату изменения файла?"):
                os.utime(self.editing_file_path, (original_mtime, original_mtime))
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")