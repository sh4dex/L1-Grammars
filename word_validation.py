import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox

class WordValidationDialog:
    def __init__(self):
        self.window = ttk.Window(themename="darkly")
        self.window.title("Grammar Tree Generator")
        self.window.geometry("200x200")
        
        # Initialize UI components
        self.word_entry = None
        self.result = None
        self.validate_callback = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create and place widgets
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Label(main_frame, text="Enter word to validate:").pack(pady=(0, 10))
        
        self.word_entry = ttk.Entry(main_frame)
        self.word_entry.pack(fill="x", pady=(0, 20))
        
        # Validate command to prevent spaces
        vcmd = (self.window.register(self._validate_input), '%P')
        self.word_entry.configure(validate='key', validatecommand=vcmd)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="Cancel", style="danger", command=self._on_cancel).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Validate", style="primary", command=self._on_validate).pack(side="right", padx=5)
        
        # Set focus to entry
        self.word_entry.focus_set()

    def _validate_input(self, value):
        return ' ' not in value
        
    def _on_validate(self):
        word = self.word_entry.get()
        if not word:
            messagebox.showerror("Error", "Input cannot be empty!")
            return
            
        if self.validate_callback and self.validate_callback(word):
            self.result = word
            self.window.withdraw()
        
    def _on_cancel(self):
        self.window.withdraw()

    def get_result(self):
        return self.result
    def set_validate_callback(self, callback):
            self.validate_callback = callback
