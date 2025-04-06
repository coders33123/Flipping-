#<<[graph_core.py:GraphManager]>>
import networkx as nx
from typing import List, Dict

class GraphManager:
    def __init__(self):
        self.graph = nx.Graph()

    def add_word(self, word: str, relationships: List[str], encoded_vector: List[int]):
        """
        Adds a word to the graph with contextual vector and relationships.
        """
        self.graph.add_node(word, encoded=encoded_vector)
        for related_word in relationships:
            self.graph.add_edge(word, related_word)
    
    def visualize(self):
        import matplotlib.pyplot as plt
        nx.draw(self.graph, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold")
        plt.show()

    def get_neighbors(self, word: str) -> List[str]:
        return list(self.graph.neighbors(word)) if word in self.graph else []
#<<[/graph_core.py:GraphManager]>>
