class DerivationGenerator:
    def __init__(self, terminal_chars, non_terminal_chars, production_rules):
        self.terminal_chars = terminal_chars
        self.non_terminal_chars = non_terminal_chars
        self.production_rules = production_rules
        self.derivation_steps = []

    '''
    Este es el metodo importante que recorre la palabra que se le ingresa y valida si se tienen lambdas
    en la producción, si es asi, se reemplaza por una cadena vacia, si no, se reemplaza por la producción
    de la derecha, si no se encuentra la producción en la izquierda, se retorna False, si se encuentra
    la producción en la izquierda, se reemplaza por la producción de la derecha, si la producción de la
    '''
    def generate(self, target, current, depth=0):
        if depth > 100:
            return False
            
        current = current.replace("λ", "")
            
        if current == target:
            if any(char in self.non_terminal_chars for char in current):
                return False
            return True
            
        if len(current) > len(target) * 2:
            return False
            
        for left, right in self.production_rules:
            if left in current:
                new_right = "" if right == "λ" else right
                new_current = current.replace(left, new_right, 1)
                # Se guarda el paso de la derivación en una lista para luego mostrarlos en el arbol de derivación
                self.derivation_steps.append((current, (left, right), new_current))
                if self.generate(target, new_current, depth + 1):
                    return True
                self.derivation_steps.pop()
        return False

    def get_derivation_steps(self):
        return self.derivation_steps