from typing import Dict, List


class Node:
    def __init__(self, accepting: bool, transitions: Dict[str, List['Node']]):
        self._accepting = accepting
        self._transitions = transitions

    @property
    def accepting(self) -> bool:
        return self._accepting

    @property
    def transitions(self) -> Dict[str, List['Node']]:
        return self._transitions
