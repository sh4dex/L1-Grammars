import tkinter as tk
from tkinter import ttk

class DerivationTreeView:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        # Añadir un título descriptivo
        title_label = ttk.Label(
            self.frame, 
            text="Árbol de Derivación", 
            font=("Segoe UI", 14, "bold"),
            bootstyle="primary"
        )
        title_label.pack(pady=(10, 5))
        
        # Añadir instrucciones
        instructions = ttk.Label(
            self.frame,
            text="Se muestra la secuencia de derivaciones aplicando las reglas de producción",
            font=("Segoe UI", 10),
            bootstyle="secondary"
        )
        instructions.pack(pady=(0, 10))
        
        # Mejorar apariencia del canvas
        self.canvas = tk.Canvas(self.frame, bg="#f8f9fa", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configuración del scrolling horizontal
        self.scrollbar = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        
        self.frame.pack(fill="both", expand=True)
        
    def draw_tree(self, derivation_steps):
        """
        Dibuja un árbol de derivación horizontal basado en los pasos de derivación proporcionados.
        
        Args:
            derivation_steps: Lista de tuplas (símbolo_actual, regla_aplicada, resultado)
        """
        self.canvas.delete("all")
        
        if not derivation_steps:
            self.canvas.create_text(50, 50, text="No hay derivación disponible", fill="black", anchor="w")
            return
        
        # Configuración visual
        node_width = 80
        node_height = 40
        level_spacing = 180
        vertical_spacing = 60
        
        # Insertar el axioma inicial como primer elemento
        first_word = derivation_steps[0][0]
        
        # Dibujar el árbol
        x_pos = 50
        y_pos = 50
        
        # Dibujar el nodo inicial (axioma)
        self.canvas.create_rectangle(
            x_pos, y_pos, 
            x_pos + node_width, y_pos + node_height,
            fill="#add8e6", outline="#4682b4", width=2
        )
        
        self.canvas.create_text(
            x_pos + node_width/2, y_pos + node_height/2,
            text=first_word, fill="black", font=("Arial", 12)
        )
        
        prev_x = x_pos
        prev_y = y_pos
        
        # Dibujar el resto del árbol
        for i, (current, rule, result) in enumerate(derivation_steps):
            x_pos = prev_x + level_spacing
            
            # Dibujar nodo resultado
            self.canvas.create_rectangle(
                x_pos, y_pos, 
                x_pos + node_width, y_pos + node_height,
                fill="#add8e6", outline="#4682b4", width=2
            )
            
            self.canvas.create_text(
                x_pos + node_width/2, y_pos + node_height/2,
                text=result, fill="black", font=("Arial", 12)
            )
            
            # Dibujar flecha
            self.canvas.create_line(
                prev_x + node_width, prev_y + node_height/2,
                x_pos, y_pos + node_height/2,
                arrow=tk.LAST, fill="black", width=2
            )
            
            # Mostrar la regla aplicada
            rule_text = f"{rule[0]} → {rule[1]}"
            self.canvas.create_text(
                (prev_x + node_width + x_pos) / 2,
                (prev_y + y_pos + node_height/2) / 2 - 15,
                text=rule_text, fill="#4682b4", font=("Arial", 10)
            )
            
            # Actualizar para el siguiente paso
            prev_x = x_pos
            prev_y = y_pos
        
        # Configurar el área desplazable
        self.canvas.config(scrollregion=self.canvas.bbox("all"))