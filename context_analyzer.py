 @@ -1,74 +1,142 @@
 import nltk
 import pytest
 from nltk.corpus import wordnet
 import requests
 from nltk.tokenize import word_tokenize
 import json
-from nltk import download
+from nltk import download, data
 
 
 BASE_URL = "http://localhost:5000"
 # Ensure necessary NLTK resources are downloaded
+try:
+    data.find('tokenizers/punkt')
+except nltk.downloader.DownloadError:
+    download('punkt')
 
-download('punkt')
 # --- Helper function to check for errors in response ---
-download('wordnet')
+try:
+    data.find('corpora/wordnet')
+except nltk.downloader.DownloadError:
+    download('wordnet')
+
 def assert_error_response(response, status_code, error_message_part=None):
-
     assert response.status_code == status_code
+    try:
+        error_data = response.json().get('error')
+        assert error_data is not None
+        if error_message_part:
+            assert error_message_part in error_data
+    except json.JSONDecodeError:
+        pytest.fail(f"Response is not valid JSON: {response.text}")
+
 class ContextAnalyzer:
-    error_data = response.json().get('error')
     def __init__(self):
-    assert error_data is not None
         self.tokenizer = word_tokenize
-    if error_message_part:
 
-        assert error_message_part in error_data
     def get_semantic_similarity(self, word1, word2):
-
         """
-# --- Tests for /decode endpoint ---
         Calculate the semantic similarity between two words using WordNet.
-def test_decode_valid_acronym():
-        
-    response = requests.post(f"{BASE_URL}/decode", json={"acronym": "TIL", "context": "HR"})
         :param word1: First word
         :param word2: Second word
         :return: Similarity score (0.0 to 1.0)
-
         """
-def test_decode_unknown_context():
         synsets1 = wordnet.synsets(word1)
-    response = requests.post(f"{BASE_URL}/decode", json={"acronym": "TIL", "context": "unknown"})
         synsets2 = wordnet.synsets(word2)
-    assert response.status_code == 200
+        if not synsets1 or not synsets2:
+            return 0.0
+        max_similarity = 0.0
+        for synset1 in synsets1:
+            for synset2 in synsets2:
+                similarity = synset1.path_similarity(synset2)
+                if similarity and similarity > max_similarity:
+                    max_similarity = similarity
+        return max_similarity
 
-    assert response.json().get('expansion') == "Unknown context"
-        if not synsets1 or not synsets2:
-
-            return 0.0
-def test_decode_missing_acronym():
-
-    response = requests.post(f"{BASE_URL}/decode", json={"context": "General"})
-        max_similarity = 0.0
-    assert_error_response(response, 400, "acronym")
-        for synset1 in synsets1:
-
-            for synset2 in synsets2:
-def test_decode_empty_payload():
-                similarity = synset1.path_similarity(synset2)
-    response = requests.post(f"{BASE_URL}/decode", json={})
-                if similarity and similarity > max_similarity:
-    assert_error_response(response, 400, "acronym")
-                    max_similarity = similarity
-
-
-# --- Tests for /feedback endpoint ---
-        return max_similarity
     def analyze_context(self, sentence, target_word):
         """
         Analyze the context of a target word in a sentence.
-        
 
         :param sentence: The sentence to analyze
         :param target_word: The target word to focus on
         :return: A dictionary with surrounding words and their similarity scores
         """
-    assert_error_response(response, 400, "feedback")
         words = self.tokenizer(sentence)
 
         target_index = words.index(target_word) if target_word in words else -1
-# --- Tests for /add_acronym endpoint ---
 
