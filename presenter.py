from grammar_input import GrammarInputWindow
from menu import MenuWindow
from tkinter import messagebox
import tkinter as tk
from word_validation import WordValidationDialog
from DerivationTreeView import DerivationTreeView
from DerivationGenerator import DerivationGenerator

class Presenter:
    def __init__(self):
        # Grammar components
        self.terminal_chars = []
        self.non_terminal_chars = []
        self.axiomatic_char = ''
        self.production_rules = []
        self.word = ""
        
        # Windows
        self.menu_window = None
        self.grammar_input = GrammarInputWindow()
        self.grammar_input.set_submit_callback(self.on_grammar_submit)
        
    def reset_grammar(self):
        self.terminal_chars = []
        self.non_terminal_chars = []
        self.axiomatic_char = ''
        self.production_rules = []
        
    def on_grammar_submit(self, terminals, non_terminals, axiomatic, productions):
        if self.validate_grammar(terminals, non_terminals, axiomatic, productions):
            self.terminal_chars = terminals
            self.non_terminal_chars = non_terminals
            self.axiomatic_char = axiomatic
            self.production_rules = productions
            
            self.grammar_input.window.withdraw()
            self.show_menu_window()
            
    def show_menu_window(self):
        self.menu_window = MenuWindow()
        self.menu_window.set_callbacks(self.on_menu_input_grammar, self.on_menu_check_word, self.show_derivation_tree)
        
        self.menu_window.update_grammar_display(
            set(self.non_terminal_chars), set(self.terminal_chars), {self.axiomatic_char}, self.production_rules
        )
        self.menu_window.run()
        
    def on_menu_input_grammar(self):
        self.reset_grammar()
        self.menu_window.window.withdraw()
        self.grammar_input.window.deiconify()
        
    def validate_grammar(self, terminals, non_terminals, axiomatic, productions):
        if not terminals:
            messagebox.showerror("Error", "Debe agregar al menos un símbolo terminal.")
            return False
        if not non_terminals:
            messagebox.showerror("Error", "Debe agregar al menos un símbolo no terminal.")
            return False 
        if not axiomatic:
            messagebox.showerror("Error", "Debe establecer un símbolo axiomático.")
            return False
        if set(terminals) & set(non_terminals):
            messagebox.showerror("Error", "Símbolos terminales y no terminales deben ser disjuntos.")
            return False
        if axiomatic not in non_terminals:
            messagebox.showerror("Error", "El símbolo axiomático debe ser un no terminal.")
            return False
        for left, right in productions:
            if left not in non_terminals:
                messagebox.showerror("Error", "El lado izquierdo de cada producción debe ser un símbolo no terminal.")
                return False
            if any(symbol not in terminals and symbol not in non_terminals for symbol in right):
                messagebox.showerror("Error", "El lado derecho de las producciones solo puede contener símbolos válidos.")
                return False
        return True
        
    def show_check_grammar(self):
        self.word_validation_dialog = WordValidationDialog()
        self.word_validation_dialog.set_validate_callback(self.on_word_validate)
        self.word_validation_dialog.window.deiconify()
        
    def on_word_validate(self, word):
        self.word = word
        if not all(char in self.terminal_chars for char in word):
            messagebox.showerror("Error", "La palabra contiene caracteres no válidos.")
            return False
        
        is_valid = self.check_word_in_grammar(word)
        messagebox.showinfo("Validación", "La palabra es válida." if is_valid else "La palabra no es válida.")
        self.word_validation_dialog.window.withdraw()
        self.menu_window.window.deiconify()
        return True
    
    def check_word_in_grammar(self, word):
        generator = DerivationGenerator(
            self.terminal_chars,
            self.non_terminal_chars,
            self.axiomatic_char,
            self.production_rules
        )
        
        self.derivation_steps = generator.generate_derivation(word)
        return self.derivation_steps is not None
    
    def on_menu_check_word(self):
        self.menu_window.window.withdraw()
        self.show_check_grammar()
    
    def show_derivation_tree(self):
        if not hasattr(self, 'word') or not self.word:
            messagebox.showerror("Error", "Primero debe validar una palabra.")
            return
            
        if not hasattr(self, 'derivation_steps') or not self.derivation_steps:
            messagebox.showerror("Error", "No se ha encontrado una derivación para esta palabra.")
            return
            
        tree_window = tk.Toplevel()
        tree_window.title(f"Árbol de Derivación para '{self.word}'")
        tree_window.geometry("800x500")
        
        tree_view = DerivationTreeView(tree_window)
        tree_view.draw_tree(self.derivation_steps)
    
    def run(self):
        self.grammar_input.run()

if __name__ == "__main__":
    presenter = Presenter()
    presenter.run()