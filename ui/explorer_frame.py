import os
import shutil
import customtkinter as ctk
from tkinter import messagebox
from core.constants import DEFAULT_PATH
from core.utils import format_timestamp
from core.system import is_admin, run_as_admin
from widgets.context_menu import ContextMenu

class ExplorerFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.current_path = DEFAULT_PATH
        self.selected_path = ""
        self.selected_button = None
        self.context_menu = ContextMenu(self, self)
        self.setup_ui()
        self.load_path(self.current_path)

    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(sidebar, text="SAFE\nEXPLORER", 
                    font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        
        ctk.CTkButton(sidebar, text="⬅ Назад", 
                     command=self.go_back).pack(pady=5, padx=10)
        
        admin_c = "#2980b9" if not is_admin() else "#27ae60"
        ctk.CTkButton(sidebar, text="🛡 Админ-права", 
                     fg_color=admin_c, command=run_as_admin).pack(pady=10, padx=10)
        
        ctk.CTkButton(sidebar, 
                     text="🔄 AnyDesk", 
                     fg_color="#8e44ad",
                     command=self.restart_anydesk).pack(pady=5, padx=10)
        
        ctk.CTkButton(sidebar, text="🚫 Блок-Сайтов", 
                     fg_color="#e67e22", 
                     command=self.controller.show_blocker).pack(side="bottom", pady=20, padx=10)
        
        main = ctk.CTkFrame(self, fg_color="#1a1a1a")
        main.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.path_entry = ctk.CTkEntry(main)
        self.path_entry.pack(fill="x", padx=10, pady=10)
        
        self.files_scroll = ctk.CTkScrollableFrame(main, fg_color="transparent")
        self.files_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        self.files_scroll._parent_canvas.bind("<Button-3>", 
                                            lambda e: self.context_menu.show(e))
        
        prop = ctk.CTkFrame(self, width=220)
        prop.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        ctk.CTkLabel(prop, text="Свойства").pack(pady=10)
        
        self.date_ent = ctk.CTkEntry(prop)
        self.date_ent.pack(pady=5, padx=10)
        
        ctk.CTkButton(prop, text="Применить дату", 
                     fg_color="#27ae60", 
                     command=self.apply_new_date).pack(pady=10)
        
        ctk.CTkButton(prop, text="Удалить", 
                     fg_color="#c0392b", 
                     command=self.delete_item).pack(pady=5)

    def load_path(self, path):
        if not os.path.isdir(path):
            return
            
        self.current_path = path
        self.selected_path = ""
        self.selected_button = None
        self.path_entry.delete(0, "end")
        self.path_entry.insert(0, path)
        
        for w in self.files_scroll.winfo_children():
            w.destroy()
        
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                is_dir = os.path.isdir(item_path)
                
                btn = ctk.CTkButton(
                    self.files_scroll,
                    text=f"{'📁' if is_dir else '📄'} {item}",
                    anchor="w",
                    fg_color="transparent"
                )
                btn.pack(fill="x", padx=2, pady=1)
                
                btn.bind("<Button-1>", 
                        lambda e, p=item_path, b=btn: self.select_item(p, b))
                btn.bind("<Button-3>", 
                       lambda e, p=item_path: self.context_menu.show(e))
                
                if is_dir:
                    btn.bind("<Double-Button-1>", 
                           lambda e, p=item_path: self.load_path(p))
                else:
                    btn.bind("<Double-Button-1>", 
                           lambda e, p=item_path: self.controller.show_editor(p))
        except PermissionError:
            pass

    def select_item(self, path, button):
        if self.selected_button:
            self.selected_button.configure(fg_color="transparent")
        
        self.selected_path = path
        self.selected_button = button
        self.selected_button.configure(fg_color="#3a3a3a")
        
        try:
            mtime = os.path.getmtime(path)
            self.date_ent.delete(0, "end")
            self.date_ent.insert(0, format_timestamp(mtime))
        except:
            pass

    def apply_new_date(self):
        from core.utils import parse_datetime_str
        
        if not self.selected_path:
            return
            
        new_time = parse_datetime_str(self.date_ent.get())
        if new_time:
            try:
                os.utime(self.selected_path, (new_time, new_time))
            except:
                pass

    def go_back(self):
        parent_dir = os.path.dirname(self.current_path)
        if os.path.exists(parent_dir):
            self.load_path(parent_dir)

    def refresh_view(self):
        self.load_path(self.current_path)

    def delete_item(self):
        if not self.selected_path:
            return
            
        if messagebox.askyesno("Удалить?", 
                              os.path.basename(self.selected_path)):
            try:
                if os.path.isdir(self.selected_path):
                    shutil.rmtree(self.selected_path)
                else:
                    os.remove(self.selected_path)
                self.refresh_view()
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def create_file(self):
        base = self.selected_path if self.selected_path and os.path.isdir(self.selected_path) else self.current_path
        open(os.path.join(base, "new_file.txt"), "w").close()
        self.refresh_view()

    def create_folder(self):
        base = self.selected_path if self.selected_path and os.path.isdir(self.selected_path) else self.current_path
        os.makedirs(os.path.join(base, "Новая папка"), exist_ok=True)
        self.refresh_view()

    def restart_anydesk(self):
        from core.system import restart_anydesk as restart_ad
        
        success, message = restart_ad()
        
        if success:
            messagebox.showinfo("Успех", message)
        else:
            messagebox.showerror("Ошибка", message)