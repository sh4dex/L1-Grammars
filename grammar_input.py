import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

class GrammarInputWindow:
    def __init__(self):
        self.window = ttk.Window(themename="darkly")
        self.window.title("Grammar Input")
        self.window.geometry("900x700")
        
        self.style = ttk.Style()
        self.style.configure("Custom.TEntry", padding=10, relief="flat")
        self.style.configure("AddField.TButton", padding=8, background="#28a745")
        self.style.configure("Delete.TButton", padding=6, background="#dc3545")
        
        self.terminal_entries = []
        self.non_terminal_entries = []
        self.production_entries = []
        
        self.setup_ui()
    
    #configuracion de la Interfaz
    def setup_ui(self):
        container = ttk.Frame(self.window)
        container.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Non-terminal symbols section
        non_terminal_frame = ttk.LabelFrame(self.scrollable_frame, text="Non-Terminal Symbols", padding=15)
        non_terminal_frame.pack(fill="x", pady=10, padx=10)
        
        add_btn = ttk.Button(non_terminal_frame, text="Add Non-Terminal Symbol", style="AddField.TButton",
                            command=lambda: self.add_non_terminal_entry(non_terminal_frame))
        add_btn.pack(anchor="w", padx=5, pady=5)
        self.add_non_terminal_entry(non_terminal_frame)
        
        # Terminal symbols section
        terminal_frame = ttk.LabelFrame(self.scrollable_frame, text="Terminal Symbols", padding=15)
        terminal_frame.pack(fill="x", pady=10, padx=10)
        
        add_btn = ttk.Button(terminal_frame, text="Add Terminal Symbol", style="AddField.TButton",
                            command=lambda: self.add_terminal_entry(terminal_frame))
        add_btn.pack(anchor="w", padx=5, pady=5)
        self.add_terminal_entry(terminal_frame)
        
        # Axiomatic symbol section
        axiomatic_frame = ttk.LabelFrame(self.scrollable_frame, text="Axiomatic Symbol", padding=15)
        axiomatic_frame.pack(fill="x", pady=10, padx=10)
        
        self.axiomatic_entry = ttk.Entry(axiomatic_frame, style="Custom.TEntry")
        self.axiomatic_entry.configure(validate="key", validatecommand=(self.axiomatic_entry.register(self.validate_single_char), '%P'))
        self.axiomatic_entry.pack(fill="x", padx=5, pady=5)
        
        # Productions section
        productions_frame = ttk.LabelFrame(self.scrollable_frame, text="Productions", padding=15)
        productions_frame.pack(fill="x", pady=10, padx=10)
        
        add_btn = ttk.Button(productions_frame, text="Add New Production", style="AddField.TButton",
                            command=lambda: self.add_production_entry(productions_frame))
        add_btn.pack(anchor="w", padx=5, pady=5)
        self.add_production_entry(productions_frame)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=5)
        scrollbar.pack(side="right", fill="y")
        
        # Add Grammar Button
        submit_frame = ttk.Frame(self.scrollable_frame)
        submit_frame.pack(fill="x", pady=20, padx=10)
        
        self.submit_btn = ttk.Button(submit_frame, text="Add Grammar", style="success", width=20, command=self.on_submit)
        self.submit_btn.pack(side="right")
        
        # Bind mouse wheel
        self.scrollable_frame.bind('<Enter>', lambda e: self._bound_to_mousewheel(e, canvas))
        self.scrollable_frame.bind('<Leave>', lambda e: self._unbound_to_mousewheel(e, canvas))

    #eSta fucnion en el Presente la llama 
    def on_submit(self):
        if hasattr(self, 'submit_callback'):
            terminal_symbols = [entry.winfo_children()[0].get() for entry in self.terminal_entries]
            non_terminal_symbols = [entry.winfo_children()[0].get() for entry in self.non_terminal_entries]
            axiomatic = self.axiomatic_entry.get()
            
            # Get productions as tuples (left_side, right_side)
            productions = []
            for entry_frame in self.production_entries:         #Una produccion tiene ("s","->","Aa")
                left = entry_frame.winfo_children()[0].get()  # Left side entry
                right = entry_frame.winfo_children()[2].get() # Right side entry (index 2 because of arrow label)
                if left and right:  # No vacio
                    productions.append((left, right))
            
            self.submit_callback(terminal_symbols, non_terminal_symbols, axiomatic, productions)

    def set_submit_callback(self, callback):
        self.submit_callback = callback

    def validate_single_char(self, P): #
        return len(P) <= 1

    #Scrollbar 
    def _bound_to_mousewheel(self, event, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, canvas))

    def _unbound_to_mousewheel(self, event, canvas):
        canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event, canvas):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_non_terminal_entry(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        
        entry = ttk.Entry(frame, style="Custom.TEntry")
        entry.configure(validate="key", validatecommand=(entry.register(self.validate_single_char), '%P'))
        entry.pack(side="left", fill="x", expand=True, padx=5)
        
        delete_btn = ttk.Button(frame, text="Delete", style="Delete.TButton",
                            command=lambda: self.delete_entry(frame, self.non_terminal_entries))
        delete_btn.pack(side="right", padx=5)
        
        self.non_terminal_entries.append(frame)

    def add_terminal_entry(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        
        entry = ttk.Entry(frame, style="Custom.TEntry")
        entry.configure(validate="key", validatecommand=(entry.register(self.validate_single_char), '%P'))
        entry.pack(side="left", fill="x", expand=True, padx=5)
        
        delete_btn = ttk.Button(frame, text="Delete", style="Delete.TButton",
                            command=lambda: self.delete_entry(frame, self.terminal_entries))
        delete_btn.pack(side="right", padx=5)
        
        self.terminal_entries.append(frame)

    def add_production_entry(self, parent):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", pady=5)
        
        # Left side entry (non-terminal)
        left_entry = ttk.Entry(frame, style="Custom.TEntry", width=10)
        left_entry.configure(validate="key", validatecommand=(left_entry.register(self.validate_single_char), '%P'))
        left_entry.pack(side="left", padx=5)
        
        # Arrow label
        arrow_label = ttk.Label(frame, text="→", font=("Arial", 12))
        arrow_label.pack(side="left", padx=10)
        
        # Right side entry (production)
        right_entry = ttk.Entry(frame, style="Custom.TEntry", width=30)
        right_entry.pack(side="left", padx=5)
        
        # Lambda button
        lambda_btn = ttk.Button(frame, text="λ", 
                              command=lambda: right_entry.insert(tk.END, "λ"))
        lambda_btn.pack(side="right", padx=2)
        
        delete_btn = ttk.Button(frame, text="Delete", style="Delete.TButton",
                            command=lambda: self.delete_entry(frame, self.production_entries))
        delete_btn.pack(side="right", padx=5)
        
        self.production_entries.append(frame)

    def on_submit(self):
        if hasattr(self, 'submit_callback'):
            terminal_symbols = [entry.winfo_children()[0].get() for entry in self.terminal_entries]
            non_terminal_symbols = [entry.winfo_children()[0].get() for entry in self.non_terminal_entries]
            axiomatic = self.axiomatic_entry.get()
            
            # Get productions as tuples (left_side, right_side)
            productions = []
            for entry_frame in self.production_entries:
                left = entry_frame.winfo_children()[0].get()  # Left side entry
                right = entry_frame.winfo_children()[2].get() # Right side entry (index 2 because of arrow label)
                if left and right:  # Only add if both sides have content
                    productions.append((left, right))
            
            self.submit_callback(terminal_symbols, non_terminal_symbols, axiomatic, productions)

    def delete_entry(self, frame, entry_list):
        if len(entry_list) > 1:
            frame.destroy()
            entry_list.remove(frame)
            
    def run(self):
        self.window.mainloop()