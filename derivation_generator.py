class DerivationGenerator:
    def __init__(self, terminal_chars, non_terminal_chars, production_rules):
        self.terminal_chars = terminal_chars
        self.non_terminal_chars = non_terminal_chars
        self.production_rules = production_rules
        self.derivation_steps = []

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
                # Store the derivation step
                self.derivation_steps.append((current, (left, right), new_current))
                if self.generate(target, new_current, depth + 1):
                    return True
                self.derivation_steps.pop()
        return False

    def get_derivation_steps(self):
        return self.derivation_steps