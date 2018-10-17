from node import Node
from typing import List


class Nfa:
    def __init__(self, initial_node: Node, accepting_nodes: List[Node]):
        self.initial_node = initial_node
        self.accepting_nodes = accepting_nodes
