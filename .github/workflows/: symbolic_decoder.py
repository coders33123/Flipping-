networkx==3.1
pytest==8.3.5
flake8
import networkx as nx
from typing import Dict, List, Tuple

# Core scoring function for symbolic transitions
def symbolic_score(base_weight: float, metadata: Dict) -> float:
    flip_depth = metadata.get("flip_depth", 1)
    vowel_flow = metadata.get("vowel_flow", False)
    symbolic_modifier = 1.2 if vowel_flow else 1.0
    return base_weight * symbolic_modifier / flip_depth

# Symbolic Graph Handler
class SymbolicGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_edge(self, from_node: str, to_node: str, base_weight: float, metadata: Dict = {}):
        weight = symbolic_score(base_weight, metadata)
        self.graph.add_edge(from_node, to_node, weight=weight, metadata=metadata)

# Symbolic Viterbi-style Decoder
class SymbolicViterbi:
    def __init__(self, graph: SymbolicGraph, scoring_function):
        self.graph = graph.graph
        self.score_fn = scoring_function

    def decode(self, start: str, end: str, top_n: int = 1) -> List[Tuple[List[str], float]]:
        all_paths = list(nx.all_simple_paths(self.graph, source=start, target=end, cutoff=10))
        path_scores = []
        for path in all_paths:
            total_score = 0.0
            for i in range(len(path) - 1):
                edge = self.graph.get_edge_data(path[i], path[i + 1])
                if edge:
                    total_score += edge["weight"]
            path_scores.append((path, total_score))
        path_scores.sort(key=lambda x: x[1], reverse=True)
        return path_scores[:top_n]

# Complete Decoder System
class SymbolicDecoderSystem:
    def __init__(self):
        self.graph = SymbolicGraph()
        self.viterbi = SymbolicViterbi(self.graph, symbolic_score)

    def add_transition(self, from_node: str, to_node: str, base_weight: float = 1.0, metadata: Dict = {}):
        self.graph.add_edge(from_node, to_node, base_weight, metadata)

    def find_optimal_paths(self, start: str, end: str, top_n: int = 1) -> List[Tuple[List[str], float]]:
        return self.viterbi.decode(start, end, top_n)

# Example use
if __name__ == "__main__":
    decoder = SymbolicDecoderSystem()
    transitions = [
        ("identity", "ide", 1.2, {"flip_depth": 1}),
        ("ide", "it", 0.9, {"flip_depth": 1}),
        ("it", "ati", 0.7, {"flip_depth": 2}),
        ("ati", "viterbi", 0.5, {"flip_depth": 3}),
        ("ati", "vit", 0.6, {"flip_depth": 2}),
        ("vit", "viterbi", 0.3, {"flip_depth": 1}),
    ]
    for from_node, to_node, weight, meta in transitions:
        decoder.add_transition(from_node, to_node, weight, meta)

    results = decoder.find_optimal_paths("identity", "viterbi", top_n=2)
    for path, score in results:
        print("Path:", " → ".join(path), "| Score:", round(score, 2))
        from symbolic_decoder import SymbolicDecoderSystem

def test_symbolic_decoder():
    decoder = SymbolicDecoderSystem()
    transitions = [
        ("identity", "ide", 1.2, {"flip_depth": 1}),
        ("ide", "it", 0.9, {"flip_depth": 1}),
        ("it", "ati", 0.7, {"flip_depth": 2}),
        ("ati", "viterbi", 0.5, {"flip_depth": 3}),
    ]
    for from_node, to_node, weight, meta in transitions:
        decoder.add_transition(from_node, to_node, weight, meta)

    results = decoder.find_optimal_paths("identity", "viterbi", top_n=1)
    assert results[0][0] == ['identity', 'ide', 'it', 'ati', 'viterbi']
    assert results[0][1] > 0
    name: Python application

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

    - name: Test with pytest
      run: |
        pytest test_symbolic_decoder.py
