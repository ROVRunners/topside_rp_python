"""A collection of little classes that perform useful functions.

Classes:
    Toggle:
        A simple class that toggles between True and False when called and returns the current state when cast to a bool
        or printed.
    ArgumentativeFunction:
        Describes a function and the arguments to be called with it. Can be called to execute the function.
"""
from typing import Callable


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


class ArgumentativeFunction:
    """Describes a function and the arguments to be called with it. Can be called to execute the function.

    Attributes:
        func (Callable[[...], object]):
            The function to be called.
        args (tuple):
            The arguments to be passed to the function.
        kwargs (dict):
            The keyword arguments to be passed to the function.
    """

    def __init__(self, func: Callable, *args, **kwargs) -> None:
        """Initialize the ArgumentativeFunction object.

        Args:
            func (Callable[[...], object]):
                The function to be called.
            args (tuple):
                The arguments to be passed to the function.
            kwargs (dict):
                The keyword arguments to be passed to the function.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self) -> object:
        return self.func(*self.args, **self.kwargs)
