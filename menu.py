import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from grammar_input import GrammarInputWindow

class MenuWindow:
    def __init__(self):
        self.window = ttk.Window(themename="darkly")
        self.window.title("Grammar Tree Generator")
        self.window.geometry("800x600")
        
        # Initialize UI components
        self.input_grammar_btn = None
        self.check_word_btn = None
        self.general_tree_btn = None
        self.particular_tree_btn = None
        self.v_label = None
        self.sigma_label = None
        self.s_label = None
        self.p_label = None
        self.productions_text = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create single button frame for all buttons
        button_frame = ttk.Frame(self.window, padding=20)
        button_frame.pack(fill="x")
        
        # Create all buttons in a single row
        self.input_grammar_btn = ttk.Button(button_frame, text="Edit Grammar", style="primary", command=self.on_input_grammar)
        self.input_grammar_btn.pack(side="left", padx=5)
        
        self.check_word_btn = ttk.Button(button_frame, text="Comprobar palabra", style="info", command=self.on_check_word)
        self.check_word_btn.pack(side="left", padx=5)
        
        self.general_tree_btn = ttk.Button(button_frame, text="Árbol derivación general", 
                                         style="success", command=self.on_general_tree)
        self.general_tree_btn.pack(side="left", padx=5)
        
        self.particular_tree_btn = ttk.Button(button_frame, text="Árbol derivación particular", style="success")
        self.particular_tree_btn.pack(side="left", padx=5)
        
        # Grammar display frame
        self.grammar_frame = ttk.LabelFrame(self.window, text="Current Grammar", padding=20)
        self.grammar_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.v_label = ttk.Label(self.grammar_frame, text="V = { }")
        self.v_label.pack(anchor="w", pady=5)
        
        self.sigma_label = ttk.Label(self.grammar_frame, text="Σ = { }")
        self.sigma_label.pack(anchor="w", pady=5)
        
        self.s_label = ttk.Label(self.grammar_frame, text="S = { }")
        self.s_label.pack(anchor="w", pady=5)
        
        self.p_label = ttk.Label(self.grammar_frame, text="Productions:")
        self.p_label.pack(anchor="w", pady=5)
        
        self.productions_text = tk.Text(self.grammar_frame, height=5, width=40)
        self.productions_text.pack(fill="both", expand=True)

    def on_input_grammar(self):
        if hasattr(self, 'input_callback'):
            self.input_callback()
            
    def on_check_word(self):
        if hasattr(self, 'check_callback'):
            self.check_callback()
            
    def set_callbacks(self, input_cb, check_cb, general_tree_cb):
        self.input_callback = input_cb
        self.check_callback = check_cb
        self.general_tree_callback = general_tree_cb
        
    def update_grammar_display(self, v_set, sigma_set, s_symbol, productions):
        self.v_label.config(text=f"V = {v_set}")
        self.sigma_label.config(text=f"Σ = {sigma_set}")
        self.s_label.config(text=f"S = {s_symbol}")
        
        self.productions_text.delete(1.0, tk.END)
        for left, right in productions:
            self.productions_text.insert(tk.END, f"{left} → {right}\n")
            
    def run(self):
        self.window.mainloop()

    def on_general_tree(self):
        if hasattr(self, 'general_tree_callback'):
            self.general_tree_callback()

