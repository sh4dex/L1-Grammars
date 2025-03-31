from grammar_input import GrammarInputWindow
from menu import MenuWindow
from tkinter import messagebox
from word_validation import WordValidationDialog
from derivation_generator import DerivationGenerator
from derivation_tree_view import DerivationTreeView
from general_tree_view import GeneralTreeView
import tkinter as tk

class Presenter:
    def __init__(self):
        # Grammar components
        self.terminal_chars = [] #Lista de Caracteres no terminales
        self.non_terminal_chars = [] #Lista de Caracteres Terminales
        self.axiomatic_char = '' #Simbolo axiomatico
        self.production_rules = [] #Producciones formato tupla("x","y") donde X produce Y
        self.word = ""
        
        # Windows
        self.menu_window = None
        self.grammar_input = GrammarInputWindow()
        self.grammar_input.set_submit_callback(self.on_grammar_submit)
    
    #Para vaciar todas las listas
    def reset_grammar(self):
        self.terminal_chars = []
        self.non_terminal_chars = []
        self.axiomatic_char = ''
        self.production_rules = []
    
    '''
    La primera ventana que se muestra es la de introducir la Gramatica.
    Luego la del menu. '''

    def on_grammar_submit(self, terminals, non_terminals, axiomatic, productions):
        if self.validate_grammar(terminals, non_terminals, axiomatic, productions):
            #Cuando se agrega la gramatica 
            self.terminal_chars = terminals
            self.non_terminal_chars = non_terminals
            self.axiomatic_char = axiomatic
            self.production_rules = productions
            self.grammar_input.window.withdraw()
            self.show_menu_window()
    
    
    def show_menu_window(self):
        self.menu_window = MenuWindow()
        self.menu_window.set_callbacks(
            self.on_menu_input_grammar, 
            self.on_menu_check_word,
            self.on_general_tree
        )
        #Aqui en la linea de arriba se deben agregar los eventos para que los otros botones sirvan 
        self.menu_window.update_grammar_display(
            set(self.non_terminal_chars), set(self.terminal_chars), {self.axiomatic_char}, self.production_rules
        )
        self.menu_window.run()
    
    #Cuando se da en volver a Editar la Gramatica, se esconde el panel y se muestra de Nuevo para introducir la gramatica
    def on_menu_input_grammar(self):
        self.reset_grammar()
        self.menu_window.window.withdraw()
        self.grammar_input.window.deiconify()
    

    #validar que la gramtica este bien escrita
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
            # Modified check to allow λ in the right side
            if any(symbol != "λ" and symbol not in terminals and symbol not in non_terminals for symbol in right):
                messagebox.showerror("Error", "El lado derecho de las producciones solo puede contener símbolos válidos o λ.")
                return False
        return True
    
    #muestra la pantalla para validar la palabra
    def show_check_grammar(self):
        self.word_validation_dialog = WordValidationDialog()
        #esto lo manda al la propiedad word (nuestro Atributo)
        self.word_validation_dialog.set_validate_callback(self.on_word_validate)
        self.word_validation_dialog.window.deiconify()
        
    def on_word_validate(self, word):
        self.word = word
        #validamos que la palabra solo contenga caracteres de nuestro lenguaje
        if not all(char in self.terminal_chars + self.non_terminal_chars for char in word):
            messagebox.showerror("Error", "La palabra contiene caracteres no válidos.")
            return False
        #si todo esta bien, ahi si validamos que la palabra este validada por el lenguaje
        is_valid = self.check_word_in_grammar(word)
        messagebox.showinfo("Validación", "La palabra es válida." if is_valid else "La palabra no es válida.")
        self.word_validation_dialog.window.withdraw()
        self.menu_window.window.deiconify()
        return True
    
    def check_word_in_grammar(self, word):
        generator = DerivationGenerator(
            self.terminal_chars,
            self.non_terminal_chars,
            self.production_rules
        )
        
        is_valid = generator.generate(word, self.axiomatic_char)
        
        # Create a new window for the derivation tree regardless of validity
        tree_window = tk.Toplevel()
        tree_window.title("Derivation Tree")
        tree_window.geometry("800x400")
        
        # Create and show the derivation tree
        tree_view = DerivationTreeView(tree_window)
        tree_view.draw_tree(generator.get_derivation_steps())
            
        return is_valid

    # Remove the generate_derivation method as it's now in DerivationGenerator
    def on_menu_check_word(self):
        self.menu_window.window.withdraw()
        self.show_check_grammar()
    
    def run(self): #despliega la ventana para introducir la Gramatica
        self.grammar_input.run()

    def on_general_tree(self):
        tree_view = GeneralTreeView(
            self.terminal_chars,
            self.non_terminal_chars,
            self.production_rules,
            self.axiomatic_char
        )
        tree_view.generate_tree(self.axiomatic_char)
        tree_view.show_tree()

if __name__ == "__main__":
    presenter = Presenter()
    presenter.run()