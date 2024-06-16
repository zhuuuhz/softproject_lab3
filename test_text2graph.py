import pytest
import networkx as nx
from text2graph import create_digraph_from_file, find_bridge_words, find_shortest_path, process_text_with_bridge_words, find_shortest_paths_to_other_words, random_traversal

@pytest.fixture
def file_path(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    file_path = d / "testfile.txt"
    file_path.write_text("Hello, world! This is a test.\nHello again.")
    return file_path

@pytest.fixture
def sample_graph(file_path):
    return create_digraph_from_file(file_path)

def test_create_directed_graph(file_path):
    graph = create_digraph_from_file(file_path)
    assert graph.has_edge("Hello", "world")
    assert graph["Hello"]["world"]["weight"] == 1

def test_find_bridge_words(sample_graph):
    assert find_bridge_words(sample_graph, "Hello", "This") == ["world"]
    assert find_bridge_words(sample_graph, "This", "a") == ["is"]
    assert find_bridge_words(sample_graph, "not_in_graph", "a") == "No word1 or word2 in the graph!"
    assert find_bridge_words(sample_graph, "This", "not_in_graph") == "No word1 or word2 in the graph!"
    assert find_bridge_words(sample_graph, "a", "Hello") == []

def test_insert_bridge_words(sample_graph):
    new_text = "Hello This is a test"
    result = process_text_with_bridge_words(sample_graph, new_text)
    assert result in ["Hello world This is a test"]

def test_find_shortest_path(sample_graph):
    assert find_shortest_path(sample_graph, "Hello", "test") == ["Hello", "world", "This", "is", "a", "test"]
    # assert find_shortest_path(sample_graph, "Hello", "not_in_graph") == "No word1 or word2 in the graph!"
    # assert find_shortest_path(sample_graph, "not_in_graph", "Hello") == "No word1 or word2 in the graph!"
    assert find_shortest_path(sample_graph, "a", "Hello") == None
    # assert find_shortest_path(sample_graph, "Hello", "") == {'world': ['Hello', 'world'], 'This': ['Hello', 'world', 'This'], 'is': ['Hello', 'world', 'This', 'is'], 'a': ['Hello', 'world', 'This', 'is', 'a'], 'test': ['Hello', 'world', 'This', 'is', 'a', 'test'], 'again': ['Hello', 'again']}

def test_random_traversal(sample_graph):
    nodes, edges = random_traversal(sample_graph)
    assert isinstance(nodes, list)
    assert isinstance(edges, list)
    assert len(nodes) > 0
    assert len(edges) >= 0
