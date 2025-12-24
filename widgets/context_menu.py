import customtkinter as ctk
from tkinter import Menu

class ContextMenu:
    def __init__(self, parent, explorer_frame):
        self.parent = parent
        self.explorer_frame = explorer_frame
        
        self.menu = Menu(
            parent, 
            tearoff=0, 
            bg="#2b2b2b", 
            fg="white", 
            borderwidth=0
        )
        self.menu.add_command(
            label="➕ Создать файл", 
            command=explorer_frame.create_file
        )
        self.menu.add_command(
            label="📂 Создать папку", 
            command=explorer_frame.create_folder
        )

    def show(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()