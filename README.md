import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn
save_metadata(f1, self.label_encoder.classes_)
# Train the model and get the f1_score manually
f1_score = manager.train_model(acronym_data)

# Save metadata
save_metadata(f1_score, manager.label_encoder.classes_)
def train_model(self, data: List[Dict[str, str]]) -> float:
    ...
    self.model.fit(X_train, y_train)
    f1 = f1_score(y_test, self.model.predict(X_test), average='weighted')
    ...
    return f1
    
def get_contextual_meaning(letter, surrounding_words):
    """
    Generate a contextual meaning for a letter based on surrounding words.
    
    Args:
    - letter (str): The letter whose meaning needs to be generated.
    - surrounding_words (list): A list of words surrounding the target word.
    
    Returns:
    - str: A contextual meaning of the letter.
    """
    meanings = []
    
    # Iterate through the surrounding words to understand the context
    for word in surrounding_words:
        synsets = wn.synsets(word)
        if synsets:
            # Use the first synset's lemma names as potential meanings
            meanings.extend([lemma.name() for lemma in synsets[0].lemmas()])
    
    # Here, we're simply returning the first meaning related to the letter
    # This could be expanded with domain-specific knowledge
    return meanings[0] if meanings else "unknown"

def encode_word_with_context(word, surrounding_words):
    """
    Encodes a word into a numeric vector based on the alphabet-to-number mapping,
    but modifies each letter's encoding based on surrounding context.
    
    Args:
    - word (str): The word to encode.
    - surrounding_words (list): List of surrounding words for contextual analysis.
    
    Returns:
    - List[int]: A list of integers representing the word with contextual adjustments.
    """
    encoded_word = []
    
    for char in word.upper():
        if char.isalpha():
            # Get the contextual meaning of the letter based on surrounding words
            meaning = get_contextual_meaning(char, surrounding_words)
            
            # Adjust the letter encoding based on the contextual meaning
            letter_encoding = (ord(char) - ord('A') + 1)  # Basic encoding (1-26)
            
            # Here, we could adjust encoding based on the meaning, for now, we use the length of meaning
            # As a simple proxy, we modify the encoding based on the length of the meaning
            contextual_encoding = letter_encoding + len(meaning)
            encoded_word.append(contextual_encoding)
        else:
            encoded_word.append(0)  # For non-alphabetic characters (e.g., spaces)
    
    return encoded_word

def add_to_graph(graph, word, relationships, surrounding_words):
    """
    Adds a new word (acronym) to the graph and updates relationships.
    
    Args:
    - graph (networkx.Graph): The existing graph.
    - word (str): The new word (acronym) to add.
    - relationships (list): A list of relationships (edges) with other words.
    - surrounding_words (list): List of surrounding words for contextual analysis.
    """
    # Add the new word as a node with context-aware encoding
    graph.add_node(word, encoded=encode_word_with_context(word, surrounding_words))
    
    # Add relationships (edges) with other words
    for related_word in relationships:
        graph.add_edge(word, related_word)

# Create an empty graph
graph = nx.Graph()

# Example of adding a new word and relationships
add_to_graph(graph, "cloudy", ["weather", "humidity"], ["temperature", "rain", "storm"])

# Visualize the updated graph
nx.draw(graph, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold")
plt.show()
