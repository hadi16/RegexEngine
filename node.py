from typing import Dict, List


class Node:
    def __init__(self, transitions: Dict[str, List['Node']]):
        self.transitions = transitions
