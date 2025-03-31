import tkinter as tk
from tkinter import ttk

class GeneralTreeView:
    def __init__(self, terminal_chars, non_terminal_chars, production_rules, axiomatic):
        self.terminal_chars = terminal_chars
        self.non_terminal_chars = non_terminal_chars
        self.production_rules = production_rules
        self.axiomatic = axiomatic
        
        # Create window and canvas
        self.window = tk.Toplevel()
        self.window.title("Árbol de Derivación General")
        self.window.geometry("1200x900")  # Increased window size
        
        # Añadir cabecera informativa
        header = ttk.Frame(self.window, padding=10)
        header.pack(fill="x")
        
        title = ttk.Label(
            header,
            text="Árbol de Derivación General",
            font=("Segoe UI", 16, "bold"),
            bootstyle="primary"
        )
        title.pack(pady=(5, 0))
        
        grammar_info = ttk.Label(
            header,
            text=f"Axioma: {axiomatic} | No terminales: {', '.join(non_terminal_chars)} | Terminales: {', '.join(terminal_chars)}",
            font=("Segoe UI", 9),
            bootstyle="secondary" 
        )
        grammar_info.pack(pady=(0, 10))
        
        self.frame = ttk.Frame(self.window)
        self.canvas = tk.Canvas(self.frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add scrollbars
        self.v_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.h_scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)
        
        self.frame.pack(fill="both", expand=True)
        
        # Tree drawing parameters - increased spacing
        self.node_width = 80  # Larger nodes
        self.node_height = 50
        self.vertical_spacing = 120  # More vertical space
        self.horizontal_spacing = 160  # More horizontal space
        self.nodes = {}  # Store node positions
        
    def generate_tree(self, current, x=None, y=None, level=0, parent_pos=None):
        if level >= 6:  # Maximum depth limit
            return
            
        if x is None:  # Root node
            x = 600  # Start from middle with more space
            y = 80
            
        # Draw current node
        node_id = self.draw_node(current, x, y)
        self.nodes[current + str(level)] = (x, y)  # Added level to key to avoid duplicates
        
        # Draw connection to parent
        if parent_pos:
            self.draw_arrow(parent_pos[0], parent_pos[1], x, y)
        
        # Calculate children positions and generate subtrees
        children = []
        for left, right in self.production_rules:
            if left in current:
                new_string = current.replace(left, right, 1)
                children.append(new_string)
        
        if children:
            # Increase width based on number of children and level
            width_multiplier = max(1, level * 0.5 + 1)  # Wider spacing for deeper levels
            width = len(children) * self.horizontal_spacing * width_multiplier
            start_x = x - width/2 + (self.horizontal_spacing * width_multiplier)/2
            
            for i, child in enumerate(children):
                child_x = start_x + i * (self.horizontal_spacing * width_multiplier)
                child_y = y + self.vertical_spacing
                self.generate_tree(child, child_x, child_y, level + 1, (x, y))
    
    def draw_node(self, text, x, y):
        # Draw node with better styling
        radius = self.node_width/2
        
        # Determinar color basado en si contiene símbolos no terminales
        contains_non_terminal = any(char in self.non_terminal_chars for char in text)
        fill_color = "#e3f2fd" if contains_non_terminal else "#f1f8e9"
        outline_color = "#1976d2" if contains_non_terminal else "#689f38"
        
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=fill_color, outline=outline_color, width=2
        )
        # Draw text
        self.canvas.create_text(
            x, y, text=text,
            font=("Arial", 12, "bold"),
            fill="#212121"
        )
        return (x, y)
    
    def draw_arrow(self, x1, y1, x2, y2):
        # Draw line with arrow
        self.canvas.create_line(
            x1, y1 + self.node_height/2,
            x2, y2 - self.node_height/2,
            arrow=tk.LAST, width=2
        )
    
    def show_tree(self):
        self.generate_tree(self.axiomatic)
        # Update scroll region to include all objects
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        # Center the view
        self.canvas.xview_moveto(0.5)
        self.canvas.yview_moveto(0)