-def test_add_acronym_success():
+        if target_index == -1:
+            return {}
+
+        context_words = words[max(0, target_index - 5):min(len(words), target_index + 6)]
+        if target_word in context_words:
+            context_words.remove(target_word)
+
+        similarity_scores = {}
+        for word in context_words:
+            similarity_scores[word] = self.get_semantic_similarity(target_word, word)
+
+        return similarity_scores
+
+# --- Tests for /decode endpoint ---
+def test_decode_valid_acronym():
+    response = requests.post(f"{BASE_URL}/decode", json={"acronym": "TIL", "context": "HR"})
+    assert response.status_code == 200
+    assert response.json().get('expansion') == "Time in Lieu"
+
+def test_decode_unknown_context():
+    response = requests.post(f"{BASE_URL}/decode", json={"acronym": "TIL", "context": "unknown"})
+    assert response.status_code == 200
+    assert response.json().get('expansion') == "Unknown context"
+
+def test_decode_missing_acronym():
+    response = requests.post(f"{BASE_URL}/decode", json={"context": "General"})
+    assert_error_response(response, 400, "acronym")
+
+def test_decode_empty_payload():
+    response = requests.post(f"{BASE_URL}/decode", json={})
+    assert_error_response(response, 400, "acronym")
+
+
+# --- Tests for /feedback endpoint ---
+def test_feedback_submission():
+    feedback_data = {"acronym": "TBD", "context": "General", "expansion": "To Be Determined", "feedback": "Looks good"}
+    response = requests.post(f"{BASE_URL}/feedback", json=feedback_data)
+    assert response.status_code == 200
+    assert response.json().get('message') == "Feedback received"
+
+def test_feedback_missing_fields():
+    feedback_data = {"acronym": "TBD", "context": "General", "expansion": "To Be Determined"} # Missing 'feedback'
+    response = requests.post(f"{BASE_URL}/feedback", json=feedback_data)
+    assert_error_response(response, 400, "feedback")
+
+# --- Tests for /add_acronym endpoint ---
+
+def test_add_acronym_success():
     new_acronym = {"acronym": "FYI", "context": "General", "expansion": "For Your Information"}
     response = requests.post(f"{BASE_URL}/add_acronym", json=new_acronym)
 
@@ -76,13 +144,11 @@
     assert response.json().get('message') == "Acronym added successfully"
 
 
-def test_add_acronym_duplicate():
+def test_add_acronym_duplicate():
     duplicate_acronym = {"acronym": "FYI", "context": "Another", "expansion": "Another meaning"}
-        for word in context_words:
     response = requests.post(f"{BASE_URL}/add_acronym", json=duplicate_acronym)
-            similarity_scores[word] = self.get_semantic_similarity(target_word, word)
     assert_error_response(response, 409, "Acronym already exists")
 
 
-        return similarity_scores
 def test_add_acronym_missing_fields():
 
     new_acronym = {"acronym": "BRB", "context": "General"} # Missing 'expansion'
@@ -90,7 +156,7 @@
     assert_error_response(response, 400, "expansion")
     analyzer = ContextAnalyzer()
 
-
+# Assuming a maximum length constraint for 'acronym'
 def test_add_large_acronym():
     # Test Case 1: "The Apple Inc. product is popular."
     large_acronym = {"acronym": "A" * 256, "context": "General", "expansion": "A long acronym"}
@@ -98,11 +164,12 @@
     response = requests.post(f"{BASE_URL}/add_acronym", json=large_acronym)
     target_word1 = "Apple"
     assert_error_response(response, 400, "acronym") # Assuming an error message containing "acronym"
-    print(f"Analyzing context for '{target_word1}' in: {sentence1}")
+    # print(f"Analyzing context for '{target_word1}' in: {sentence1}")
+    # print(analyzer.analyze_context(sentence1, target_word1))
 
-    print(analyzer.analyze_context(sentence1, target_word1))
+# Assuming a maximum length constraint for 'acronym'
 def test_add_acronym_max_length():
-
+    # Assuming max length is 50
     max_length_acronym = {"acronym": "B" * 50, "context": "Test", "expansion": "Valid long expansion"} # Assuming max length is 50
     # Test Case 2: "The bank is next to the river."
     response = requests.post(f"{BASE_URL}/add_acronym", json=max_length_acronym)
@@ -110,10 +177,11 @@
     target_word2 = "bank"
 
     print(f"Analyzing context for '{target_word2}' in: {sentence2}")
+    print(analyzer.analyze_context(sentence2, target_word2))
+
 def test_add_acronym_just_over_max_length():
-    print(analyzer.analyze_context(sentence2, target_word2))
+    # Assuming max length is 50
     over_length_acronym = {"acronym": "C" * 51, "context": "Test", "expansion": "Invalid long expansion"} # Assuming max length is 50
     response = requests.post(f"{BASE_URL}/add_acronym", json=over_length_acronym)
     assert_error_response(response, 400, "acronym") # Assuming an error message containing "acronym"
