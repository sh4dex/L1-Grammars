class DerivationGenerator:
    def __init__(self, terminals, non_terminals, axiom, productions):
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.axiom = axiom
        self.productions = productions
        # Convertir las producciones a un diccionario para acceso más rápido
        self.production_map = {}
        for left, right in productions:
            if left not in self.production_map:
                self.production_map[left] = []
            self.production_map[left].append(right)
    
    def generate_derivation(self, target_word):
        """
        Genera una lista de pasos de derivación para la palabra objetivo
        
        Args:
            target_word: La palabra que se quiere derivar
            
        Returns:
            Lista de tuplas (símbolo_actual, regla_aplicada, resultado) o None si no hay derivación
        """
        # Usaremos BFS para encontrar una derivación
        queue = [(self.axiom, [])]
        visited = set([self.axiom])
        
        while queue:
            current, steps = queue.pop(0)
            
            # Verificar si ya alcanzamos la palabra objetivo
            if current == target_word:
                return steps
            
            # Si la cadena actual tiene solo terminales, y no es la objetivo, no se puede derivar
            if all(s in self.terminals for s in current):
                continue
                
            # Probar todas las posibles derivaciones
            for i, symbol in enumerate(current):
                if symbol in self.non_terminals and symbol in self.production_map:
                    for production in self.production_map[symbol]:
                        # Aplicar la producción
                        new_string = current[:i] + production + current[i+1:]
                        
                        if new_string not in visited:
                            visited.add(new_string)
                            new_steps = steps + [(current, (symbol, production), new_string)]
                            queue.append((new_string, new_steps))
        
        return None  # No se encontró derivación