from grammar_input import GrammarInputWindow
from menu import MenuWindow
from tkinter import messagebox
from word_validation import WordValidationDialog

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
        #Se vinculan los eventos:
        self.menu_window.set_callbacks(self.on_menu_input_grammar, self.on_menu_check_word)
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
            if any(symbol not in terminals and symbol not in non_terminals for symbol in right):
                messagebox.showerror("Error", "El lado derecho de las producciones solo puede contener símbolos válidos.")
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
        #entonces tenemos la palabra a Validar (word)
        #y lo que tenemos generado es el axiomatico 
        return self.generate_derivation(word, self.axiomatic_char)
    
    #TODO: Explicar cuando llegue a casa
    def generate_derivation(self, target, current, depth=0, steps=None):
        if steps is None:
            steps = [current]
            
        if depth > 100:
            return False
            
        current = current.replace("λ", "")
            
        if current == target:
            if any(char in self.non_terminal_chars for char in current):
                return False
            print("\nDerivation steps:")
            for i, step in enumerate(steps):
                print(f"{i+1}. {step}")
            return True
            
        if len(current) > len(target) * 2:
            return False
            
        for left, right in self.production_rules:
            if left in current:
                new_right = "" if right == "λ" else right
                new_current = current.replace(left, new_right, 1)
                steps.append(new_current)
                if self.generate_derivation(target, new_current, depth + 1, steps):
                    return True
                steps.pop()
        return False

    def on_menu_check_word(self):
        self.menu_window.window.withdraw()
        self.show_check_grammar()
    
    def run(self): #despliega la ventana para introducir la Gramatica
        self.grammar_input.run()

if __name__ == "__main__":
    presenter = Presenter()
    presenter.run()