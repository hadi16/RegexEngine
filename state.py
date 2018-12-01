class State:
    """
    State
    Class to define a state of an NFA, identifiable by an id.
    """

    def __init__(self, state_id: int):
        """
        __init__
        Creates a new State.

        :param state_id: The ID to set the state to.
        """

        self.state_id = state_id

    def __str__(self) -> str:
        """
        __str__
        Returns a string representation of the state (which is its ID).
        :return: The string representation of the state.
        """

        return 'State ' + str(self.state_id)

    def __repr__(self) -> str:
        """
        __repr__
        Returns what __str__ is set to.

        :return: A string representation of the State from __str__.
        """

        return str(self)
