import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict

# GraphManager Class for handling graph-based word relationships
class GraphManager:
    def __init__(self):
        """ Initializes a GraphManager instance. """
        # Initialize the graph instance using NetworkX
        self.graph = nx.Graph()

    def add_word(self, word: str, relationships: List[str] = [], encoded_vector: List[int] = []):
        """
        Adds a word to the graph with encoded vector and relationships.
        """
        self.graph.add_node(word, encoded=encoded_vector)
        for related_word in relationships:
            self.graph.add_edge(word, related_word)

    def visualize(self):
        """
        Visualizes the graph using matplotlib to render nodes with labels.
        """
        # Generate the visualization of the graph
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', font_size=12, node_size=5000, font_weight='bold', edge_color='gray')
        plt.title('Word Relationship Graph')
        plt.show()

    def get_neighbors(self, word: str) -> List[str]:
        """
        Returns a list of words directly connected to the specified word.
        
        Parameters:
        word (str): The word for which we want to find neighbors.
        
        Returns:
        list: List of neighboring words.
        """
        return list(self.graph.neighbors(word)) if word in self.graph else []


# TransformationSystem Class to handle dynamic transformations and state management
class TransformationSystem:
    def __init__(self, context_influence: Dict[str, Dict[str, int]] = None):
        """
        Initializes the TransformationSystem with optional context influence.
        Parameters:
        context_influence (dict, optional): A dictionary defining how context should influence the system. Defaults to None.
        """
        self.context_influence = context_influence
        self.system_state = {}
        self.state_change = {}

    def execute(self, action: str, vowel: str = None, parameters: Dict[str, int] = None):
        """
        Executes the action based on vowel-based flow control, context influence, and core logic.
        
        Parameters:
        action (str): The action to execute (e.g., "Start", "Branch", "Merge").
        vowel (str, optional): The vowel that influences the flow (e.g., 'a', 'e', etc.). Defaults to None.
        parameters (dict, optional): Additional parameters influencing the action. Defaults to None.
        
        Returns:
        tuple: Contains state_change, output_effect, and the updated system_state.
        """
        try:
            # Handle vowel-based flow control and action execution
            if vowel:
                self._apply_vowel_flow(vowel, parameters)
            
            # Apply contextual influence if defined
            if self.context_influence:
                self._apply_contextual_influence(action)
            
            # Perform the action
            output_effect = self._perform_action(action, parameters)
            self.state_change = self.system_state.copy()  # Capture state change
            return self.state_change, output_effect, self.system_state
        
        except KeyError as e:
            # Handle missing parameter or state key errors
            print(f"Error: Missing key {e}")
            return {}, "Error: Missing key", self.system_state
        
        except Exception as e:
            # Handle any other unexpected errors
            print(f"Unexpected error: {e}")
            return {}, "Unexpected error", self.system_state

    def _apply_vowel_flow(self, vowel: str, parameters: Dict[str, int]):
        """
        Applies vowel-based flow control to modify the system’s state.
        
        Parameters:
        vowel (str): The vowel that influences the transformation.
        parameters (dict): Parameters that determine how the vowel flow is applied.
        """
        # Example: Influence system state based on the vowel
        flow_intensity = parameters.get('intensity', 1)
        self.system_state['vowel'] = vowel
        self.system_state['flow_intensity'] = flow_intensity
        # Add more flow logic depending on vowel (for example, 'a' could increase speed, 'e' could increase scope)

    def _apply_contextual_influence(self, action: str):
        """
        Modifies the system state based on the defined context (e.g., Start, Branch, etc.).
        
        Parameters:
        action (str): The action being executed that could influence the context.
        """
        if action in self.context_influence:
            context_effect = self.context_influence[action]
            self.system_state.update(context_effect)

    def _perform_action(self, action: str, parameters: Dict[str, int]):
        """
        Executes core actions like initiation, branching, merging, and filtering.
        
        Parameters:
        action (str): The action to perform.
        parameters (dict): Parameters that may influence the action.
        
        Returns:
        str: A message describing the outcome of the action.
        """
        if action == "Start":
            self.system_state['status'] = "Started"
            return "System Started"
        elif action == "Branch":
            self.system_state['status'] = "Branching"
            return "System Branching"
        elif action == "Merge":
            self.system_state['status'] = "Merging"
            return "System Merging"
        elif action == "Filter":
            self.system_state['status'] = "Filtering"
            return "System Filtering"
        else:
            self.system_state['status'] = "Unknown Action"
            return "Unknown Action"


# Example Usage

# GraphManager Example
graph_manager = GraphManager()
graph_manager.add_word("apple", relationships=["banana"], encoded_vector=[1, 2, 3])
graph_manager.add_word("banana", relationships=["apple"], encoded_vector=[4, 5, 6])
graph_manager.visualize()

# Setting up transformation system with contextual influence
context_influence = { 
    "Start": {"threshold": 10}, 
    "Branch": {"threshold": 20}, 
    "Combine": {"threshold": 30} 
}
transformation_system = TransformationSystem(context_influence)
state_change, output_effect, system_state = transformation_system.execute("Start", vowel="a", parameters={'intensity': 5})

print(state_change, output_effect, system_state)
