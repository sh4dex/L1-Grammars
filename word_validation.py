import tkinter as tk
from tkinter import ttk

class WordValidationDialog:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Word Validation")
        self.window.geometry("400x200")
        self.window.configure(bg="#f0f0f0")
        
        # Centrar la ventana
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Enter a word to validate", font=("Arial", 12))
        title_label.pack(pady=10)
        
        # Word entry
        self.word_entry = ttk.Entry(main_frame, width=30)
        self.word_entry.pack(pady=10, fill="x")
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)
        
        self.validate_btn = ttk.Button(button_frame, text="Validate", command=self.on_validate)
        self.validate_btn.pack(side="right", padx=5)
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.window.withdraw)
        self.cancel_btn.pack(side="right", padx=5)
        
    def on_validate(self):
        word = self.word_entry.get().strip()
        if hasattr(self, 'validate_callback'):
            if self.validate_callback(word):
                self.word_entry.delete(0, tk.END)
                
    def set_validate_callback(self, callback):
        self.validate_callback = callback