import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import download

# Ensure necessary NLTK resources are downloaded
download('punkt')
download('wordnet')

class ContextAnalyzer:
    def __init__(self):
        self.tokenizer = word_tokenize

    def get_semantic_similarity(self, word1, word2):
        """
        Calculate the semantic similarity between two words using WordNet.
        
        :param word1: First word
        :param word2: Second word
        :return: Similarity score (0.0 to 1.0)
        """
        synsets1 = wordnet.synsets(word1)
        synsets2 = wordnet.synsets(word2)
        
        if not synsets1 or not synsets2:
            return 0.0
        
        max_similarity = 0.0
        for synset1 in synsets1:
            for synset2 in synsets2:
                similarity = synset1.path_similarity(synset2)
                if similarity and similarity > max_similarity:
                    max_similarity = similarity
        
        return max_similarity

    def analyze_context(self, sentence, target_word):
        """
        Analyze the context of a target word in a sentence.
        
        :param sentence: The sentence to analyze
        :param target_word: The target word to focus on
        :return: A dictionary with surrounding words and their similarity scores
        """
        words = self.tokenizer(sentence)
        target_index = words.index(target_word) if target_word in words else -1
        
        if target_index == -1:
            return {}
        
        context_words = words[max(0, target_index - 5):min(len(words), target_index + 6)]
        context_words.remove(target_word)
        
        similarity_scores = {}
        for word in context_words:
            similarity_scores[word] = self.get_semantic_similarity(target_word, word)
        
        return similarity_scores

# Example usage and testing
if __name__ == "__main__":
    analyzer = ContextAnalyzer()
    
    # Test Case 1: "The Apple Inc. product is popular."
    sentence1 = "The Apple Inc. product is popular."
    target_word1 = "Apple"
    print(f"Analyzing context for '{target_word1}' in: {sentence1}")
    print(analyzer.analyze_context(sentence1, target_word1))
    
    # Test Case 2: "The bank is next to the river."
    sentence2 = "The bank is next to the river."
    target_word2 = "bank"
    print(f"Analyzing context for '{target_word2}' in: {sentence2}")
    print(analyzer.analyze_context(sentence2, target_word2))
