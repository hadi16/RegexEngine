class State:
    """
    State
    Class to define a state of an NFA, identifiable by an id.
    """

    def __init__(self, state_id: int):
        self.state_id = state_id

    def __str__(self):
        return 'State ' + str(self.state_id)

    def __repr__(self):
        return str(self)
