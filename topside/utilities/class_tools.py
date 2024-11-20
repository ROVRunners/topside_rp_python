"""A collection of little classes that perform useful functions."""


class Toggle:
    """A simple class that toggles between True and False when called and returns the current state when cast to a bool
    or printed.

    Attributes:
        state (bool):
            The current state of the Toggle.
    """
    def __init__(self, state=False) -> None:
        """Initialize the Toggle object.

        Args:
            state (bool, optional):
                The initial state of the Toggle.
                Defaults to False.
        """
        self.state = state

    def __call__(self) -> bool:
        self.state = not self.state
        return self.state

    def __bool__(self) -> bool:
        return self.state

    def __repr__(self) -> str:
        return str(self.state)
