import os
import sys
import customtkinter as ctk
from core.utils import fix_keyboard_bindings
from ui.explorer_frame import ExplorerFrame
from ui.editor_frame import EditorFrame
from ui.blocker_frame import BlockerFrame

class SafeExplorer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SelfExlporer Free")
        self.geometry("1200x750")
        
        fix_keyboard_bindings(self)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.explorer_frame = ExplorerFrame(self, controller=self)
        self.editor_frame = EditorFrame(self, controller=self)
        self.blocker_frame = BlockerFrame(self, controller=self)
        
        self.show_explorer()
        
    def show_explorer(self):
        self.editor_frame.grid_forget()
        self.blocker_frame.grid_forget()
        self.explorer_frame.grid(row=0, column=0, sticky="nsew")
        
    def show_editor(self):
        self.explorer_frame.grid_forget()
        self.blocker_frame.grid_forget()
        self.editor_frame.grid(row=0, column=0, sticky="nsew")
        
    def show_blocker(self):
        self.explorer_frame.grid_forget()
        self.editor_frame.grid_forget()
        self.blocker_frame.grid(row=0, column=0, sticky="nsew")