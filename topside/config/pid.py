from typing import NamedTuple


class PIDConfig(NamedTuple):
    """Describe a PID configuration.

    Attributes:
        p (float):
            The proportional gain.
        i (float):
            The integral gain.
        d (float):
            The derivative gain.
        output (tuple[float, float]):
            The range the output can be in.
    """
    p: float = 1
    i: float = 0
    d: float = 0
    output: tuple[float, float] = (-1, 1)
