import os
import customtkinter as ctk
from tkinter import messagebox
from core.constants import FREQUENT_SITES, APPDATA_DB
from core.system import get_hosts_path

class BlockerFrame(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.appdata_db = APPDATA_DB
        self.frequent_sites = FREQUENT_SITES
        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        toolbar = ctk.CTkFrame(self, height=60)
        toolbar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ctk.CTkButton(toolbar, text="⬅ Назад", width=80,
                     command=self.controller.show_explorer).pack(side="left", padx=10)
        
        self.new_site_entry = ctk.CTkEntry(toolbar, 
                                         placeholder_text="сайт.com", 
                                         width=250)
        self.new_site_entry.pack(side="left", padx=10)
        
        ctk.CTkButton(toolbar, text="Блокировать",
                     command=self.add_site_to_hosts).pack(side="left", padx=5)
        
        ctk.CTkButton(toolbar, text="⭐ Частые сайты",
                     fg_color="#34495e",
                     command=self.open_frequent_sites_dialog).pack(side="right", padx=10)
        
        self.sites_list_frame = ctk.CTkScrollableFrame(
            self, 
            label_text="Мои заблокированные сайты"
        )
        self.sites_list_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def add_site_to_hosts(self):
        site = self.new_site_entry.get().strip()
        if not site:
            return
            
        hosts_path = get_hosts_path()
        
        try:
            with open(hosts_path, "a") as f:
                f.write(f"\n127.0.0.1 {site}")
            
            with open(self.appdata_db, "a") as f:
                f.write(site + "\n")
            
            self.new_site_entry.delete(0, "end")
            self.refresh_blocked_list()
            
        except PermissionError:
            messagebox.showerror("Ошибка", 
                               "Требуются права администратора!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def remove_site(self, site):
        hosts_path = get_hosts_path()
        
        try:
            with open(hosts_path, "r") as f:
                lines = f.readlines()
            
            with open(hosts_path, "w") as f:
                for line in lines:
                    if site not in line:
                        f.write(line)
            
            if os.path.exists(self.appdata_db):
                with open(self.appdata_db, "r") as f:
                    sites = f.readlines()
                
                with open(self.appdata_db, "w") as f:
                    for s in sites:
                        if s.strip() != site:
                            f.write(s)
            
            self.refresh_blocked_list()
            
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def refresh_blocked_list(self):
        for widget in self.sites_list_frame.winfo_children():
            widget.destroy()
        
        if os.path.exists(self.appdata_db):
            with open(self.appdata_db, "r") as f:
                for site in f:
                    site = site.strip()
                    if site:
                        self._add_site_to_list(site)

    def _add_site_to_list(self, site):
        row = ctk.CTkFrame(self.sites_list_frame, fg_color="transparent")
        row.pack(fill="x", pady=2)
        
        ctk.CTkLabel(row, text=site).pack(side="left", padx=10)
        
        ctk.CTkButton(row, text="🗑", width=30,
                     fg_color="#c0392b",
                     command=lambda s=site: self.remove_site(s)).pack(side="right")

    def open_frequent_sites_dialog(self):
        dialog = FrequentSitesDialog(self, self.frequent_sites)
        dialog.after(10, dialog.focus_force)
        
    def update_frequent_sites(self, selected_sites):
        """Обновление hosts выбранными сайтами"""
        hosts_path = get_hosts_path()
        
        try:
            with open(hosts_path, "r") as f:
                lines = f.readlines()
            
            new_lines = [
                line for line in lines 
                if not any(site in line for site in self.frequent_sites)
            ]

            with open(self.appdata_db, "a+") as db:
                db.seek(0)
                db_content = db.read()
                
                for site in selected_sites:
                    new_lines.append(f"127.0.0.1 {site}\n")
                    if site not in db_content:
                        db.write(site + "\n")
            
            with open(hosts_path, "w") as f:
                f.writelines(new_lines)
            
            self.refresh_blocked_list()
            messagebox.showinfo("Успех", "Список hosts обновлен!")
            
        except PermissionError:
            messagebox.showerror("Ошибка", 
                               "Запустите от имени администратора!")


class FrequentSitesDialog(ctk.CTkToplevel):
    def __init__(self, parent, frequent_sites):
        super().__init__(parent)
        self.parent = parent
        self.frequent_sites = frequent_sites
        self.title("Быстрая блокировка")
        self.geometry("500x550")
        self.attributes("-topmost", True)
        self.setup_ui()

    def setup_ui(self):
        ctk.CTkLabel(self, 
                    text="Выберите сайты для блокировки",
                    font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        scroll_frame = ctk.CTkScrollableFrame(self)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        hosts_path = get_hosts_path()
        try:
            with open(hosts_path, "r") as f:
                current_hosts = f.read()
        except:
            current_hosts = ""
        
        self.checkboxes = {}
        
        for site, description in self.frequent_sites.items():
            var = ctk.BooleanVar(value=site in current_hosts)
            
            cb = ctk.CTkCheckBox(scroll_frame, text=site, variable=var)
            cb.pack(anchor="w", pady=5, padx=10)
            
            ctk.CTkLabel(scroll_frame, 
                        text=f"   └ {description}",
                        font=ctk.CTkFont(size=11),
                        text_color="gray").pack(anchor="w", padx=25)
            
            self.checkboxes[site] = var
        
        ctk.CTkButton(self, 
                     text="💾 Сохранить изменения",
                     fg_color="#27ae60",
                     command=self.save_selection).pack(pady=15)

    def save_selection(self):
        selected_sites = [
            site for site, var in self.checkboxes.items() 
            if var.get()
        ]
        self.parent.update_frequent_sites(selected_sites)
        self.destroy()