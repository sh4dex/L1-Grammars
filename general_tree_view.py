import matplotlib.pyplot as plt
import networkx as nx

class GeneralTreeView:
    def __init__(self, terminal_chars, non_terminal_chars, production_rules, axiomatic):
        self.terminal_chars = terminal_chars
        self.non_terminal_chars = non_terminal_chars
        self.production_rules = production_rules
        self.axiomatic = axiomatic
        self.G = nx.DiGraph()
        self.pos = None
        self.node_count = 0
        
    def generate_tree(self, current, depth=0, parent=None):
        if depth >= 6:  # Maximum depth limit
            return
            
        node_id = f"{current}_{self.node_count}"
        self.node_count += 1
        self.G.add_node(node_id, label=current)
        
        if parent is not None:
            self.G.add_edge(parent, node_id)
            
        # Only continue if the current string contains non-terminals
        if any(nt in current for nt in self.non_terminal_chars):
            for left, right in self.production_rules:
                if left in current:
                    # Generate one child for each possible production
                    new_string = current.replace(left, right, 1)
                    self.generate_tree(new_string, depth + 1, node_id)
    
    def show_tree(self):
        if not self.G.nodes():
            return
            
        plt.figure(figsize=(12, 8))
        self.pos = nx.spring_layout(self.G, k=1, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.G, self.pos, 
                             node_color='lightblue',
                             node_size=2000,
                             alpha=0.7)
        
        # Draw edges
        nx.draw_networkx_edges(self.G, self.pos, 
                             edge_color='gray',
                             arrows=True,
                             arrowsize=20)
        
        # Draw labels
        labels = nx.get_node_attributes(self.G, 'label')
        nx.draw_networkx_labels(self.G, self.pos, labels,
                              font_size=10,
                              font_weight='bold')
        
        plt.title("General Derivation Tree (up to depth 5)")
        plt.axis('off')
        plt.show()