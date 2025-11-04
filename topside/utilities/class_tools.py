"""A collection of little classes that perform useful functions.

Classes:
    Toggle:
        A simple class that toggles between True and False when called and returns the current state when cast to a bool
        or printed.
    ArgumentativeFunction:
        Describes a function and the arguments to be called with it. Can be called to execute the function.
"""
import time
from typing import Callable, Literal


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


class Stopwatch:
    """Describes a timer for determining time since it was started. Allows for pausing and resuming."""

    def __init__(self, mode: Literal["nano", "sec"] = "nano") -> None:
        """Initialize the Stopwatch object.

        Args:
            mode (Literal["nano", "sec"], optional):
                The mode of the stopwatch. "nano" indicates that returned values will be in nanoseconds, while "sec"
                indicates that returned values will be in seconds.
                Defaults to "nano".
        """
        self._mode: str = mode

        self.start_time: int | float | None = None
        self.stop_time: int | float | None = None
        self.elapsed_time: int | float | None = None

    def start(self) -> None:
        """Start or resume the stopwatch."""
        if self.start_time is None:
            self.start_time = self.get_time()

        self.stop_time = None

    def stop(self) -> int | float:
        """Stop the stopwatch.

        Returns:
            (int | float): The number of seconds or nanoseconds elapsed, depending on the mode.
        """
        if self.start_time is not None:
            self.stop_time = self.get_time()

        if self.elapsed_time is None:
            self.elapsed_time = 0 if self._mode == "nano" else 0.0

        self.elapsed_time += self.stop_time - self.start_time

        return self.elapsed_time

    def reset(self) -> None:
        """Reset the stopwatch."""
        self.start_time = None
        self.stop_time = None
        self.elapsed_time = None

    def get_time(self) -> int | float:
        """Get the current time in seconds or nanoseconds depending on the mode.

        Returns:
            (int | float): The current time in seconds or nanoseconds depending on the mode.
        """
        if self._mode == "nano":
            return time.time_ns()
        if self._mode == "sec":
            return time.time()

    def __call__(self, *args, **kwargs) -> object:
        return self.elapsed_time + self.get_time() - self.start_time
